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
from zyxxy_shapes_base import Shape
from zyxxy_settings import set_fill_in_outline_kwarg_defaults
from MY_zyxxy_SETTINGS import my_default_margin_adjustments, my_default_demo_canvas_size, my_default_demo_figsize, my_default_demo_dpi, my_default_demo_tick_step

import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
import numpy as np

slider_range = {'half_way_0_1' : [0., 1., 0.5, 1],
                'stretch'      : [0., 5, 1, 0.1],
                'turn'         : [0, 12, 0, 1],
                'double_turn'  : [0, 24, 0, 1],
                'long_turn'    : [0, 60, 0, 3],
                'half_turn'    : [0,  6, 0, 1],
                'minus_1_to_1' : [-1., 1., 0., .1],
                'vertices'     : [1, 12, 5, 1],}

common_params_dict_definition = {'stretch_x' : 'stretch',
                                 'stretch_y' : 'stretch',
                                 'turn' : 'turn',
                                 'diamond_x' : 'half_way_0_1', 
                                 'diamond_y' : 'half_way_0_1'}

shape_names_params_dicts_definition = {
                            'a_circle': {}, 
                            'a_rhombus' : {},
                            'a_triangle': {}, 
                            'a_square': {}, 
                            'an_elliptic_drop': {},
                            'a_smile': {'dip' : 'minus_1_to_1'},
                            'a_star': {'ends_qty' : 'vertices', 'radii_ratio' : 'stretch'},
                            'a_regular_polygon': {'vertices_qty' : 'vertices'},
                            #'an_ellipse': {'radius_x' : [], 'radius_y' : []},
                            'a_double_smile': {'dip_1' : 'minus_1_to_1', 'dip_2' : 'minus_1_to_1'},
                            'a_heart': {'angle_middle' : 'half_turn', 'tip_addon' : 'stretch'},
                            'a_sector': {'angle_start' : 'turn', 'angle_end' : 'double_turn', 'radii_ratio' : 'stretch'},
                            'an_arc': {'angle_start' : 'turn', 'angle_end' : 'double_turn', 'speed_x' : 'stretch', 'speed_y' : 'stretch'}}

shapes_by_side_by_shapename = {'left' : {key : None for key in shape_names_params_dicts_definition.keys()},
                               'right': {key : None for key in shape_names_params_dicts_definition.keys()},}
widgets_by_side_by_shapename = {'left' : {key : {} for key in shape_names_params_dicts_definition.keys()},
                                'right': {key : {} for key in shape_names_params_dicts_definition.keys()},}
active_shapename = {'left' : None, 'right' : None}

# Creating the canvas!
ax = create_canvas_and_axes(canvas_width=my_default_demo_canvas_size[0],
                            canvas_height=my_default_demo_canvas_size[1], 
                            tick_step=my_default_demo_tick_step,
                            title="Try Out Shapes")
rax_left = plt.axes([0.025, 0.3, 0.15, 0.05*len(shape_names_params_dicts_definition)])
radio_left = RadioButtons(rax_left, shape_names_params_dicts_definition.keys(), active=2)
count_shapes = 0


