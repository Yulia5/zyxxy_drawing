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
from zyxxy_utils import sin_hours, cos_hours, asin_hours, acos_hours, atan_hours, is_the_same_point, my_default_vertices_qty_in_circle, full_turn_angle

from scipy.optimize import fsolve
from math import sqrt, ceil, floor

########################################################################

angles_std = np.linspace(start=0, stop=full_turn_angle, num=my_default_vertices_qty_in_circle)

sin_cos_std = [[sin_hours(a), cos_hours(a)] for a in angles_std]

#####################################################
## contours manipulation                           ##
#####################################################
def conc_1_or_2_dim(a, b):
  if a.ndim != b.ndim:
    raise Exception("Dimension number mismatch", a.ndim, "!=", b.ndim)
  if a.ndim == 1:
    return np.hstack((a, b))
  else:
    return np.vstack((a, b))

#####################################################
def link_contours(*arg):
  result = np.empty((2, 0))
  for _a in arg:
    if isinstance(_a, np.ndarray):
      a = _a
    else:
      a = np.array(_a, np.float64)
    if (a.size == 0):
      continue
    if (result.size == 0):
      result = a
      continue
    if is_the_same_point(p1=result[-1], p2=a[0]):
      result = conc_1_or_2_dim(result[:-1], a)
    else:
      result = conc_1_or_2_dim(result, a)
  return result

#####################################################
def add_a_left_mirror(contour, mirror_x=0):
  reverse_contour = np.copy(contour[::-1, :])
  reverse_contour[:, 0] = 2 * mirror_x - reverse_contour[:, 0]
  result = link_contours(reverse_contour, contour)
  return result

#####################################################
#####################################################
# a rectangle ####################################################
def build_a_rectangle(width, height, left_x=None, centre_x=None, right_x=None, bottom_y=None, centre_y=None, top_y=None):

  # checking that we the right number of inputs
  how_many_are_defined = {'x' : (left_x is not None) + (centre_x is not None) + (right_x is not None), 'y' :  (bottom_y is not None) + (centre_y is not None) + (top_y is not None)}
  errorMsg = ['One and only one ' + key + ' coordinate should be defined, but ' + str(value) + ' are defined' for key, value in how_many_are_defined.items() if value != 1]
  if len(errorMsg) != 0:
    raise Exception('; '.join(errorMsg))

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
 
  contour_array = np.array([[left_x, bottom_y], [right_x,bottom_y], [right_x, top_y], [left_x, top_y]])

  return diamond_best_guess, contour_array

# a line ######################################################
def build_a_line():
  contour = np.array([[0, 0], [0, 1]])
  return contour

# a square ######################################################
def build_a_square():
  contour = np.array([[0, 0], [0, 1], [1, 1], [1, 0]])
  return contour

# a triangle ######################################################
def build_a_triangle():
  contour_array = np.array([[-1/2, 1], [0, 0], [1/2, 1]]) 
  return contour_array

# an arc ##########################################################
def _build_an_arc(angle_start, angle_end):
  if angle_start > angle_end:
    angle_start, angle_end = angle_end, angle_start

  angle_start_normalized = angle_start / full_turn_angle
  angle_end_normalized   = angle_end   / full_turn_angle

  turn_nb_start = angle_start_normalized // 1
  turn_nb_end   =   angle_end_normalized // 1

  residual_start = ceil((angle_start_normalized % 1) * my_default_vertices_qty_in_circle)
  residual_end = floor((angle_end_normalized % 1)  * my_default_vertices_qty_in_circle)

  if is_the_same_point(turn_nb_start, turn_nb_end):
    contour = sin_cos_std[residual_start : (residual_end+1)]
  else:
    contour = sin_cos_std[residual_start : ] + sin_cos_std * int(turn_nb_end - turn_nb_start-1) + sin_cos_std[ : (residual_end+1)]

  contour = np.array(contour, np.float64)

  c_len = contour.size
  contour = link_contours([[sin_hours(angle_start), cos_hours(angle_start)]], contour)
  if c_len == contour.size:
    added_start = None
  else:
    added_start = residual_start - (angle_start_normalized % 1) * my_default_vertices_qty_in_circle

  c_len = contour.size 
  contour = link_contours(contour, [[sin_hours(angle_end), cos_hours(angle_end)]])
  if c_len == contour.size:
    added_end = None
  else:
    added_end = -residual_end + (angle_end_normalized % 1) * my_default_vertices_qty_in_circle

  return contour, added_start, added_end

def build_an_arc(angle_start, angle_end):
  contour, _, _ = _build_an_arc(angle_start=angle_start, angle_end=angle_end)
  return contour

# an arc with different speeds ####################################
def build_an_arc_multispeed(angle_start, angle_end, speed_x=1.0, speed_y=1.0):
  if angle_start > angle_end:
    angle_start, angle_end = angle_end, angle_start

  step = full_turn_angle / (max(abs(speed_x), abs(speed_y)) * my_default_vertices_qty_in_circle)
  angles = link_contours(np.arange(angle_start, angle_end, step), [angle_end])

  contour = np.array([[sin_hours(a * speed_x), cos_hours(a * speed_y)] for a in angles])
  return contour

# a circle ########################################################
def build_a_circle():
  contour = build_an_arc(angle_start=0, angle_end=12)
  return contour 

# an ellipse ######################################################
def build_an_ellipse(radius_x, radius_y):
  contour = build_a_circle()
  contour[:, 0] *= radius_x
  contour[:, 1] *= radius_y
  return contour

