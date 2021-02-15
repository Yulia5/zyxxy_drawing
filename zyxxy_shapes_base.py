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
import matplotlib.pyplot as plt

import zyxxy_coordinates
from zyxxy_utils import rotate_point, stretch_something
import matplotlib.lines, matplotlib.patches
from zyxxy_shapes_colour_style import set_fill_in_outline_kwarg_defaults, get_line_style, get_patch_style

##################################################################
## CANVAS HELPERS                                               ## 
##################################################################
def get_width(ax=None):
  if ax is None:
    ax = plt.gca()
  xlims = ax.set_xlim()
  return (xlims[1] - xlims[0])

def get_height(ax=None):
  if ax is None:
    ax = plt.gca()
  ylims = ax.set_ylim()
  return (ylims[1] - ylims[0])


##################################################################
## MOVEMENT HELPERS                                             ## 
##################################################################
def _get_xy(something):
  if isinstance(something, np.ndarray):
    return something
  elif isinstance(something, matplotlib.lines.Line2D):
    return something.get_xydata()
  elif isinstance(something, matplotlib.patches.Polygon):
    return something.get_xy()
  raise Exception("Data type ", type(something), " is not handled")

def _set_xy(something, xy):
  if isinstance(something, np.ndarray):
    something = xy
  elif isinstance(something, matplotlib.lines.Line2D):
    something.set_xdata(xy[:, 0])
    something.set_ydata(xy[:, 1])
  elif isinstance(something, matplotlib.patches.Polygon):
    something.set_xy(xy)
  else:
    raise Exception("Data type ", type(something), " is not handled")
  return something

class Shape:
  def __init__(self, ax, defaults_for_demo=False, **kwargs):

    if ax is None:
      self.ax = plt.gfa()
    else:
      self.ax = ax

    kwargs = set_fill_in_outline_kwarg_defaults(kwargs=kwargs, 
                                                defaults_for_demo=defaults_for_demo)

    self.diamond_coords = np.array([0, 0])
    self.diamond_contour = (np.array([[1, 0], [0, -1], [-1, 0], [0, 1]]) * 
                                   (get_width(ax=ax)*kwargs["diamond_size"]))
    self.clip_patch = None
    self.clip_line = None

    (self.line, ) = self.ax.plot([0, 0, 1], [0, 1, 1], **get_line_style("line", kwargs))    
    (self.outline, ) = self.ax.plot([0, 0, 1], [0, 1, 1], **get_line_style("outline", kwargs))
    
    self.patch = plt.Polygon(np.array([[0,0], [0,1], [1,1]]), **get_patch_style("patch", kwargs))
    self.ax.add_patch(self.patch)

    self.diamond_patch = plt.Polygon(self.diamond_contour, **get_patch_style("diamond", kwargs))
    self.ax.add_patch(self.diamond_patch)

    for s in [self.patch, self.line, self.outline]:
      add_to_layer_record(what_to_add=s)

  def update_xy_by_shapename(self, shapename, **kwargs):
    method_to_call = getattr(zyxxy_coordinates, 'build_'+shapename)
    contour = method_to_call(**kwargs)

    # updating the shapes
    if self.line is not None:
      if shapename not in ['a_line', 'a_smile', 'a_coil', 'an_arc', 'a_zigzag', 'a_wave']: # the only open shapes
        line_to_plot = np.append(contour, contour[0:2], axis=0)
      else:
        line_to_plot = contour
      _set_xy(self.line, line_to_plot)
    if self.outline is not None:
      if (np.array(contour)).shape[0] > 2:
        contour_to_plot = np.append(contour, contour[0:2], axis=0)
      else:
        contour_to_plot = contour
      _set_xy(self.outline, contour_to_plot)
      # raise Exception(_get_xy(self.outline)) 
    if self.patch is not None:
      _set_xy(self.patch, contour)
    
    # updating the diamond
    self.update_diamond(new_diamond_coords=np.array([0, 0]))

  def redraw_on_axes(self):
    what_to_redraw = self.get_what_to_move() + [self.diamond_patch]
    for something in what_to_redraw:
      if something is not None:
        my_ax = something.axes
        try:
          my_ax.draw_artist(something)
        except Exception as inst:
          raise Exception(inst.args, _get_xy(something))

  def update_given_shapename(self, shapename, kwargs_shape, kwargs_common):
    self.update_xy_by_shapename(shapename, **kwargs_shape)
    if kwargs_common['flip']:
      self.flip()
    self.set_new_diamond_and_shift(new_diamond_coords=kwargs_common['diamond'])
    self.stretch(stretch_x=kwargs_common['stretch_x'], stretch_y=kwargs_common['stretch_y'])
    self.rotate(turn=kwargs_common['turn'])

  def add_clip_outline(self, clip_outline):
    if type(clip_outline) is plt.Polygon:
      clip_contour = clip_outline.get_xy()
    else:
      clip_contour = clip_outline

    if self.patch is not None:
      self.clip_patch = plt.Polygon(clip_contour, 
                               fc = 'none', 
                               ec = 'none',
                               zorder = self.patch_zorder)
      _ax = self.patch.axes
      _ax.add_patch(self.clip_patch)
      self.patch.set_clip_path(self.clip_patch)
    
    if (self.outline is not None) or (self.line is not None): 
      self.clip_line = plt.Polygon(clip_contour, 
                               fc = 'none', 
                               ec = 'none',
                               zorder = self.line_zorder)
      if self.outline is not None:
        _ax = self.outline.axes
        _ax.add_patch(self.clip_line)
        self.outline.set_clip_path(self.clip_line)
      if self.line is not None:
        _ax = self.line.axes
        _ax.add_patch(self.clip_line)
        self.line.set_clip_path(self.clip_line)

    add_to_layer_record(what_to_add=self.clip_line)
    add_to_layer_record(what_to_add=self.clip_patch)
  
  def update_diamond(self, new_diamond_coords):
    self.diamond_coords = np.array(new_diamond_coords)
    if self.diamond_patch is not None:                  
      _set_xy(something=self.diamond_patch, 
              xy=self.diamond_coords+self.diamond_contour)

  def get_what_to_move(self):
    return [self.line, self.patch, self.outline, self.clip_patch, self.clip_line]

  def set_visible(self, val):
    if val is None:
      what_to_hide = self.get_what_to_move()
      for something in what_to_hide:
        if something is not None:
          something.set_visible(False)
    else:
      for something in [self.patch, self.outline, self.clip_patch]:
        if something is not None:
          something.set_visible(val)
      for something in [self.line, self.clip_line]:
        if something is not None:
          something.set_visible(not val)
    self.diamond_patch.set_visible(val is not None)

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