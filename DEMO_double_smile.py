#######################################################
## Importing functions that we will use below        ##
from zyxxy_canvas import create_canvas_and_axes, show_drawing_and_save_if_needed
from zyxxy_shapes import draw_a_double_smile
from zyxxy_helpers import set_xy
from zyxxy_coordinates import build_a_double_smile

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

#########################################################
## CREATING THE DRAWING!                               ##
#######################################################
# Creating the canvas!                               ##
ax = create_canvas_and_axes(canvas_width = 12,
                            canvas_height = 10)

double_smile_shape = draw_a_double_smile(ax=ax, centre_x=0, width=2, corners_y=0, mid1_y=0, mid2_y=0, colour='red')

button = Button(plt.axes([0.6, 0.025, 0.1, 0.04]), 'Reset')

param_params_dict = {'centre_x' : [0, 12, 6], 
                     'width' : [0, 6, 3], 
                     'corners_y' : [0, 10, 8], 
                     'mid1_y' : [0, 10, 6], 
                     'mid2_y' : [0, 10, 5]}
sliders = {}
counter = 0
step = 1
for param_name, param_params in param_params_dict.items():
  sliders[param_name] = Slider(
                          plt.axes([0.35, 0.1+0.05*counter, 0.5, 0.03]), param_name, param_params[0], param_params[1], valinit=param_params[2], valstep=step)
  counter += 1

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

show_drawing_and_save_if_needed()