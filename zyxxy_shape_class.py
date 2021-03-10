########################################################################
## Draw With Zixxy (or Zixxy Drawings, or Drawing With Zyxxy)
## (C) 2021 by Yulia Voevodskaya (draw.with.zyxxy@outlook.com)
## 
##  This program is free software: you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation, either version 3 of the License, or
##  (at your option) any later version.
##  See <https://www.gnu.org/licenses/> for the specifics.
##  
##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License for more details.
########################################################################

import numpy as np
from matplotlib.pyplot import Polygon
import zyxxy_coordinates
from zyxxy_utils import rotate_point, stretch_something
from zyxxy_shape_style import set_patch_style, set_line_style, get_diamond_size, format_arg_dict
from MY_zyxxy_SETTINGS import my_default_colour_etc_settings
from zyxxy_shape_style import raise_Exception_if_not_processed

########################################################################
# handling shapes per layers
########################################################################

def get_all_shapes_in_layers(*args_layer_nb):
  if len(args_layer_nb) == 0:
    _shapes = Shape.all_shapes
  else:
    _shapes = [sh for sh in Shape.all_shapes if sh.get_layer_nb() in args_layer_nb]
  return _shapes

def get_all_polygons_in_layers(*args_layer_nb):
  _shapes = get_all_shapes_in_layers(*args_layer_nb)
  result = []
  for _sh in _shapes:
    result += _sh.get_what_to_move()
  return result

def shift_layer(shift, layer_nbs):
  _shapes = get_all_shapes_in_layers(*layer_nbs)
  for shape in _shapes:
    shape.shift(shift=shift)

def rotate_layer(turn, diamond, layer_nbs):
  _shapes = get_all_shapes_in_layers(*layer_nbs)
  for shape in _shapes:
    shape.rotate(turn=turn, diamond_override=diamond)

def stretch_layer(diamond, stretch_x=1., stretch_y=1., layer_nbs=[]):
  _shapes = get_all_shapes_in_layers(*layer_nbs)
  for shape in _shapes:
    shape.stretch(diamond_override=diamond, stretch_x=stretch_x, stretch_y=stretch_y)

##################################################################
## SHAPE                                                        ## 
##################################################################

class Shape:


  all_shapes = []

##################################################################
  def _get_xy(something):
    if isinstance(something, np.ndarray):
      return something
    elif isinstance(something, Polygon):
      return something.get_xy()
    raise Exception("Data type ", type(something), " is not handled")

  def _set_xy(something, xy):
    if isinstance(something, np.ndarray):
      something = xy
    elif isinstance(something, Polygon):
      something.set_xy(xy)
    else:
      raise Exception("Data type ", type(something), " is not handled")
    return something

 ################################################################## 

  def __init__(self, ax, shapetype):

    self.diamond_coords = np.array([0, 0])

    if shapetype == "patch":  
      self.patch = Polygon(np.array([[0,0], [0,1], [1,1]]), fill=True, closed=True)
      ax.add_patch(self.patch)
      self.outline = Polygon(np.array([[0,0], [0,1], [1,1]]), fill=False, closed=True) 
      ax.add_patch(self.outline)
      self.line = None
    elif shapetype == "line":
      self.patch = None
      self.outline = None
      self.line = Polygon(np.array([[0,0], [0,1], [1,1]]), fill=False, closed=False) 
      ax.add_patch(self.line)
    else:
      raise Exception(shapetype, "not a recognized shapetype")

    diamond_size = get_diamond_size(ax)
    if diamond_size is not None:
      self.diamond_contour = np.array([[1, 0], [0, -1], [-1, 0], [0, 1]]) * diamond_size
      self.diamond = Polygon(self.diamond_contour, fill=True, closed=True)
      ax.add_patch(self.diamond)
    else:
      self.diamond_contour = None
      self.diamond = None

    for attr_name in format_arg_dict.keys():
      _attr = getattr(self, attr_name)
      if _attr is None:
        continue
      if "line" in attr_name:
        set_line_style(_attr, **my_default_colour_etc_settings[attr_name])
      else:
        set_patch_style(_attr, **my_default_colour_etc_settings[attr_name])

    self.clip_patches = []
    self.move_history = {'flip' : False, 'stretch_x' : 1., 'stretch_y' : 1., 'turn' : 0}
    self.shape_kwargs = {}
    self.shapename = None
    Shape.all_shapes.append(self)

##################################################################

  def set_visible(self, s):
    for attr_name in format_arg_dict.keys():
      _attr = getattr(self, attr_name)
      if _attr is not None:
        _attr.set_visible(s)   

##################################################################

  def set_style(self, **kwargs):

    used_args = []
    for attr_name, arg_types in format_arg_dict.items():
      _attr = getattr(self, attr_name)
      if _attr is None:
        continue

      if attr_name in ["patch", "line"]:
        prefix = ""
      else:
        prefix = attr_name + "_"

      keys_for_kwargs = [prefix + at for at in arg_types]
      
      _kwargs = {key[len(prefix):] : value for key, value in kwargs.items() if key in keys_for_kwargs}

      if "line" in attr_name:
        set_line_style(_attr, **_kwargs)
      else:
        set_patch_style(_attr, **_kwargs)

      used_args += [prefix + k for k in _kwargs.keys()]

    raise_Exception_if_not_processed(kwarg_keys=kwargs.keys(), allowed_keys=used_args)

