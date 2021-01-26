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
from zyxxy_settings import set_fill_in_outline_kwarg_defaults
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

new_shape=None

slider_range = {'half_way_0_1' : np.array([0., 1., 0.5, 1]),
                'stretch'      : np.array([0., 5, 1, 0.1]),
                'turn'         : np.array([0, 12, 0, 1]),
                'double_turn'  : np.array([0, 24, 0, 1]),
                'long_turn'    : np.array([0, 60, 0, 3]),
                'half_turn'    : np.array([0,  6, 0, 1]),
                'minus_1_to_1' : np.array([-1., 1., 0., .1]),
                'vertices'     : np.array([0, 12, 0, 1]),}

common_params_dict_definition = {'turn' : 'turn',
                                 'stretch_x' : 'stretch',
                                 'stretch_y' : 'stretch',
                                 'diamond_x' : 'half_way_0_1', 
                                 'diamond_y' : 'half_way_0_1'}

shape_names_params_dicts_definition = {
                            'a_rhombus' : {},
                            'a_triangle': {}, 
                            'a_square': {}, 
                            'a_circle': {}, 
                            'an_elliptic_drop': {},
                            'a_smile': {'dip' : 'minus_1_to_1'},
                            'a_star': {'ends_qty' : 'vertices', 'radii_ratio' : 'stretch'},
                            'a_regular_polygon': {'vertices_qty' : 'vertices'},
                            #'an_ellipse': {'radius_x' : [], 'radius_y' : []},
                            'a_double_smile': {'dip_1' : 'minus_1_to_1', 'dip_2' : 'minus_1_to_1'},
                            'a_heart': {'angle_middle' : 'half_turn', 'tip_addon' : 'stretch'},
                            'a_sector': {'angle_start' : 'turn', 'angle_end' : 'double_turn', 'radii_ratio' : 'stretch'},
                            'an_arc': {'angle_start' : 'turn', 'angle_end' : 'double_turn', 'speed_x' : 'stretch', 'speed_y' : 'stretch'}}

def run_demo(shapename):
  this_shape_params_definition = shape_names_params_dicts_definition[shapename]
  shape_params_dict =  {key:np.copy(slider_range[value]) for key, value in this_shape_params_definition.items()}
  top_slider_location = max(len(shape_params_dict), len(common_params_dict_definition))
  my_default_margin_adjustments['bottom'] += 0.05 * top_slider_location

  # Creating the canvas!
  ax = create_canvas_and_axes(canvas_width=my_default_demo_canvas_size[0],
                              canvas_height=my_default_demo_canvas_size[1],
                              tick_step=my_default_demo_tick_step,
                              title="Try Out "+shapename)
  
  common_params_dict = {key:np.copy(slider_range[value]) for key, value in common_params_dict_definition.items()}
  
  common_params_dict['diamond_x'][:-1] *= my_default_demo_canvas_size[0]
  common_params_dict['diamond_y'][:-1] *= my_default_demo_canvas_size[1]

  button = Button(plt.axes([0.6, 0.025, 0.1, 0.04]), 'Reset')

  sliders_specific = {}
  sliders_common = {}
  for slider_start, param_params_dict, target in ((0.15, shape_params_dict, sliders_specific), (0.65, common_params_dict, sliders_common)):
    counter = top_slider_location
    for param_name, param_params in param_params_dict.items():
      counter -= 1
      target[param_name] = Slider(ax=plt.axes([slider_start, 0.1+0.05*counter, 0.3, 0.03]), label=param_name, valmin=param_params[0], valmax=param_params[1], valinit=param_params[2], valstep=get_step(params = param_params))

  def draw_new_shape(ax):
    global new_shape

    kwargs_shape = {key:sliders_specific[key].val for key in sliders_specific.keys()}
    kwargs_common= {key:sliders_common[key].val for key in ['turn', 'stretch_x', 'stretch_y']}
    kwargs_common['diamond'] = [sliders_common['diamond_x'].val, 
                                sliders_common['diamond_y'].val]
    colour_etc_kwargs = set_fill_in_outline_kwarg_defaults({}, defaults_for_demo=True)

    if new_shape is None:
      new_shape = draw_given_shapename(ax=ax, is_patch=True, shapename=shapename, kwargs_shape=kwargs_shape, kwargs_common=kwargs_common, **colour_etc_kwargs)
    else:
      new_shape.update_given_shapename(shapename=shapename, kwargs_shape=kwargs_shape, kwargs_common=kwargs_common)
   
    plt.draw()

  def update(val):
    draw_new_shape(ax=ax)

  def reset(event):
    for _slider in ([v for v in sliders_specific.values()] + [v for v in sliders_common.values()]):
      _slider.reset()

  for _slider in ([v for v in sliders_specific.values()] + [v for v in sliders_common.values()]):
      _slider.on_changed(update)

  button.on_clicked(reset)
  
  draw_new_shape(ax=ax)
  show_drawing_and_save_if_needed(figsize=my_default_demo_figsize, 
                                  dpi=my_default_demo_dpi,
                                  margin_adjustments=my_default_margin_adjustments)