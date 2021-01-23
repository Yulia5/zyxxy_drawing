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
import matplotlib.colors as mcolors

from MY_zyxxy_SETTINGS import my_default_diamond_size, my_default_diamond_colour, my_colour_palette
import zyxxy_coordinates
from zyxxy_utils import rotate_point, stretch_something
import matplotlib.lines, matplotlib.patches

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
## DIAMOND HELPERS                                              ## 
##################################################################
_default_diamond_arguments = {
  'show' : False,
  'zorder' : 1000, 
  'size' : my_default_diamond_size,
  'colour' : my_default_diamond_colour
}

def set_diamond_style(show=None):
  global _default_diamond_arguments
  if show is not None:
    _default_diamond_arguments['show'] = show

##################################################################
## COLOUR HELPERS                                               ## 
##################################################################

# Find colour that should be used. 
# Assume that it's a name of a standard colour.
# Attention, names are case-sensitive
def find_colour_code(colour_name):
  if colour_name is None:
    return 'none'
  if colour_name in my_colour_palette:
    return my_colour_palette[colour_name] 
  if colour_name in mcolors.CSS4_COLORS:
    return colour_name # matplotlib knows how to handle it
  # If we are here, the colour name has not been recognised
  # Assuming that it is a colour code.
  return colour_name

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
  def __init__(self, ax, is_patch, patch_zorder, patch_colour, patch_alpha, line_colour, line_width, line_joinstyle, line_zorder):
    colour_code_patch = find_colour_code(colour_name = patch_colour)
    colour_code_line = find_colour_code(colour_name = line_colour)
    if ax is None:
      self.ax = plt.gfa()
    else:
      self.ax = ax

    self.patch_zorder = patch_zorder
    self.line_zorder = line_zorder
    self.diamond_coords = [0, 0]
    self.diamond_contour = build_a_regular_polygon(
      centre_x=0, centre_y=0, vertices_qty=4, 
      radius=(get_width(ax=ax)*_default_diamond_arguments['size']/1000))
    self.clip_patch = None
    self.clip_line = None

    dummy_line, = ax.plot([0, 0], [0, 1], lw=line_width, color=colour_code_line, zorder=line_zorder, solid_joinstyle=line_joinstyle)
    
    if is_patch:
      self.line = None
      self.outline = dummy_line
      self.patch = plt.Polygon(np.array([[0,0], [1,1], [1,0]]), #dummy 
                               fc = colour_code_patch, 
                               ec = 'none',
                               zorder = patch_zorder,
                               alpha = patch_alpha)
      self.ax.add_patch(self.patch)
    else:
      self.patch = None
      self.outline = None
      self.line, = dummy_line

    self.diamond_patch = plt.Polygon(self.diamond_contour, 
      fc = _default_diamond_arguments['colour'], 
      ec = 'none',
      zorder = _default_diamond_arguments['zorder'],
      alpha = 1.0)

    add_to_layer_record(what_to_add=self.patch)
    add_to_layer_record(what_to_add=self.line)
    add_to_layer_record(what_to_add=self.outline)

  def update_xy(self, shapename, **kwargs):
    method_to_call = getattr(zyxxy_coordinates, 'build_'+shapename)
    diamond_coords, contour = method_to_call(**kwargs)

    # updating the shapes
    if self.line is not None:
      _set_xy(self.line, contour)
    if self.outline is not None:
      _set_xy(self.outline, np.append(contour, contour[0:2], axis=0))
    if self.patch is not None:
      _set_xy(self.patch, contour)
    
    # updating the diamond
    self.update_diamond(new_diamond_coords=np.array(diamond_coords))

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
      self.ax.add_patch(self.clip_patch)
      self.patch.set_clip_path(self.clip_patch)
    
    if (self.outline is not None) or (self.line is not None): 
      self.clip_line = plt.Polygon(clip_contour, 
                               fc = 'none', 
                               ec = 'none',
                               zorder = self.line_zorder)
      if self.outline is not None:
        self.outline.set_clip_path(self.clip_line)
      if self.line is not None:
        self.line.set_clip_path(self.clip_line)

    add_to_layer_record(what_to_add=self.clip_line)
    add_to_layer_record(what_to_add=self.clip_patch)
  
  def update_diamond(self, new_diamond_coords):
    self.diamond_coords = new_diamond_coords
    if self.diamond_patch is not None:                  
      _set_xy(something=self.diamond_patch, 
              xy=self.diamond_coords+self.diamond_contour)

  def get_what_to_move(self):
    return [self.line, self.patch, self.outline, self.clip_patch, self.clip_line]

  def shift(self, shift):
    what_to_move = self.get_what_to_move()
    for something in what_to_move:
      if something is None:
        continue
      xy = _get_xy(something=something)
      xy += shift
      _set_xy(something=something, xy=xy)
    self.update_diamond(new_diamond_coords = self.diamond_coords + shift)

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
      self.diamond_coords[0] = stretch_something        (what_to_stretch=self.diamond_coords[0], 
                                                 diamond=diamond_to_use[0], 
                                                 stretch_coeff=stretch_x)
      self.diamond_coords[1] = stretch_something(what_to_stretch=self.diamond_coords[1], 
                                                 diamond=diamond_to_use[1], 
                                                 stretch_coeff=stretch_y)
    else:
      diamond_to_use = self.diamond_coords

    for something in [self.patch_or_line, self.outline, self.clip]:
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


def draw_given_shapename(ax, is_patch, shapename, shape_kwargs, diamond_x, diamond_y, stretch_x, stretch_y, turn, **kwargs):
  new_shape = Shape(ax=ax, is_patch=is_patch, **kwargs)
  new_shape.update_xy_by_shapename(shapename=shapename, **shape_kwargs)
  new_shape.shift(shift=[diamond_x, diamond_y])
  new_shape.stretch(stretch_x=stretch_x, stretch_y=stretch_y)
  new_shape.rotate(turn=turn)
  return new_shape

def draw_given_contour(ax, is_patch, contour, diamond_x, diamond_y, stretch_x, stretch_y, turn, **kwargs):
  new_shape = Shape(ax=ax, is_patch=is_patch, **kwargs)
  new_shape.update_xy_given_contour(contour=contour)
  new_shape.shift(shift=[diamond_x, diamond_y])
  new_shape.stretch(stretch_x=stretch_x, stretch_y=stretch_y)
  new_shape.rotate(turn=turn)
  return new_shape

def draw_a_rectangle(ax, width, height, left_x=None, centre_x=None, right_x=None, bottom_y=None, centre_y=None, top_y=None, **kwargs):
  diamond_best_guess, contour = zyxxy_coordinates.build_a_rectangle(
    width=width, height=height, 
    left_x=left_x, centre_x=centre_x, right_x=right_x, bottom_y=bottom_y, centre_y=centre_y, top_y=top_y)
  draw_given_contour(ax=ax, is_patch=True, contour=contour, diamond_x=diamond_best_guess[0], diamond_y=diamond_best_guess[1], stretch_x=1.0, stretch_y=1.0, turn=0, **kwargs)
  
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