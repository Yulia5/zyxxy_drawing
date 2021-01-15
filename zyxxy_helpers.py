#####################################################
## don't change this file, please                  ##
#####################################################

import math
import random
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from zyxxy_settings import set_outline_kwarg_default

##################################################################
## MATHS HELPERS                                                ## 
##################################################################
def random_number(max, min=0.):
  return random.uniform(0, 1) * (max - min) + min

# both limits, min and max, are included in possible outcomes
def random_integer_number(max, min=0.):
  return random.randint(min, max)

def random_element(list_to_choose_from):
  return random.choice(list_to_choose_from)

##################################################################
## DIAMOND HELPERS                                              ## 
##################################################################
_default_diamond_arguments = {
  'show' : False,
  'zorder' : 1000, 
  'size' : 15,
  'colour' : 'green'
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
    diamond_r = (_default_diamond_arguments['size'] / 1000) * (ax.get_xlim()[1] - ax.get_xlim()[0])
    all_diamond_x = [diamond_location[0], diamond_location[0]+diamond_r, diamond_location[0], diamond_location[0]-diamond_r, diamond_location[0]]
    all_diamond_y = [diamond_location[1]+diamond_r, diamond_location[1], diamond_location[1]-diamond_r, diamond_location[1], diamond_location[1]+diamond_r]
    fill_in_outline(ax=ax, all_x=all_diamond_x, all_y=all_diamond_y, colour=_default_diamond_arguments['colour'], diamond=None, turn=None, alpha=1.0, zorder=_default_diamond_arguments['zorder'])

##################################################################
## COLOUR HELPERS                                               ## 
##################################################################

# Find colour that should be used. 
# Assume that it's a name of a standard colour.
# Attention, names are case-sensitive
def find_colour_code(colour_name):
  if colour_name in mcolors.CSS4_COLORS:
    return colour_name
  # if we are here, the colour name has not been recognised
  all_colour_names = mcolors.CSS4_COLORS.keys().sort()
  raise Exception("Colour name is not recognised. Colour names are case-sensitive. Colour name should be one of the following names: " + ', '.join(all_colour_names))

##################################################################
## SHAPES AND LINES HELPERS                                     ## 
##################################################################

def vertices_qty_in_circle():
  return 60

# auxiliary functions to define sin and cos of angles measured in hours
# we need "12-" because matlibplot's angle turns counterclockwise
def sin_hours(turn):
  return math.sin(math.radians((12 - turn) * 30))
def cos_hours(turn):
  return math.cos(math.radians((12 - turn) * 30))

def rotate_point(point, diamond, turn):
  if diamond is None:
    return point
  return [diamond[0] + (point[0] - diamond[0]) * cos_hours(turn) - (point[1] - diamond[1]) * sin_hours(turn),
          diamond[1] + (point[0] - diamond[0]) * sin_hours(turn) + (point[1] - diamond[1]) * cos_hours(turn)] 

# this function fills in the outline given by all_x and all_y
# and rotates it if needed.
# turn is like the turn of the hours hand of the clock
# i.e. for turn = 3 (3 o'clock) the line with be drawn to the left of the diamond point
# turn = 6 (6 o'clock) the line with be drawn to the bottom of the diamond point, and so on.
# you can use any number, it will be transformed to degrees using 30*turn formula, and used accordingly.
def fill_in_outline(ax, all_x, all_y, colour, diamond, turn, zorder, alpha, outline_colour=None, outline_linewidth=None, outline_joinstyle=None, outline_zorder=None, clip_outline=None):  
  contour = [[x, y] for x, y in list(zip(all_x, all_y))]
  if diamond is not None:
    contour = [rotate_point(point=point, diamond=diamond, turn=turn) for point in contour] 
    __draw_diamond(ax=ax, diamond_location=diamond)   
  
  outline_style = {'colour' : outline_colour,
             'linewidth' : outline_linewidth,
             'joinstyle' : outline_joinstyle,
             'zorder' : outline_zorder}

  _draw_broken_line(ax=ax, contour=contour+contour[0:2], diamond=None, **set_outline_kwarg_default(outline_style))
  
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
    if colour is None:
      raise Exception('none')
    return contour
  if (diamond is not None) and (turn is not None):
    contour = [rotate_point(point=point, diamond=diamond, turn=turn) for point in contour] 

  colour_code = find_colour_code(colour_name = colour)
  ax.plot([c[0] for c in contour], [c[1] for c in contour],     lw=linewidth, color=colour_code, zorder=zorder, solid_joinstyle=joinstyle)

  __draw_diamond(ax=ax, diamond_location=diamond)
  return contour