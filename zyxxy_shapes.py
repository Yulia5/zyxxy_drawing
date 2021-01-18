#####################################################
## don't change this file, please                  ##
#####################################################

from zyxxy_helpers import _fill_in_outline
from zyxxy_coordinates import vertices_qty_in_circle, link_contours, add_mirror
from zyxxy_utils import acos_hours, tan_hours
from zyxxy_settings import set_fill_in_outline_kwarg_defaults
from zyxxy_coordinates import build_smile, build_star, build_polygon, build_arc, build_ellipse_different_speeds
import numpy as np 
import math 

# this function draws a polygon
def draw_a_polygon(ax, contour, diamond=None, **kwargs):

  contour2 = _fill_in_outline(ax=ax, contour=contour, diamond=diamond, **set_fill_in_outline_kwarg_defaults(kwargs))

  return contour2

# this function draws a rectangle
# diamond point is at the bottom left vertice
def draw_a_rectangle(ax, width, height, left_x=None, centre_x=None, right_x=None, bottom_y=None, centre_y=None, top_y=None, diamond=None, **kwargs):

  # checking that we the right number of inputs
  how_many_are_defined = {'x' : (left_x is not None) + (centre_x is not None) + (right_x is not None), 'y' :  (bottom_y is not None) + (centre_y is not None) + (top_y is not None)}
  errorMsg = '; '.join('One and only one ' + key + ' coordinate should be defined, but ' + str(value) + ' are defined' for key, value in how_many_are_defined.items() if value != 1)
  if errorMsg != '':
    raise Exception(errorMsg)

  diamond_best_guess = [None, None]
  # defining coordinates that are undefined - x
  if left_x is not None:
    centre_x = left_x + width / 2
    right_x = left_x + width
    diamond_best_guess[0] = left_x
  else:
    if centre_x is not None:
      left_x = centre_x - width / 2
      right_x = centre_x + width / 2
      diamond_best_guess[0] = centre_x
    elif right_x is not None:
      left_x = right_x - width
      centre_x = right_x - width / 2  
      diamond_best_guess[0] = right_x

  # defining coordinates that are undefined - y
  if bottom_y is not None:
    centre_y = bottom_y + height / 2
    top_y = bottom_y + height
    diamond_best_guess[1] = bottom_y
  else:
    if centre_y is not None:
      bottom_y = centre_y - height / 2
      top_y = centre_y + height / 2
      diamond_best_guess[1] = centre_y
    elif top_y is not None:
      bottom_y = top_y - height
      centre_y = top_y - height / 2 
      diamond_best_guess[1] = top_y

  # ... and the diamond          
  if diamond is None:
    diamond = diamond_best_guess
  kwargs['diamond'] = diamond
 
  contour_array = np.array([[left_x, bottom_y], [right_x,bottom_y], [right_x, top_y], [left_x, top_y]])
  contour = _fill_in_outline(ax=ax, contour=contour_array, **set_fill_in_outline_kwarg_defaults(kwargs))

  return contour

# draw a square, default side = 1, the simplest polygon!
def draw_a_square(ax, left_x, bottom_y, side=1, **kwargs):
  contour = draw_a_rectangle(ax=ax, left_x=left_x, bottom_y=bottom_y, height=side, width=side, **kwargs)

  return contour

# this function draws a symmetrical (isosceles) triangle
# diamond point is at the tip point
# if not rotated, the tip is pointing down
def draw_a_triangle(ax, tip_x, tip_y, height, width, **kwargs):
  contour_array = np.array([[tip_x-width/2, tip_y+height], [tip_x, tip_y], [tip_x+width/2, tip_y+height]])
  contour = _fill_in_outline(ax=ax, contour=contour_array, diamond=(tip_x, tip_y), **set_fill_in_outline_kwarg_defaults(kwargs))

  return contour

# this function that draws a star
# its diamond point is in the centre
def draw_star(ax, centre_x, centre_y, radius1, radius2, ends_qty, diamond=None, **kwargs): 

  contour_init = build_star(centre_x=centre_x, centre_y=centre_y, radius1=radius1, radius2=radius2, ends_qty=ends_qty)

  if diamond is None:
    diamond=(centre_x, centre_y)

  contour = _fill_in_outline(ax=ax, contour = contour_init, diamond=diamond, **set_fill_in_outline_kwarg_defaults(kwargs))

  return contour

# a polygon is a special case of a star (when radiuses are equal), so we will reuse that function
# its diamond point is in the centre (same as the star)
def draw_a_regular_polygon(ax, centre_x, centre_y, radius, 
vertices_qty, diamond=None, **kwargs):
  contour_init = build_polygon(centre_x=centre_x, centre_y=centre_y, radius=radius, vertices_qty=vertices_qty) 

  if diamond is None:
    diamond=(centre_x, centre_y)

  contour = _fill_in_outline(ax=ax, contour = contour_init, diamond=diamond, **set_fill_in_outline_kwarg_defaults(kwargs))

  return contour

