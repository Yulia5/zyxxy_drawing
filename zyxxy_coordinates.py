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

zyxxy_line_shapes = ['a_segment', 'a_smile', 'a_coil', 'an_arc', 'a_zigzag', 'a_wave']

def get_type_given_shapename(shapename):
  if shapename in zyxxy_line_shapes:
    return 'line'
  elif shapename in shape_names_params_dicts_definition.keys():
    return 'patch'
  else:
    raise Exception(shapename, " is not a recognized shapename")

shape_names_params_dicts_definition = {
                            'a_segment' : {'length': 'half_min_size'},               
                            'a_triangle': {'width' : 'half_min_size', 'height' : 'half_min_size'}, 
                            'a_square': {'side' : 'half_min_size'}, 
                            'a_rectangle': {'width' : ['half_min_size', 4], 'height' : ['half_min_size', 2]}, 
                            'a_rhombus' : {'width' : 'half_min_size', 'height' : 'half_min_size'},
                            'a_circle': {'radius' : 'half_min_size'},
                            'an_ellipse': {'width' : ['half_min_size', 4], 'height' : ['half_min_size', 2]}, 
                            'an_arc' : {'angle_start' : ['turn', full_turn_angle/4], 'angle_end' : ['turn', full_turn_angle/2], 'radius' : 'half_min_size'},
                            'an_elliptic_drop': {'width' : 'half_min_size', 'height' : 'half_min_size_34'},
                            'a_smile': {'width' : 'half_min_size', 'depth' : ['plus_minus_half_min_size', 1]},
                            'a_star': {'ends_qty' : 'vertices', 'radius_1' : 'half_min_size_34', 'radius_2' : ['half_min_size', 2]},
                            'a_regular_polygon': {'radius' : 'half_min_size', 'vertices_qty' : 'vertices'},
                            'an_eye': {'width' : ['half_min_size', 4], 'depth_1' : ['plus_minus_half_min_size', -1], 'depth_2' : ['plus_minus_half_min_size', 1]},
                            'a_heart': {'angle_top_middle' : ['quarter_turn', 3], 'tip_addon' : 'stretch'},
                            'an_egg' : {'power' : ['vertices', 3], 'height_widest_point': ['half_height', 3], 'width' : ['half_width', 4], 'height' : ['half_height', 5]},
                            'a_sector': {'angle_start' : 'turn', 'angle_end' : ['double_turn', 3], 'radius' : 'half_min_size', 'radius_2' : 'half_min_size_34'},
                            'a_zigzag' : {'width': 'half_min_size', 'height': 'half_min_size', 'angle_start': 'turn', 'nb_segments': 'vertices'},
                            'a_wave' : {'width': 'half_min_size', 'height': 'half_min_size', 'angle_start': 'turn', 'nb_waves': 'vertices'},
                            'a_coil' : {'angle_start' : 'turn', 'nb_turns' : ['stretch', 3], 'speed_x' : 'stretch', 'speed_out' : ['stretch', 1.2]},
                            'an_arc_multispeed': {'angle_start' : ['turn', 0], 'angle_end' : ['double_turn', 24], 'speed_x' : ['stretch', 3], 'width' : ['half_width', 2], 'height' : 'half_height'}}

########################################################################

