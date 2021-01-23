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


tolerance = 0.0001

def is_the_same_point(p1, p2):
  sqr_dist = ((p1[0] - p2[0]) ** 2) + ((p1[1] - p2[1]) ** 2) 
  return (sqr_dist < tolerance)

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

def stretch_something(what_to_stretch, diamond, stretch_coeff):
  if is_the_same_point(stretch_coeff, 1.):
    return what_to_stretch
  result = diamond + (what_to_stretch - diamond) * stretch_coeff
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
  return math.sin(math.radians(turn * 30))
def cos_hours(turn):
  return math.cos(math.radians(turn * 30))
def tan_hours(turn):
  return math.tan(math.radians(turn * 30))

def asin_hours(sin_value):
  return math.degrees(math.asin(min(1.0, sin_value)))/30 
def acos_hours(cos_value):
  return math.degrees(math.acos(min(1.0, cos_value)))/30 