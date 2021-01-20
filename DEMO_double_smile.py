#######################################################
## Importing functions that we will use below        ##
from zyxxy_canvas import create_canvas_and_axes, show_drawing_and_save_if_needed
from zyxxy_shapes import draw_a_double_smile
from zyxxy_helpers import set_xy
from zyxxy_coordinates import build_a_double_smile
from zyxxy_MY_SETTINGS import my_default_margin_adjustments

import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

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

double_smile_shape = draw_a_double_smile(ax=ax, centre_x=0, width=2, corners_y=0, mid1_y=0, mid2_y=0, colour='red')

button = Button(plt.axes([0.6, 0.025, 0.1, 0.04]), 'Reset')

sliders = {}
for slider_start, param_params_dict in ((0.15, shape_params_dict), (0.65, common_params_dict)):
  counter = top_slider_location
  for param_name, param_params in param_params_dict.items():
    counter -= 1
    sliders[param_name] = Slider(ax=plt.axes([slider_start, 0.1+0.05*counter, 0.35, 0.03]), label=param_name, valmin=param_params[0], valmax=param_params[1], valinit=param_params[2], valstep=get_step(params = param_params))


def update(val):
  params = {key:sliders[key].val for key, value in sliders.items()}
  data = build_a_double_smile(**params)
  set_xy(double_smile_shape, data)
  plt.draw()

def reset(event):
  for _slider in sliders.values():
    _slider.reset()

for _slider in sliders.values():
    _slider.on_changed(update)
button.on_clicked(reset)

# Initialize plot with correct initial active value
update(None)
show_drawing_and_save_if_needed(figsize = [5, 5])