sin_cos_std = [[sin_hours(a/my_default_vertices_qty_in_circle*full_turn_angle), cos_hours(a/my_default_vertices_qty_in_circle*full_turn_angle)] for a in range(my_default_vertices_qty_in_circle)]

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
def build_a_rectangle_and_its_diamond(width, height, left=None, centre_x=None, right=None, bottom=None, centre_y=None, top=None):

  # checking that we the right number of inputs
  how_many_are_defined = {'x' : (left is not None) + (centre_x is not None) + (right is not None), 'y' :  (bottom is not None) + (centre_y is not None) + (top is not None)}
  errorMsg = ['One and only one ' + key + ' coordinate should be defined, but ' + str(value) + ' are defined' for key, value in how_many_are_defined.items() if value > 1]
  if len(errorMsg) != 0:
    raise Exception('; '.join(errorMsg))

  presumed_diamond = [None, None]

  # defining coordinates that are undefined - x
  if left is not None:
    centre_x = left + width / 2
    right = left + width
    presumed_diamond[0] = left
  elif centre_x is not None:
    left = centre_x - width / 2
    right = centre_x + width / 2
    presumed_diamond[0] = centre_x
  elif right is not None:
    left = right - width
    centre_x = right - width / 2
    presumed_diamond[0] = right 
  else:
    left, right = - width / 2, width / 2
    presumed_diamond[0] = 0 

  # defining coordinates that are undefined - y
  if bottom is not None:
    centre_y = bottom + height / 2
    top = bottom + height
    presumed_diamond[1] = bottom
  elif centre_y is not None:
    bottom = centre_y - height / 2
    top = centre_y + height / 2
    presumed_diamond[1] = centre_y
  elif top is not None:
    bottom = top - height
    centre_y = top - height / 2 
    presumed_diamond[1] = top
  else:
    bottom, top = - height / 2, height / 2
    presumed_diamond[1] = 0
 
  contour_array = np.array([[left, bottom], [right, bottom], [right, top], [left, top]]) - presumed_diamond
  return contour_array, presumed_diamond

# a segment ######################################################
def build_a_segment(length):
  contour = np.array([[0, 0], [0, length]])
  return contour

# a triangle ######################################################
def build_a_triangle(width, height):
  contour_array = np.array([[-1/2, 1], [0, 0], [1/2, 1]]) * [width, height]
  return contour_array

# an arc ##########################################################
def _build_an_arc(angle_start, angle_end):
  if angle_start > angle_end:
    angle_start, angle_end = angle_end, angle_start

  angle_start_normalized = angle_start / full_turn_angle
  angle_end_normalized   = angle_end   / full_turn_angle

  turn_nb_start = floor(angle_start_normalized)
  turn_nb_end   = floor(  angle_end_normalized)

  residual_start = ceil((angle_start_normalized - turn_nb_start) * my_default_vertices_qty_in_circle)
  residual_end = floor((angle_end_normalized - turn_nb_end)  * my_default_vertices_qty_in_circle)

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

def build_an_arc(angle_start, angle_end, radius=1):
  contour, _, _ = _build_an_arc(angle_start=angle_start, angle_end=angle_end)
  result = contour * radius
  return result

# an arc with different speeds ####################################
def build_an_arc_multispeed(angle_start, angle_end, speed_x, width, height):
  if angle_start > angle_end:
    angle_start, angle_end = angle_end, angle_start

  step = full_turn_angle / (max(abs(speed_x), 1) * my_default_vertices_qty_in_circle)
  angles = link_contours(np.arange(angle_start, angle_end, step), [angle_end])

  contour = np.array([[sin_hours(a * speed_x), cos_hours(a)] for a in angles])  * [width/2, height/2]
  return contour

# a circle ########################################################
def build_a_circle(radius):
  contour = build_an_arc(angle_start=0, angle_end=full_turn_angle) * radius
  return contour 

# an ellipse ######################################################
def build_an_ellipse(width, height):
  contour = build_an_arc(angle_start=0, angle_end=full_turn_angle) * [width/2, height/2]
  return contour

# a coil ##########################################################
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

  contour[:, 0] *= mult_xy
  contour[:, 1] *= mult_xy
  contour[:, 0] += add_x
  contour -= contour[0]

  return contour

