import numpy as np
from matplotlib.colors import is_color_like
from MY_zyxxy_SETTINGS import my_colour_palette

##################################################################
## COLOUR HELPERS                                               ## 
##################################################################

# Find colour that should be used. 
# Assume that it's a name of a standard colour.
# Attention, names are case-sensitive
def find_colour_code(colour_name):
  if colour_name is None:
    return 'none'
  if isinstance(colour_name, str) and colour_name in my_colour_palette:
    return my_colour_palette[colour_name] 

  if not is_color_like(colour_name):
    raise Exception(colour_name, "is not a valid colour!")
  return colour_name

##################################################################

def find_GCD(n, m):
  while n % m != 0:
    n = n % m
    n, m = m, n
  return int(m)

def find_LCM(n, m):
  result = int(n * m / find_GCD(n=n, m=m))
  return result

def sign_(n):
  if n > 0:
    return 1
  if n < 0:
    return -1
  return 0

def create_gradient_colours(rgb_start, rgb_end):

  nb_steps_per_channel = [int(abs(rgb_start[i]- rgb_end[i])+1) for i in range(3)]

  nb_steps = 1
  for i in range(3):
    nb_steps = find_LCM(n=nb_steps_per_channel[i], m=nb_steps)

  result = np.array([rgb_start for _ in range(nb_steps)])
  for i in range(3):
    size_of_the_step = int(nb_steps / nb_steps_per_channel[i])
    for j in range(nb_steps_per_channel[i]):
      result[j*size_of_the_step : (j+1)*size_of_the_step, i] += sign_(rgb_end[i]-rgb_start[i]) * j

  result = [[re/ 255. for re in r] for r in result] 

  return result