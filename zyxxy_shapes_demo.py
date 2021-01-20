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

from zyxxy_canvas import create_canvas_and_axes, show_drawing_and_save_if_needed
from zyxxy_patches import draw_a_polygon
from zyxxy_shapes_base import  update_xy
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

def run_demo(shapename, shape_params_dict):

  top_slider_location = max(len(shape_params_dict), len(common_params_dict))

  my_default_margin_adjustments['bottom'] += 0.05 * top_slider_location

  # Creating the canvas!
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
  
    kwargs_shape = {key:sliders_specific[key].val for key in sliders_specific.keys()}
    kwargs_common= {key:sliders_common[key].val for key in sliders_common.keys()}
  
    old_diamond_coords = update_xy(shapename=shapename, kwargs_shape=kwargs_shape, kwargs_common=kwargs_common, shape=shape, diamond_shape=diamond_shape, old_diamond_coords=old_diamond_coords)

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