def place_shapes_and_widgets(side, shapename):
  global count_shapes
  count_shapes += 1
  this_shape_params_definition = shape_names_params_dicts_definition[shapename]
  shape_params_dict = {key:np.copy(slider_range[value]) for key, value in this_shape_params_definition.items()}
  top_slider_location = len(shape_params_dict) + len(common_params_dict_definition)

  common_params_dict = {key:np.copy(slider_range[value]) for key, value in common_params_dict_definition.items()}
  
  common_params_dict['diamond_x'][:-1] *= my_default_demo_canvas_size[0]
  common_params_dict['diamond_y'][:-1] *= my_default_demo_canvas_size[1]

  if side == 'left':
    widget_left = 0.15
  else:
    widget_left = 0.65
  widget_left += count_shapes * 0.0001

  #widgets_by_side_by_shapename[side][shapename]['Reset'] = plt.axes([widget_left, 0.025, 0.1, 0.04])
  button = Button(ax=plt.axes([widget_left, 0.025, 0.1, 0.04]) , label='Reset')

  counter = top_slider_location
  sliders_specific = {}
  sliders_common = {}
  for param_params_dict, target in ((shape_params_dict, sliders_specific), (common_params_dict, sliders_common)):
    for param_name, param_params in param_params_dict.items():
      counter -= 1
      target[param_name] = Slider(ax=plt.axes([widget_left, 0.1+0.05*counter, 0.3, 0.03]), label=shapename+param_name, valmin=param_params[0], valmax=param_params[1], valinit=param_params[2], valstep=param_params[3])

  widgets_by_side_by_shapename[side][shapename] = {'sliders_specific': sliders_specific, 
                                                   'sliders_common': sliders_common, 
                                                   'button': button}
  colour_etc_kwargs = set_fill_in_outline_kwarg_defaults({}, defaults_for_demo=True)
  _shape = Shape(ax=ax, is_patch=True, **colour_etc_kwargs)
  shapes_by_side_by_shapename[side][shapename] = _shape                                                

  def draw_new_shape():
    global shapes_by_side_by_shapename
    global widgets_by_side_by_shapename
    _shape = shapes_by_side_by_shapename[side][shapename]
    _widgets = widgets_by_side_by_shapename[side][shapename]
    _sliders_specific = _widgets['sliders_specific']
    _sliders_common = _widgets['sliders_common']

    kwargs_shape = {key:_sliders_specific[key].val for key in sliders_specific.keys()}
    kwargs_common= {key:_sliders_common[key].val for key in ['turn', 'stretch_x', 'stretch_y']}
    kwargs_common['diamond'] = [_sliders_common['diamond_x'].val, 
                                _sliders_common['diamond_y'].val]
    _shape.update_given_shapename(shapename=shapename, kwargs_shape=kwargs_shape, kwargs_common=kwargs_common)
   
    ax.redraw_in_frame()

  def update(val):
    draw_new_shape()

  def reset(event):
    for _slider in ([v for v in sliders_specific.values()] + [v for v in sliders_common.values()]):
      _slider.reset()

  for _slider in ([v for v in sliders_specific.values()] + [v for v in sliders_common.values()]):
      _slider.on_changed(update)

  button.on_clicked(reset)

def switch_demo(side, shapename, switch_on):
  if shapename is None:
    return
  _shape = shapes_by_side_by_shapename[side][shapename]
  _widgets = widgets_by_side_by_shapename[side][shapename]
  if not switch_on:
    _shape.set_visible(None)
  else:
    _shape.set_visible(True) # depends on the switch

  # widgets
  _widgets['button'].ax.set_visible(switch_on)
  for _s in _widgets['sliders_specific'].values():
    _s.ax.set_visible(switch_on)
  for _s in _widgets['sliders_common'].values():
    _s.ax.set_visible(switch_on)

  widgets_qty = len(_widgets['sliders_specific']) + len(_widgets['sliders_common'])
  return widgets_qty


for side in ['left', 'right']:
  for shapename in shape_names_params_dicts_definition.keys():
    place_shapes_and_widgets(side=side, shapename=shapename)
    switch_demo(side=side, shapename=shapename, switch_on=False)
plt.draw()

def switch_demo_left(label):
  # label == radio_left.value_selected
  switch_demo(side='left', shapename=active_shapename['left'] , switch_on=False)
  widgets_qty = switch_demo(side='left', shapename=label, switch_on=True)
  active_shapename['left'] = label
  margin_adjustments = {k:v for k, v in my_default_margin_adjustments.items()}
  margin_adjustments['bottom'] += 0.05 * widgets_qty
  plt.subplots_adjust(**margin_adjustments)
  plt.draw()

radio_left.on_clicked(switch_demo_left)

# Initialize plot with correct initial active value
switch_demo_left(radio_left.value_selected)

show_drawing_and_save_if_needed(figsize=my_default_demo_figsize, 
                                  dpi=my_default_demo_dpi)