# a polygon with 60 vertices looks very similar to a circle
# possible to increase the number of vertices if needed
# its diamond point is in the centre (same as the star)
def draw_an_ellipse(ax, centre_x, centre_y, radius_x, radius_y, diamond=None, **kwargs):
  kwargs['stretch_x'] = radius_x
  kwargs['stretch_y'] = radius_y

  contour = draw_a_regular_polygon(ax=ax, centre_x=centre_x, centre_y=centre_y, radius=1, vertices_qty=vertices_qty_in_circle(), diamond=diamond, **kwargs)

  return contour

# a circle is a special case of an ellipse
def draw_a_circle(ax, centre_x, centre_y, radius, diamond=None, **kwargs):
  contour = draw_an_ellipse(ax=ax, centre_x=centre_x, centre_y=centre_y, radius_x=radius, radius_y=radius, diamond=diamond, **kwargs)

  return contour 

# this function that draws a star
# its diamond point is in the centre
def draw_a_double_smile(ax, centre_x, width, corners_y, mid1_y, mid2_y, **kwargs): 
  smile1 = build_smile(centre_x=centre_x, bottom_y=mid1_y, top_y=corners_y, width=width)
  smile2 = build_smile(centre_x=centre_x, bottom_y=mid2_y, top_y=corners_y, width=width)
  contour_init = smile1[:-1] + smile2[::-1]

  contour = _fill_in_outline(ax=ax, contour=contour_init, diamond=(centre_x, corners_y), **set_fill_in_outline_kwarg_defaults(kwargs))

  return contour

def draw_a_rhombus(ax, centre_x, centre_y, width, height, diamond=None, **kwargs):
  contour = draw_star(ax=ax, centre_x=centre_x, centre_y=centre_y, radius1=height/2, radius2=width/2, ends_qty=2, diamond=diamond, **kwargs)

  return contour

# draw a segment of an ellipse
def draw_a_sector(ax, centre_x, centre_y, radius, 
angle_start, angle_end, connect_centre=True, diamond=None, **kwargs):
  

  contour_init = build_arc(centre_x=centre_x, centre_y=centre_y, radius_x=radius, radius_y=radius, angle_start=angle_start, angle_end=angle_end)

  if connect_centre:
    contour_init = np.append(contour_init, [[centre_x, centre_y]], axis=0)

  if diamond is None:
    diamond=(centre_x, centre_y)

  contour = _fill_in_outline(ax=ax, contour=contour_init, diamond=diamond, **set_fill_in_outline_kwarg_defaults(kwargs))

  return contour

# drawing a drop. 
def draw_a_drop(ax, centre_x, centre_y, radius, diamond=None, **kwargs):
  contour_init = build_ellipse_different_speeds(centre_x=centre_x, centre_y=centre_y, radius_x=radius, radius_y=radius, angle_start=3, angle_end=9, speed_x=2.0, speed_y=1.0)

  if diamond is None:
    diamond=(centre_x, centre_y)

  contour = _fill_in_outline(ax=ax, contour=contour_init, diamond=diamond, **set_fill_in_outline_kwarg_defaults(kwargs))

  return contour

# drawing a heart. Might need to change parametrization
def draw_a_heart(ax, centre_x, centre_y, radius, angle_middle=0, angle_tip=3, diamond=None, **kwargs):
  
  # adding the right half-circle
  right_contour = build_arc(centre_x=0, centre_y=0, radius_x=radius, radius_y=radius, angle_start=9+angle_middle/2, angle_end=3+angle_tip/2)

  # moving the mid-point to 0
  right_contour -= [right_contour[0, 0], 0]

  # adding the tip
  tip_y = right_contour[-1, 1] + right_contour[-1, 0] / abs(tan_hours(angle_tip/2))

  right_contour = link_contours(right_contour, [[0, tip_y]])

  # connecting left and right arcs. Keeping y coordinate of the points where arc connect for future use.
  contour_init = add_mirror(right_contour)
  
  # moving the heart so that its centre were in the tip point
  contour_init += [centre_x, centre_y - tip_y]

  if diamond is None:
    diamond=(centre_x, centre_y)

  contour = _fill_in_outline(ax=ax, contour=contour_init, diamond=diamond, **set_fill_in_outline_kwarg_defaults(kwargs))

  return contour


# drawing an egg shape. Might need to change parametrization
def draw_an_egg(ax, centre_x, centre_y, width, height,where_it_bends, power, diamond=None, **kwargs):
  wibr = where_it_bends/(1 - where_it_bends)

  cos_alpha = 2 / (power * wibr + math.sqrt((power * wibr)**2 - 4 * (power - 1)))

  alpha = acos_hours(cos_value=cos_alpha)

  a = height*where_it_bends - height *(1-where_it_bends)*cos_alpha/((0.5 * width * math.sqrt(1 - cos_alpha**2)) ** power)

  arc_outline = build_arc(centre_x=0, centre_y=height*where_it_bends, radius_x=0.5*width, radius_y=height*(1-where_it_bends), angle_start=0, angle_end=3+alpha)

  power_func_x = np.linspace(start=0, stop=0.5*width, num=vertices_qty_in_circle()/2)

  power_func_outline = a * power_func_x**power

  right_half_contour = link_contours(arc_outline, power_func_outline[::-1, :]) 

  # adding the left half and
  # moving the egg so that its centre were where needed
  contour_init = add_mirror(right_half_contour)
  contour_init += [centre_x, centre_y]