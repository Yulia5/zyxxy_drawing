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

import math
import random
import numpy as np

my_default_vertices_qty_in_circle = 72 
tolerance = 0.000000001
full_turn_angle = 12 # 12 for hours

##################################################################
def is_number(val):
  return isinstance(val, (int, float, np.float64, np.int64))

##################################################################
def is_the_same_point(p1, p2):
  diff = p1 - p2
  if is_number(diff):
    sqr_dist = diff**2
  else:
    sqr_dist = np.sum(diff**2) 
  return (sqr_dist < tolerance)

##################################################################
def conc_contours(a, b):
  if a.ndim != b.ndim:
    raise Exception("Dimension number mismatch", a.ndim, "!=", b.ndim)
  if a.ndim == 1:
    return np.hstack((a, b))
  else:
    return np.vstack((a, b))  

##################################################################
def is_the_same_contour(p1, p2, start_1=0, start_2=0, opposite_directions=False):
  assert p1.shape == p2.shape
  if (p1.size == 0):
    return True
    
  p1_modif = conc_contours(p1[start_1:-1], p1[:start_1])
  p2_modif = conc_contours(p2[start_2:-1], p2[:start_2])
  if opposite_directions:
    p2_modif = p2_modif[::-1]
  result = is_the_same_point(p1=p1_modif, p2=p2_modif)
  return result

##################################################################
def is_contour_V_symmetric(contour):
  result = is_the_same_contour(contour[:, 0], -contour[::-1][:, 0])
  return result

##################################################################
def remove_contour_points(contour, range_to_remove):
  result = np.delete(contour, range_to_remove, axis=0)
  return result

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
      result = conc_contours(result[:-1], a)
    else:
      result = conc_contours(result, a)
  return result

#####################################################
def add_a_left_mirror(contour, mirror_x=0):
  reverse_contour = np.copy(contour[::-1, :])
  reverse_contour[:, 0] = 2 * mirror_x - reverse_contour[:, 0]
  result = link_contours(reverse_contour, contour)
  return result

##################################################################
## MOVEMENT HELPERS                                             ## 
##################################################################

def rotate_point(point, diamond, turn):
  if (diamond is None) or is_the_same_point(turn, 0.):
    return point
  cos_turn = cos_hours(turn)
  sin_turn = sin_hours(turn)
  diff_0 = point[0] - diamond[0]
  diff_1 = point[1] - diamond[1]
  return [diamond[0] + diff_0 * cos_turn + diff_1 * sin_turn,
          diamond[1] - diff_0 * sin_turn + diff_1 * cos_turn] 

def _stretch_something(what_to_stretch, diamond, stretch_coeff):
  if is_the_same_point(stretch_coeff, 1.):
    return what_to_stretch
  result = diamond + (what_to_stretch - diamond) * stretch_coeff
  return result

def stretch_something(what_to_stretch, diamond, stretch_coeff):
  if is_number(what_to_stretch[0]):
    result = np.array([_stretch_something(what_to_stretch=what_to_stretch[i], 
                                          diamond=diamond[i], 
                                          stretch_coeff=stretch_coeff[i]) for i in [0, 1]]) 
  else:
    result = np.array([[_stretch_something(what_to_stretch=point[i], 
                                           diamond=diamond[i], 
                                           stretch_coeff=stretch_coeff[i]) for i in [0, 1]] for point in what_to_stretch]) 
  return result

##################################################################
## RANDOM NUMBERS HELPERS                                       ## 
##################################################################
def random_number(max, min=0.):
  return random.uniform(0, 1) * (max - min) + min

# both limits, min and max, are included in possible outcomes
def random_integer_number(max, min=0.):
  return random.randint(min, max)

def random_element(list_to_choose_from):
  return random.choice(list_to_choose_from)

##################################################################
## TRIGONOMETRY HELPERS                                         ## 
##################################################################

# auxiliary functions to define sin and cos of angles measured in hours
def sin_hours(turn):
  return math.sin(turn / full_turn_angle * (2 * math.pi))
def cos_hours(turn):
  return math.cos(turn / full_turn_angle * (2 * math.pi))
def tan_hours(turn):
  return math.tan(turn / full_turn_angle * (2 * math.pi))

def asin_hours(sin_value):
  return math.asin(sin_value) / (2 * math.pi) * full_turn_angle
def acos_hours(cos_value):
  return math.acos(cos_value) / (2 * math.pi) * full_turn_angle
def atan_hours(tan_value):
  return math.atan(tan_value) / (2 * math.pi) * full_turn_angle

########################################################################

def raise_Exception_if_not_processed(kwarg_keys, allowed_keys):
  not_processed = [arg_name for arg_name in kwarg_keys if arg_name not in allowed_keys]
  if len(not_processed) > 0:
    raise Exception("Arguments", ', '.join(not_processed), " are not recognised, allowed keys:", allowed_keys)

########################################################################

__is_running_tests = False

def is_running_tests(val=None):
  global __is_running_tests
  if val is not None:
    __is_running_tests = val
  return __is_running_tests

def wait_for_enter(msg = "Press ENTER when you are ready ..."):
  if not is_running_tests():
    _ = input(msg)
