#####################################################
## don't change this file, please                  ##
#####################################################

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from zyxxy_utils import cos_hours, sin_hours
from zyxxy_settings import set_outline_kwarg_default
from zyxxy_MY_SETTINGS import my_default_diamond_size, my_default_diamond_colour, my_colour_palette
from zyxxy_coordinates import build_polygon

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
    fill_in_outline(ax=ax, contour=contour, stretch_x=1, stretch_y=1, colour=_default_diamond_arguments['colour'], diamond=None, turn=None, alpha=1.0, zorder=_default_diamond_arguments['zorder'])

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

def rotate_point(point, diamond, turn):
  if diamond is None:
    return point
  return [diamond[0] + (point[0] - diamond[0]) * cos_hours(turn) - (point[1] - diamond[1]) * sin_hours(turn),
          diamond[1] + (point[0] - diamond[0]) * sin_hours(turn) + (point[1] - diamond[1]) * cos_hours(turn)] 

def stretch_contour(contour, diamond, stretch_x, stretch_y):
  if diamond is None:
    return contour
  if stretch_x is not None:
    contour[:, 0] = diamond[0] + (contour[:, 0] - diamond[0]) * stretch_x 
  if stretch_y is not None:
    contour[:, 1] = diamond[1] + (contour[:, 1] - diamond[1]) * stretch_y
  return contour

# this function fills in the outline given by all_x and all_y
# and rotates it if needed.
# turn is like the turn of the hours hand of the clock
# i.e. for turn = 3 (3 o'clock) the line with be drawn to the left of the diamond point
# turn = 6 (6 o'clock) the line with be drawn to the bottom of the diamond point, and so on.
# you can use any number, it will be transformed to degrees using 30*turn formula, and used accordingly.
def fill_in_outline(ax, contour, colour, diamond, turn, stretch_x, stretch_y, zorder, alpha, outline_colour=None, outline_linewidth=None, outline_joinstyle=None, outline_zorder=None, clip_outline=None):  
  contour = stretch_contour(contour=contour, diamond=diamond, stretch_x=stretch_x, stretch_y=stretch_y)
  if diamond is not None:
    contour = [rotate_point(point=point, diamond=diamond, turn=turn) for point in contour] 
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
                               ec = colour_code,
                               zorder = zorder,
                               alpha = alpha)
  ax.add_patch(patch)

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
  
  return patch

def _draw_broken_line(ax, contour, colour, linewidth, joinstyle, zorder, diamond=None, turn=None):
  if (contour is None) or (linewidth is None) or (colour is None) or (zorder is None) or (joinstyle is None) or (linewidth == 0):
    return contour
  if (diamond is not None) and (turn is not None):
    contour = [rotate_point(point=point, diamond=diamond, turn=turn) for point in contour] 

  colour_code = find_colour_code(colour_name = colour)
  ax.plot([c[0] for c in contour], [c[1] for c in contour],     lw=linewidth, color=colour_code, zorder=zorder, solid_joinstyle=joinstyle)

  __draw_diamond(ax=ax, diamond_location=diamond)
  return contour