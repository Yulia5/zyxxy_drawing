#####################################################
## don't change this file, please                  ##
#####################################################

import math
import random
import numpy as np

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


# auxiliary functions to define sin and cos of angles measured in hours
# we need "12-" because matlibplot's angle turns counterclockwise
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

# useful function to build animation scenarios
def build_piecewise_const_array(nb_elements_elements, total_size):
  result = []
  for nb_elements, element in nb_elements_elements:
    result += [element for _ in range(nb_elements)]
  result += [0 for _ in range(total_size - len(result))]
  return np.array(result, dtype=type(0.))