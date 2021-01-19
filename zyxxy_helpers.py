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
from zyxxy_settings import set_outline_kwarg_default
from zyxxy_MY_SETTINGS import my_default_diamond_size, my_default_diamond_colour, my_colour_palette
from zyxxy_coordinates import build_polygon
from zyxxy_move import stretch_something, shift_something, rotate_something

_all_shapes_per_zorder = {}

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

def set_diamond_style(show=None, size=None, colour=None, zorder=None):
  global _default_diamond_arguments
  if show is not None:
    _default_diamond_arguments['show'] = show
  if size is not None:
    _default_diamond_arguments['size'] = size
  if colour is not None:
    _default_diamond_arguments['colour'] = colour
  if zorder is not None:
    _default_diamond_arguments['zorder'] = zorder

def __draw_diamond(ax, diamond_location):
  if _default_diamond_arguments['show'] and (diamond_location is not None):
    diamond_r = get_width(ax=ax) * _default_diamond_arguments['size'] / 1000
    contour = build_polygon(centre_x=diamond_location[0], 
                            centre_y=diamond_location[1], 
                            vertices_qty=4, radius=diamond_r)
    _fill_in_outline(ax=ax, contour=contour, stretch_x=1, stretch_y=1, colour=_default_diamond_arguments['colour'], diamond=None, turn=None, alpha=1.0, zorder=_default_diamond_arguments['zorder'])

##################################################################
## COLOUR HELPERS                                               ## 
##################################################################

# Find colour that should be used. 
# Assume that it's a name of a standard colour.
# Attention, names are case-sensitive
def find_colour_code(colour_name):
  if colour_name in my_colour_palette:
    return my_colour_palette[colour_name] 
  if colour_name in mcolors.CSS4_COLORS:
    return colour_name # matplotlib knows how to handle it

  # If we are here, the colour name has not been recognised
  # Assuming that it is a colour code.
  return colour_name

##################################################################
## SHAPES AND LINES HELPERS                                     ## 
##################################################################

# this function fills in the outline given by all_x and all_y
# and rotates it if needed.
# turn is like the turn of the hours hand of the clock
# i.e. for turn = 3 (3 o'clock) the line with be drawn to the left of the diamond point
# turn = 6 (6 o'clock) the line with be drawn to the bottom of the diamond point, and so on.
# you can use any number, it will be transformed to degrees using 30*turn formula, and used accordingly.
def _fill_in_outline(ax, contour, colour, diamond, turn, stretch_x, stretch_y, zorder, alpha, outline_colour=None, outline_linewidth=None, outline_joinstyle=None, outline_zorder=None, clip_outline=None):  
  contour = stretch_something(something=contour, diamond=diamond, stretch_x=stretch_x, stretch_y=stretch_y)
  contour = rotate_something(something=contour, diamond=diamond, turn=turn)
  __draw_diamond(ax=ax, diamond_location=diamond)   
  
  outline_style = {'colour' : outline_colour,
             'linewidth' : outline_linewidth,
             'joinstyle' : outline_joinstyle,
             'zorder' : outline_zorder}

  _draw_broken_line(ax=ax, contour=np.append(contour, contour[0:2], axis=0), diamond=None, **set_outline_kwarg_default(outline_style))
  
  if colour is not None:
    colour_code = find_colour_code(colour_name = colour)
  else:
    colour_code = 'none'
  patch = plt.Polygon(contour, fc = colour_code, 
                               ec = 'none',
                               zorder = zorder,
                               alpha = alpha)
  ax.add_patch(patch)
  add_to_layer_record(zorder=zorder, what_to_add=patch)

  if clip_outline is not None:
    if type(clip_outline) is plt.Polygon:
      clip_contour = clip_outline.get_xy()
    else:
      clip_contour = clip_outline
    clip_patch = plt.Polygon(clip_contour, 
                               fc = 'none', 
                               ec = 'none',
                               zorder = zorder)
    ax.add_patch(clip_patch)
    patch.set_clip_path(clip_patch)
    add_to_layer_record(zorder=zorder, what_to_add=clip_patch)
  
  return patch

def add_to_layer_record(zorder, what_to_add):
  if zorder not in _all_shapes_per_zorder:
    _all_shapes_per_zorder[zorder] = [what_to_add]
  else:
    _all_shapes_per_zorder[zorder] += [what_to_add]

def get_all_shapes_in_layers(*args):
  result = []
  for zorder in args:
    result += _all_shapes_per_zorder[zorder]
  return result

def shift_layer(layer_nb, shift):
  if layer_nb not in _all_shapes_per_zorder:
    return []
  for something in _all_shapes_per_zorder[layer_nb]:
    shift_something(something=something, shift=shift)
  return _all_shapes_per_zorder[layer_nb]

def rotate_layer(layer_nb, turn, diamond):
  if layer_nb not in _all_shapes_per_zorder:
    return []
  for something in _all_shapes_per_zorder[layer_nb]:
    rotate_something(something=something, turn=turn, diamond=diamond)
  return _all_shapes_per_zorder[layer_nb]

def stretch_layer(layer_nb, diamond, stretch_x, stretch_y):
  if layer_nb not in _all_shapes_per_zorder:
    return []
  for something in _all_shapes_per_zorder[layer_nb]:
    stretch_something(something=something, diamond=diamond, stretch_x=stretch_x, stretch_y=stretch_y)
  return _all_shapes_per_zorder[layer_nb]
  
def _draw_broken_line(ax, contour, colour, linewidth, joinstyle, zorder, diamond=None, turn=None):
  if (contour is None) or (linewidth is None) or (colour is None) or (zorder is None) or (joinstyle is None) or (linewidth == 0):
    return contour
  
  contour = rotate_something(something=contour, diamond=diamond, turn=turn)

  colour_code = find_colour_code(colour_name = colour)
  line, = ax.plot([c[0] for c in contour], [c[1] for c in contour],     lw=linewidth, color=colour_code, zorder=zorder, solid_joinstyle=joinstyle)

  add_to_layer_record(zorder=zorder, what_to_add=line)

  __draw_diamond(ax=ax, diamond_location=diamond)
  return contour