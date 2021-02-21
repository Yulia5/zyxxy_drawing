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
from zyxxy_shape_style import set_patch_style, set_line_style, raise_Exception_if_not_processed, get_diamond_size, format_arg_dict, get_default_arguments


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
## SHAPE                                                        ## 
##################################################################

class Shape:
  def __init__(self, ax, is_patch_not_line, defaults_for_demo):

    self.diamond_coords = np.array([0, 0])

    if is_patch_not_line:  
      self.patch = Polygon(np.array([[0,0], [0,1], [1,1]]), fill=True, closed=True)
      ax.add_patch(self.patch)
      self.outline = Polygon(np.array([[0,0], [0,1], [1,1]]), fill=False, closed=True) 
      ax.add_patch(self.outline)
      self.line = None
    else:
      self.patch = None
      self.outline = None
      self.line = Polygon(np.array([[0,0], [0,1], [1,1]]), fill=False, closed=False) 
      ax.add_patch(self.line)

    diamond_size = get_diamond_size(ax)
    if diamond_size is not None:
      self.diamond_contour = np.array([[1, 0], [0, -1], [-1, 0], [0, 1]]) * diamond_size
      self.diamond = Polygon(self.diamond_contour, fill=True, closed=True)
      ax.add_patch(self.diamond)
    else:
      self.diamond_contour = None
      self.diamond = None

    defaults_to_use = get_default_arguments(defaults_for_demo = defaults_for_demo)
    for attr_name in format_arg_dict.keys():
      _attr = getattr(self, attr_name)
      if _attr is None:
        continue
      if "line" in attr_name:
        set_line_style(_attr, **defaults_to_use[attr_name])
      else:
        set_patch_style(_attr, **defaults_to_use[attr_name])

    self.clip_patches = []
    self.move_history = []
    self.shape_kwargs = None
    self.shapename = None
    self.is_patch_not_line = is_patch_not_line


  def set_visible(self, s):
    for attr_name in format_arg_dict.keys():
      _attr = getattr(self, attr_name)
      if _attr is not None:
        _attr.set_visible(s)   

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

    raise_Exception_if_not_processed(kwarg_keys=kwargs.keys(), processed_keys=used_args)


  def update_xy_by_shapename(self, shapename, **kwargs):
    if isinstance(shapename, str):
      method_to_call = getattr(zyxxy_coordinates, 'build_'+shapename)
      contour = method_to_call(**kwargs)
    else:
      contour = shapename

    # updating the elements
    for what in [self.line, self.outline, self.patch]:
      if what is not None:
        _set_xy(what, contour)
    
    # updating the diamond
    self.update_diamond(new_diamond_coords=np.array([0, 0]))

  def move(self, **kwargs_common):
    if 'flip' in kwargs_common and kwargs_common['flip']:
      self.flip()
    diamond = [0., 0.]
    if 'diamond_x' in kwargs_common:
      diamond[0] = kwargs_common['diamond_x']
    if 'diamond_y' in kwargs_common:
      diamond[1] = kwargs_common['diamond_y']
    self.set_new_diamond_and_shift(new_diamond_coords=diamond)
    if 'stretch_x' in kwargs_common:
      self.stretch(stretch_x=kwargs_common['stretch_x'], stretch_y=1)
    if 'stretch_y' in kwargs_common:
      self.stretch(stretch_x=1, stretch_y=kwargs_common['stretch_y'])
    if 'turn' in kwargs_common:
      self.rotate(turn=kwargs_common['turn'])

  def get_xy(self):
    if self.patch is not None:
      return _get_xy(self.patch)
    if self.line is not None:
      return _get_xy(self.line)
    raise Exception("Unable to identify xy")

  def clip(self, clip_outline):
    for what in [self.patch, self.line, self.outline]:
      if what is None:
        continue
      if isinstance(clip_outline, Shape):
        clip_xy = clip_outline.get_xy()
      else:
        clip_xy = _get_xy(clip_outline)
      clip_patch = Polygon(clip_xy, 
                               fc = 'none', 
                               ec = 'none',
                               zorder = self.patch.get_zorder())
      what.axes.add_patch(clip_patch)
      what.set_clip_path(clip_patch)

      self.clip_patches.append(clip_patch)
  
  def update_diamond(self, new_diamond_coords):
    self.diamond_coords = np.array(new_diamond_coords)
    if self.diamond is not None:                  
      _set_xy(something=self.diamond, 
              xy=self.diamond_coords+self.diamond_contour)

  def get_what_to_move(self):
    return [self.line, self.patch, self.outline] + self.clip_patches

  def flip(self):
    what_to_move = self.get_what_to_move()
    for something in what_to_move:
      if something is None:
        continue
      xy = _get_xy(something=something)
      xy[:, 1] = 2 * self.diamond_coords[1] - xy[:, 1]
      _set_xy(something=something, xy=xy)

  def shift(self, shift):
    if shift is None:
      return
    what_to_move = self.get_what_to_move()
    for something in what_to_move:
      if something is None:
        continue
      xy = _get_xy(something=something)
      xy += shift
      _set_xy(something=something, xy=xy)
    self.update_diamond(new_diamond_coords = self.diamond_coords + shift)

  def set_new_diamond_and_shift(self, new_diamond_coords):
    if new_diamond_coords is None:
      return
    shift = -self.diamond_coords + new_diamond_coords
    what_to_move = self.get_what_to_move()
    for something in what_to_move:
      if something is None:
        continue
      xy = _get_xy(something=something)
      xy += shift
      _set_xy(something=something, xy=xy)
    self.update_diamond(new_diamond_coords = new_diamond_coords)

  def rotate(self, turn, diamond_override = None):
    if (turn is None) or (turn == 0):
      return
    if diamond_override is not None:
      diamond_to_use = diamond_override
      rotate_point(point=self.diamond_coords, diamond=diamond_override, turn=turn)
    else:
      diamond_to_use = self.diamond_coords
      
    what_to_move = self.get_what_to_move()
    for something in what_to_move:
      if something is None:
        continue
      xy = _get_xy(something=something)
      xy = np.array([rotate_point(point=point, diamond=diamond_to_use, turn=turn) for point in xy])
      _set_xy(something=something, xy=xy)

  def stretch(self, stretch_x, stretch_y, diamond_override = None):
    if diamond_override is not None:
      diamond_to_use = diamond_override
      self.diamond_coords[0] = stretch_something(what_to_stretch=self.diamond_coords[0], 
                                                 diamond=diamond_to_use[0], 
                                                 stretch_coeff=stretch_x)
      self.diamond_coords[1] = stretch_something(what_to_stretch=self.diamond_coords[1], 
                                                 diamond=diamond_to_use[1], 
                                                 stretch_coeff=stretch_y)
    else:
      diamond_to_use = self.diamond_coords

    what_to_move = self.get_what_to_move()
    for something in what_to_move:
      if something is None:
        continue
      xy = _get_xy(something=something)
      xy[:, 0] = stretch_something(what_to_stretch=xy[:, 0], 
                                                 diamond=diamond_to_use[0], 
                                                 stretch_coeff=stretch_x)
      xy[:, 1] = stretch_something(what_to_stretch=xy[:, 1], 
                                                 diamond=diamond_to_use[1], 
                                                 stretch_coeff=stretch_y)
      _set_xy(something=something, xy=xy)
  