##################################################################

  def update_xy_by_shapename(self, shapename, **kwargs):
    if isinstance(shapename, str):
      method_to_call = getattr(zyxxy_coordinates, 'build_'+shapename)
      contour = method_to_call(**kwargs)
      self.shapename = shapename
      self.shape_kwargs = kwargs
    else:
      contour = shapename # assume that it's an array of coordinates

    # updating the elements
    for what in [self.line, self.outline, self.patch]:
      if what is not None:
        Shape._set_xy(what, contour)
    
    # updating the diamond
    self.update_diamond(new_diamond_coords=np.array([0, 0]))

##################################################################

  def update_shape_parameters(self, **kwargs):
    
    for key, value in kwargs.items():
      self.shape_kwargs[key] = value
    
    method_to_call = getattr(zyxxy_coordinates, 'build_'+self.shapename)
    contour = method_to_call(**self.shape_kwargs)
    for what in [self.line, self.outline, self.patch]:
      if what is not None:
        Shape._set_xy(what, contour)

    self.move(**self.move_history) # correct for clipping contours

    shift = self.diamond_coords # self.shift will restore the value of self.diamond_coords
    self.update_diamond(new_diamond_coords = [0., 0.])
    self.shift(shift=shift)

##################################################################

  def shift_shape_parameters(self, **kwargs):
    for key in kwargs.keys():
      kwargs[key]+= self.shape_kwargs[key]
    self.update_shape_parameters(**kwargs)

##################################################################

  def move(self, **kwargs_common):
    if 'flip' in kwargs_common and kwargs_common['flip']:
      self.flip()

    stretch = [1., 1.]
    if 'stretch_x' in kwargs_common:
      stretch[0] = kwargs_common['stretch_x']
    if 'stretch_y' in kwargs_common:
      stretch[1] = kwargs_common['stretch_y']
    self.stretch(stretch_x=stretch[0], stretch_y=stretch[1])

    if 'turn' in kwargs_common:
      self.rotate(turn=kwargs_common['turn'])

    shift = [0., 0.]
    if 'diamond_x' in kwargs_common:
      shift[0] = kwargs_common['diamond_x']
    if 'diamond_y' in kwargs_common:
      shift[1] = kwargs_common['diamond_y']
    self.shift(shift=shift)

##################################################################

  def get_xy(self):
    if self.patch is not None:
      return Shape._get_xy(self.patch)
    if self.line is not None:
      return Shape._get_xy(self.line)
    raise Exception("Unable to identify xy")

##################################################################

  def get_layer_nb(self):
    if self.patch is not None:
      return self.patch.zorder
    if self.line is not None:
      return self.line.zorder
    raise Exception("Unable to identify xy")

##################################################################

  def clip(self, clip_outline):
    for what in [self.patch, self.line, self.outline]:
      if what is None:
        continue
      clip_patch = None
      if isinstance(clip_outline, Shape):
        clip_xy = clip_outline.get_xy()
        for clip_candidate in [clip_outline.patch, clip_outline.line]:
          if clip_candidate is not None:
            if clip_candidate.get_zorder() == what.get_zorder():
              clip_patch = clip_candidate
      else:
        clip_xy = Shape._get_xy(clip_outline)
      if clip_patch is None:
        clip_patch = Polygon(clip_xy, 
                               fc = 'none', 
                               ec = 'none',
                               zorder = what.get_zorder())
        what.axes.add_patch(clip_patch)
        self.clip_patches.append(clip_patch)
        
      what.set_clip_path(clip_patch)

##################################################################
  
  def update_diamond(self, new_diamond_coords):
    self.diamond_coords = np.array(new_diamond_coords)
    if self.diamond is not None:                  
      Shape._set_xy(something=self.diamond, 
                    xy=self.diamond_coords+self.diamond_contour)

##################################################################

  def get_what_to_move(self):
    all_candidates = [self.line, self.patch, self.outline] + self.clip_patches
    result = [r for r in all_candidates if r is not None]
    return result

##################################################################

  def _move_xy(self, func):
    what_to_move = self.get_what_to_move()
    for something in what_to_move:
      xy = func(xy=Shape._get_xy(something=something))
      Shape._set_xy(something=something, xy=xy)

##################################################################

  def flip(self):
    def func(xy):
      xy[:, 1] = 2 * self.diamond_coords[1] - xy[:, 1]
      return xy

    self._move_xy(func=func)
    self.move_history['flip'] = not self.move_history['flip']
    self.move_history['turn'] =   - self.move_history['turn']

##################################################################

  def shift(self, shift):
    def func(xy):
      xy += shift
      return xy
    self._move_xy(func=func)

    self.update_diamond(new_diamond_coords = self.diamond_coords + shift)

##################################################################

  def rotate(self, turn, diamond_override = None):
    if turn == 0:
      return

    def func(xy):
      xy = np.array([rotate_point(point=point, diamond=self.diamond_coords, turn=turn) for point in xy])
      return xy

    self._move_xy(func=func)

    if diamond_override is not None:
      shift = - self.diamond_coords + rotate_point(
                                point=self.diamond_coords, diamond=diamond_override, turn=turn)
      self.shift(shift=shift)

    self.move_history['turn'] += turn

##################################################################

  def stretch(self, stretch_x, stretch_y, diamond_override = None):
    def func(xy):
      xy = stretch_something(what_to_stretch=xy, 
                             diamond=self.diamond_coords, 
                             stretch_coeff=[stretch_x, stretch_y])
      return xy
      
    self._move_xy(func=func)

    if diamond_override is not None:
      shift = - self.diamond_coords + stretch_something(what_to_stretch=self.diamond_coords, 
                                                 diamond=diamond_override, 
                                                 stretch_coeff=[stretch_x, stretch_y])
      self.shift(shift=shift)                                                 
  