# a pig tail ######################################################
def build_a_coil(angle_start, nb_turns, speed_x, speed_out):
  contour, added_start, added_end = _build_an_arc(angle_start=angle_start, angle_end=angle_start+nb_turns*full_turn_angle)

  len_contour_m1 = contour.shape[0] - 1

  mult_xy = [1] + [speed_out**(1./my_default_vertices_qty_in_circle)] * len_contour_m1
  add_x = [0] + [speed_x/my_default_vertices_qty_in_circle] * len_contour_m1
  if added_start is not None:
    mult_xy[1] = mult_xy[1] ** added_start
    add_x[1] *= added_start
  if added_end is not None:
    mult_xy[-1] = mult_xy[-1] ** added_end
    add_x[-1] *= added_end
  
  add_x = np.cumsum(add_x)
  mult_xy = np.cumprod(mult_xy)

  for l in range(contour.shape[0]):
    contour[l, 0] *= mult_xy[l]
    contour[l, 1] *= mult_xy[l]
    contour[l, 0] += add_x[l]

  return contour

# a smile ###########################################################
# dip is middle_y_to_half_width
def build_a_smile(dip): # assume that the width = 2
  # if mid_point is almost at the same hor line, assume it's a straight line
  if is_the_same_point(dip, 0.0): 
    result = np.empty([2, 2])
  else:
    radius = abs((1 + dip**2) / (2 * dip))
    angle = (asin_hours(sin_value = 1 / radius))
    # reusing build_arc
    result = build_an_arc(angle_start=-angle, 
                          angle_end=+angle) * radius - [0, radius-abs(dip)]
    if dip < 0:
      result[:, 1] *= -1
  # adjusting start and end points to make sure they match the inputs exactly
  result[0] = [-1, 0]
  result[-1] = [1, 0]
  # all done!
  return result

# an eye ########################################################
def build_an_eye(dip_1, dip_2): 
  smile1 = build_a_smile(dip=dip_1)
  smile2 = build_a_smile(dip=dip_2)
  result = link_contours(smile1, smile2[::-1])
  return result

# a sector ######################################################
def build_a_sector(angle_start, angle_end, radii_ratio=0.):
  contour = build_an_arc(angle_start=angle_start, angle_end=angle_end)

  if is_the_same_point(radii_ratio, 0.0):
    # special case - just add the mid-point
    result = link_contours(contour, [[0, 0]])
  else:
    # add the arc
    inner_arc = np.ndarray.copy(contour) * radii_ratio
    result = link_contours(contour, inner_arc[::-1])
  return result

# a drop #########################################################
def build_an_elliptic_drop():
  contour = build_an_arc_multispeed(angle_start=3, angle_end=9, speed_x=2.0, speed_y=1.0)
  return contour

# a heart (or an ice-cream) ########################################
# the arcs are the circle arcs, no compression #####################
# 3 for the heart, 0 for an ice-cream :) ###########################
def build_a_heart(angle_top_middle, tip_addon):
  radius = 1 / (1 + sin_hours(angle_top_middle)) # this ensures that the width = 2

  a = sin_hours(angle_top_middle) * radius
  b = (1 + tip_addon) * radius
  c = sqrt(a*a + b*b)

  angle_bottom = atan_hours(a/b) + asin_hours(radius/c) 

  # adding the right half-circle
  right_arc = build_an_arc(angle_start=12-angle_top_middle, angle_end=15+angle_bottom) * radius
  # moving the mid-point's x to 0
  right_arc -= [right_arc[0, 0], 0]
  # adding the tip
  right_side = link_contours(right_arc, [[0, -radius * (1 + tip_addon)]])
  # moving up so that the tip is in [0, 0]
  right_side += [0, +radius * (1 + tip_addon)]
  # adding up a left side
  contour = add_a_left_mirror(right_side)

  return contour

# an egg shape #######################################################
def build_an_egg(power, tip_addon):

  h = lambda cos_alpha: cos_alpha * (1 - 1 / power) + 1 / (power * cos_alpha) - (1 + tip_addon)
  cos_alpha_solution = fsolve(h , x0=.5)[0]

  if cos_alpha_solution > 1.:
    cos_alpha_solution = 1 / (cos_alpha_solution * (power-1))

  if is_the_same_point(1., cos_alpha_solution):
    a = 0
  else:
    a = (1 + tip_addon - cos_alpha_solution) / ((1 - cos_alpha_solution*cos_alpha_solution) ** (power/2))

  alpha_solution = acos_hours(cos_alpha_solution)
  _arc = build_an_arc(angle_start=0, angle_end=6-alpha_solution)

  pf_points_qty = int(my_default_vertices_qty_in_circle/4)

  power_func_x = sqrt(1 - cos_alpha_solution*cos_alpha_solution) * (1. - np.array([n/pf_points_qty for n in range(pf_points_qty+1)]))
  power_func_2D = [[x, a * (x**power) - (1 + tip_addon)] for x in power_func_x]

  right_half_contour = link_contours(_arc, power_func_2D) 

  # adding the left half and
  # moving the egg so that its centre were where needed
  contour = add_a_left_mirror(right_half_contour)
  return contour

# a regular polygon ###################################################
def build_a_regular_polygon(vertices_qty): 
  angles = [(i * 12 / vertices_qty) for i in range(vertices_qty)]
  contour = np.array([[sin_hours(a), cos_hours(a)] for a in angles])
  return contour

# a star #############################################################
def build_a_star(ends_qty, radii_ratio): 
  angles = [i * 12/(2*ends_qty) for i in range(2*ends_qty)]
  radii = [radii_ratio * (i%2 == 0) + 1 * (i%2 == 1) for i in range(2*ends_qty)]

  contour = np.array([[radii[i] * sin_hours(angles[i]), 
                       radii[i] * cos_hours(angles[i])] for i in range(2*ends_qty)])

  return  contour

## a rhombus ###########################################################
def build_a_rhombus():
  contour = build_a_regular_polygon(vertices_qty=4)
  return contour