# a smile ###########################################################
# depth is middle_y_to_half_width
def build_a_smile(width, depth):
  # if mid_point is almost at the same hor line, assume it's a straight line
  if is_the_same_point(depth/(width/2), 0.0): # this will be a segment
    result = np.empty([2, 2])
  elif abs(depth/(width/2)) <= 1: # an arc of a circle
    radius = abs((1 + (depth/(width/2))**2) / (2 * depth/(width/2)))
    angle = (asin_hours(sin_value = 1 / radius))
    # reusing build_arc
    result = build_an_arc(angle_start=-angle, 
                          angle_end=+angle) * radius - [0, radius-abs(depth/(width/2))]
    if depth > 0:
      result[:, 1] *= -1
  else: # a half-ellipse
    result = build_an_arc(angle_start=full_turn_angle/4, 
                          angle_end=full_turn_angle*3/4) * [-1, depth/(width/2)]
  # adjusting start and end points to make sure they match the inputs exactly
  result[0] = [-1, 0]
  result[-1] = [1, 0]
  # scaling!
  result *= abs((width/2))
  # all done!
  return result

# an eye ########################################################
def build_an_eye(width, depth_1, depth_2): 
  smile1 = build_a_smile(width=width, depth=depth_1)
  smile2 = build_a_smile(width=width, depth=depth_2)
  result = link_contours(smile1, smile2[::-1])
  return result

# a sector ######################################################
def build_a_sector(angle_start, angle_end, radius, radius_2=0):
  # make sure radius_1 >= radius_2 >= 0
  if abs(radius) > abs(radius_2):
    radius, radius_2 = abs(radius), abs(radius_2)
  else:
    radius_2, radius = abs(radius), abs(radius_2)

  contour = build_an_arc(angle_start=angle_start, angle_end=angle_end)

  if is_the_same_point(radius_2, 0.0):
    # special case - just add the mid-point
    result = link_contours(contour, [[0, 0]]) * radius
  else:
    # add the arc
    inner_arc = np.ndarray.copy(contour) * radius_2
    result = link_contours(contour * radius, inner_arc[::-1])
  return result

# a drop #########################################################
def build_an_elliptic_drop(width, height):
  contour = build_an_arc_multispeed(angle_start=full_turn_angle/4, angle_end=full_turn_angle*3/4, speed_x=2.0, width=width, height=height*2)
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
  right_arc = build_an_arc(angle_start=full_turn_angle-angle_top_middle, angle_end=full_turn_angle*1.25+angle_bottom) * radius
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
def _build_an_egg(power, tip_addon):

  h = lambda cos_alpha: cos_alpha * (1 - 1 / power) + 1 / (power * cos_alpha) - (1 + tip_addon)
  cos_alpha_solution = fsolve(h , x0=.5)[0]

  if cos_alpha_solution > 1.:
    cos_alpha_solution = 1 / (cos_alpha_solution * (power-1))

  if is_the_same_point(1., cos_alpha_solution):
    a = 0
  else:
    a = (1 + tip_addon - cos_alpha_solution) / ((1 - cos_alpha_solution*cos_alpha_solution) ** (power/2))

  alpha_solution = acos_hours(cos_alpha_solution)
  _arc = build_an_arc(angle_start=0, angle_end=full_turn_angle/2-alpha_solution)

  pf_points_qty = int(my_default_vertices_qty_in_circle/4)

  power_func_x = sqrt(1 - cos_alpha_solution*cos_alpha_solution) * (1. - np.array([n/pf_points_qty for n in range(pf_points_qty+1)]))
  power_func_2D = [[x, a * (x**power) ] for x in power_func_x]

  right_half_contour = link_contours(_arc + [0, (1 + tip_addon)], power_func_2D) 

  # adding the left half and
  # moving the egg so that its centre were where needed
  contour = add_a_left_mirror(right_half_contour)
  return contour

def build_an_egg(width, height, height_widest_point, power):
  tip_addon = height/(height - height_widest_point) - 2
  _unscaled_egg = _build_an_egg(power=power, tip_addon=tip_addon)
  contour = _unscaled_egg * [width/2, height/(2+tip_addon)]
  return contour

# a regular polygon ###################################################
def build_a_regular_polygon(vertices_qty, radius): 
  angles = [(i * full_turn_angle / vertices_qty) for i in range(vertices_qty)]
  contour = np.array([[sin_hours(a), cos_hours(a)] for a in angles]) * radius
  return contour