########################################################################
# handling shapes per layers
########################################################################

_all_shapes_per_zorder = {}

def add_to_layer_record(what_to_add):
  if what_to_add is not None:
    zorder = what_to_add.get_zorder()
    if zorder not in _all_shapes_per_zorder:
      _all_shapes_per_zorder[zorder] = [what_to_add]
    else:
      _all_shapes_per_zorder[zorder] += [what_to_add]

def get_all_shapes_in_layers(*args):
  result = []
  if len(args) == 0:
    args = [k for k in _all_shapes_per_zorder.keys() if k>=0]
  for zorder in args:
    result += _all_shapes_per_zorder[zorder]
  return result

def shift_layer(layer_nb, shift):
  if layer_nb not in _all_shapes_per_zorder:
    return []
  for shape in _all_shapes_per_zorder[layer_nb]:
    shape.rotate(shift=shift)
  return _all_shapes_per_zorder[layer_nb]

def rotate_layer(layer_nb, turn, diamond):
  if layer_nb not in _all_shapes_per_zorder:
    return []
  for shape in _all_shapes_per_zorder[layer_nb]:
    shape.rotate(turn=turn, diamond=diamond)
  return _all_shapes_per_zorder[layer_nb]

def stretch_layer(layer_nb, diamond, stretch_x, stretch_y):
  if layer_nb not in _all_shapes_per_zorder:
    return []
  for shape in _all_shapes_per_zorder[layer_nb]:
    shape.rotate(diamond=diamond, stretch_x=stretch_x, stretch_y=stretch_y)
  return _all_shapes_per_zorder[layer_nb]