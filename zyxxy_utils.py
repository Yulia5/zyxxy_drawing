#####################################################
## don't change this file, please                  ##
#####################################################

import math
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from zyxxy_settings import set_outline_kwarg_default
from zyxxy_MY_SETTINGS import my_default_diamond_size,my_default_diamond_colour, my_colour_palette

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