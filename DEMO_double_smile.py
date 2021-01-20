#######################################################
## Importing functions that we will use below        ##
from zyxxy_canvas import create_canvas_and_axes, show_drawing_and_save_if_needed
from zyxxy_shapes import draw_a_polygon
from zyxxy_helpers import set_xy, stretch_something, rotate_something, shift_something
import zyxxy_coordinates
from MY_zyxxy_SETTINGS import my_default_margin_adjustments

import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import numpy as np

old_diamond_coords = np.array([0, 0])

default_step = 1
def get_step(params):
  step = default_step
  for p in params:
    candidate_step = p % 1
    if candidate_step > 0.01 and candidate_step < step:
      step = candidate_step
  return step

common_params_dict = {'turn' : [0, 12, 0],
                      'stretch_x' : [0.2, 5, 1],
                      'stretch_y' : [0.2, 5, 1]}

shapename = "a_double_smile"
shape_params_dict = {'centre_x' : [0, 12, 6], 
                     'width' : [0, 6, 3], 
                     'corners_y' : [0, 10, 8], 
                     'mid1_y' : [0, 10, 6], 
                     'mid2_y' : [0, 10, 5]}

top_slider_location = max(len(shape_params_dict), len(common_params_dict))

my_default_margin_adjustments['bottom'] += 0.05 * top_slider_location

#########################################################
## CREATING THE DRAWING!                               ##
#########################################################
# Creating the canvas!                                 ##
ax = create_canvas_and_axes(canvas_width = 16,
                            canvas_height = 10,
                            tick_step = 1,
                            title = "Try Out " + shapename)

# does not matter what shape, it will be redrawn

diamond_shape, shape = draw_a_polygon(ax=ax, contour=np.array([[0,0], [1,1], [2,0]]), diamond=old_diamond_coords, colour='red')

button = Button(plt.axes([0.6, 0.025, 0.1, 0.04]), 'Reset')

sliders_specific = {}
sliders_common = {}
for slider_start, param_params_dict, target in ((0.15, shape_params_dict, sliders_specific), (0.65, common_params_dict, sliders_common)):
  counter = top_slider_location
  for param_name, param_params in param_params_dict.items():
    counter -= 1
    target[param_name] = Slider(ax=plt.axes([slider_start, 0.1+0.05*counter, 0.3, 0.03]), label=param_name, valmin=param_params[0], valmax=param_params[1], valinit=param_params[2], valstep=get_step(params = param_params))

def update(val):
  global old_diamond_coords
  # setting parameters and method to call
  kwargs = {key:sliders_specific[key].val for key in sliders_specific.keys()}
  method_to_call = getattr(zyxxy_coordinates, 'build_'+shapename)
  # putting them together to create the initial contour and the diamond
  diamond_coords, contour = method_to_call(**kwargs)
  # stretching
  contour = stretch_something(something=contour, diamond=diamond_coords, stretch_x=sliders_common['stretch_x'].val, stretch_y=sliders_common['stretch_y'].val)
  # turning
  contour = rotate_something(something=contour, diamond=diamond_coords, turn=sliders_common['turn'].val)
  # updating the plot
  set_xy(shape, contour)
  shift_something(something=diamond_shape, shift=np.array(diamond_coords)-old_diamond_coords)
  old_diamond_coords = np.array(diamond_coords)
  plt.draw()

def reset(event):
  for _slider in sliders_specific.values():
    _slider.reset()
  for _slider in sliders_common.values():
    _slider.reset()

for _slider in sliders_specific.values():
  _slider.on_changed(update)
for _slider in sliders_common.values():
  _slider.on_changed(update)
button.on_clicked(reset)

# Initialize plot with correct initial active value
update(None)
show_drawing_and_save_if_needed(figsize = [6, 5])