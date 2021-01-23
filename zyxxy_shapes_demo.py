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
from zyxxy_shapes_base import draw_given_shapename
from MY_zyxxy_SETTINGS import my_default_margin_adjustments, my_default_demo_canvas_size, my_default_demo_figsize, my_default_demo_dpi, my_default_demo_tick_step

import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import numpy as np

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
                      'stretch_y' : [0.2, 5, 1],
                      'diamond_x' : np.array([0.5, 0, 1]), 
                      'diamond_y' : np.array([0.5, 0, 1])}

shape_names_params_dicts = {'a_rhombus' : {},
                            'a_triangle': {}, 
                            'a_square': {}, 
                            'a_circle': {}, 
                            'an_elliptic_drop': {},
                            'a_smile': {'dip' : []},
                            'a_star': {'ends_qty' : [], 'radii_ratio' : []},
                            'a_regular_polygon': {'vertices_qty' : []},
                            'an_ellipse': {'radius_x' : [], 'radius_y' : []},
                            'a_double_smile': {'dip_1' : [], 'dip_2' : []},
                            'a_heart': {'angle_middle' : [], 'tip_addon' : []},
                            'a_sector': {'angle_start' : [], 'angle_end' : [], 'radii_ratio' : []},
                            'an_arc': {'angle_start' : [], 'angle_end' : [], 'speed_x' : [], 'speed_y' : []}}

def run_demo(shapename):
  shape_params_dict = shape_names_params_dicts[shapename]

  top_slider_location = max(len(shape_params_dict), len(common_params_dict))

  my_default_margin_adjustments['bottom'] += 0.05 * top_slider_location

  # Creating the canvas!
  ax = create_canvas_and_axes(canvas_width=my_default_demo_canvas_size[0],
                              canvas_height=my_default_demo_canvas_size[1],
                              tick_step=my_default_demo_tick_step,
                              title="Try Out "+shapename)
  
  common_params_dict['diamond_x'] *= my_default_demo_canvas_size[0]
  common_params_dict['diamond_y'] *= my_default_demo_canvas_size[1]

  button = Button(plt.axes([0.6, 0.025, 0.1, 0.04]), 'Reset')

  sliders_specific = {}
  sliders_common = {}
  for slider_start, param_params_dict, target in ((0.15, shape_params_dict, sliders_specific), (0.65, common_params_dict, sliders_common)):
    counter = top_slider_location
    for param_name, param_params in param_params_dict.items():
      counter -= 1
      target[param_name] = Slider(ax=plt.axes([slider_start, 0.1+0.05*counter, 0.3, 0.03]), label=param_name, valmin=param_params[0], valmax=param_params[1], valinit=param_params[2], valstep=get_step(params = param_params))

  def draw_new_shape():
    global new_shape

    kwargs_shape = {key:sliders_specific[key].val for key in sliders_specific.keys()}
    kwargs_common= {key:sliders_common[key].val for key in sliders_common.keys()}

    new_shape = draw_given_shapename(ax=None, is_patch=True, shapename=shapename, shape_kwargs=kwargs_shape, **kwargs_common)
    plt.draw()

  def update_specific(val):
    draw_new_shape()

  def just_stretch():
    global new_shape
    new_shape.stretch(stretch_x=sliders_common['stretch_x'].val, 
                        stretch_y=sliders_common['stretch_y'].val)
  def just_shift():
    global new_shape
    new_shape.shift(shift=[sliders_common['diamond_x'].val, 
                           sliders_common['diamond_y'].val])  
  def just_turn():
    global new_shape
    new_shape.rotate(turn=sliders_common['turn'].val)  

  def update_given_action(action_func):
    global new_shape
    if new_shape is None:
      draw_new_shape()
    else:
      action_func()
      plt.draw()

  def update_stretch(val):
    update_given_action(just_stretch)

  def update_shift(val):
    update_given_action(just_shift)    
    
  def update_turn(val):
    update_given_action(just_turn)    

  def reset(event):
    for _slider in [sliders_specific.values() + sliders_common.values()]:
      _slider.reset()

  for _slider in sliders_specific.values():
    _slider.on_changed(update_specific)

  for _slider in [sliders_common['stretch_x'], sliders_common['stretch_y']]:
    _slider.on_changed(update_stretch)
  for _slider in [sliders_common['shift_x'], sliders_common['shift_y']]:
    _slider.on_changed(update_shift)
  sliders_common['turn'].on_changed(update_turn)
  button.on_clicked(reset)
  
  draw_new_shape()
  show_drawing_and_save_if_needed(figsize=my_default_demo_figsize, dpi=my_default_demo_dpi)