# a star #############################################################
def build_a_star(ends_qty, radius_1, radius_2): 
  angles = [i * full_turn_angle/(2*ends_qty) for i in range(2*ends_qty)]
  radii = [radius_1 * (i%2 == 0) + radius_2 * (i%2 == 1) for i in range(2*ends_qty)]

  contour = np.array([[radii[i] * sin_hours(angles[i]), 
                       radii[i] * cos_hours(angles[i])] for i in range(2*ends_qty)])

  return  contour

## a rhombus ###########################################################
def build_a_rhombus(width, height):
  contour = build_a_regular_polygon(vertices_qty=4, radius=1) * [width/2, height/2]
  return contour

## a zigzag ###########################################################
def build_a_wave(width, height, angle_start, nb_waves):

  contour, added_start, added_end = _build_an_arc(angle_start=angle_start, 
                                                    angle_end=angle_start+nb_waves*full_turn_angle)
  # y's will be sin's, the x's of _build_an_arc's output, with normalization
  contour[:, 1] = contour[:, 0] * height/2
  # x's are mostly equidistant. We start by putting together an array of distances
  contour[:, 0] = contour[:, 0] * 0 + 1
  contour[0, 0] = 0
  if added_start is not None:
    contour[1, 0] = added_start
  if added_end is not None:
    contour[-1, 0] = added_end
  # now computing x's and normalizing them
  contour[:, 0] = np.cumsum(contour[:, 0])
  contour[:, 0] *= width/ contour[-1, 0]
  # adjust the starting point 
  contour -= contour[0, :]

  return contour

## a zigzag ###########################################################
def _build_a_V_sequence(start, end):
  reverse = (start > end)
  if start > end:
    start, end = end, start

  nb_start = floor(start)
  nb_end   = floor(end)

  residual_start = start - nb_start
  residual_end   =      end - nb_end  

  # start and ending are in different V's
  if nb_end > nb_start:
    # repeted part
    contour = [[start, 1]]
    if nb_end - nb_start > 1:
      contour += [[1/2, -1], [1/2, 1]] * (nb_end - nb_start - 1)
    # adding custom start
    if 1/2 <= residual_start:
      contour[0][0] = 1 - residual_start
      contour = [[start, -3 + 4 * residual_start]] + contour
    else:
      contour[0][0] = 1/2
      contour = [[start, 1 - 4 * residual_start], [1/2 - residual_start, -1]] + contour
    
    # adding custom ending
    if 0 < residual_end <= 1/2:
      contour += [[residual_end, 1 - 4 * residual_end]]
    elif 1/2 < residual_end:
      contour += [[1/2, -1], [residual_end - 1/2, -3 + 4 * residual_end]]

  else: #same V
    # both points are in \
    if residual_end <= 1/2:
      contour = [[start, 1 - 4 * residual_start], 
                 [end - start, 1 - 4 * residual_end]]
    # both points are in /
    elif residual_start >= 1/2:
      contour = [[start, -3 + 4 * residual_start], 
                 [end - start, -3 + 4 * residual_end]]
    # start < 1/2 + nb_start < end
    else:
      contour = [[start, 1 - 4 * residual_start], 
                 [1/2 + nb_start - start, -1], 
                 [end - (1/2 + nb_start), -3 + 4 * residual_end]]
  contour = np.array(contour)
  if reverse:
    contour[:, 0] = contour[:, 0][::-1]

  return contour


def build_a_zigzag(width, height, angle_start, nb_segments):

  angle_start_normalized = angle_start / full_turn_angle
  angle_end_normalized   = angle_start_normalized + nb_segments / 2

  contour = _build_a_V_sequence(start = angle_start_normalized - 1/4, end = angle_end_normalized - 1/4)
    

  contour[:, 0] = np.cumsum(contour[:, 0])
  contour -= contour[0]
  contour[:, 0] *= width / contour[-1, 0]
  contour[:, 1] *= height/2

  return contour