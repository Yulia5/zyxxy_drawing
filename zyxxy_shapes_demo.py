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

from zyxxy_canvas import create_canvas_and_axes
from zyxxy_shapes_base import Shape
from zyxxy_settings import set_fill_in_outline_kwarg_defaults
from MY_zyxxy_SETTINGS import my_default_demo_canvas_size, my_default_demo_figsize, my_default_demo_dpi, my_default_demo_tick_step, my_default_demo_radio_width, my_default_demo_widget_height, my_default_demo_radio_side_margin, my_default_demo_widget_gap, my_default_demo_plot_gap, my_default_demo_plot_bottom_gap, my_default_demo_font_size

import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
import numpy as np

plt.rcParams.update({'font.size': my_default_demo_font_size})

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

# finding the max number of widgets
MAX_WIDGET_QTY = 0
for spec_param_dict in shape_names_params_dicts_definition.values():
  if MAX_WIDGET_QTY < len(spec_param_dict):
    MAX_WIDGET_QTY = len(spec_param_dict)
MAX_WIDGET_QTY += len(common_params_dict_definition) + 1

# variables that will be populated later

shapes_by_side_by_shapename = {'left' : {key : None for key in shape_names_params_dicts_definition.keys()},
                               'right': {key : None for key in shape_names_params_dicts_definition.keys()},}
widgets_by_side_by_shapename = {'left' : {key : {} for key in shape_names_params_dicts_definition.keys()},
                                'right': {key : {} for key in shape_names_params_dicts_definition.keys()},}
active_shapename = {'left' : None, 'right' : None}

my_default_demo_rax_bottom = (MAX_WIDGET_QTY + 1) * (my_default_demo_widget_height + my_default_demo_widget_gap )
# create the figure and the radio buttons
both_rax_x_left = {'left' : my_default_demo_radio_side_margin, 'right' : (1 - my_default_demo_radio_side_margin - my_default_demo_radio_width)}
shape_switcher = {}
shape_switcher_options = ['None']+[k for k in shape_names_params_dicts_definition.keys()]
fig = plt.figure()
for side, rax_x_left in both_rax_x_left.items():
  rax = plt.axes([rax_x_left, my_default_demo_rax_bottom, my_default_demo_radio_width, my_default_demo_widget_height*len(shape_switcher_options)])
  fig.add_axes(rax)
  shape_switcher[side] = RadioButtons(rax, shape_switcher_options, active=2)

# Creating the canvas!

big_axes_width = 1-2*(my_default_demo_radio_width + my_default_demo_radio_side_margin+my_default_demo_plot_gap)
ax = plt.axes([my_default_demo_radio_side_margin+my_default_demo_radio_width+my_default_demo_plot_gap, my_default_demo_rax_bottom+my_default_demo_plot_bottom_gap, big_axes_width, 1-my_default_demo_rax_bottom-my_default_demo_plot_bottom_gap])
fig.add_axes(ax)

create_canvas_and_axes(canvas_width=my_default_demo_canvas_size[0],
                            canvas_height=my_default_demo_canvas_size[1], 
                            tick_step=my_default_demo_tick_step,
                            title="Try Out Shapes",
                            title_font_size = my_default_demo_font_size*1.5,
                            axes_label_font_size = my_default_demo_font_size,
                            axes_tick_font_size = my_default_demo_font_size,
                            ax=ax)
plt.draw()
plt.show(block=False)

count_shapes = 0

def update_given_shapename_and_side(side, shapename):
  global shapes_by_side_by_shapename
  global widgets_by_side_by_shapename
  _shape = shapes_by_side_by_shapename[side][shapename]
  _widgets = widgets_by_side_by_shapename[side][shapename]
  _sliders_specific = _widgets['sliders_specific']
  _sliders_common = _widgets['sliders_common']

  kwargs_shape = {key:_sliders_specific[key].val for key in _sliders_specific.keys()}
  kwargs_common= {key:_sliders_common[key].val for key in ['turn', 'stretch_x', 'stretch_y']}
  kwargs_common['diamond'] = [_sliders_common['diamond_x'].val, 
                              _sliders_common['diamond_y'].val]
  _shape.update_given_shapename(shapename=shapename, kwargs_shape=kwargs_shape, kwargs_common=kwargs_common)

def place_shapes_and_widgets(side, shapename):
  global count_shapes
  count_shapes += 1
  this_shape_params_definition = shape_names_params_dicts_definition[shapename]
  shape_params_dict = {key:np.copy(slider_range[value]) for key, value in this_shape_params_definition.items()}

  common_params_dict = {key:np.copy(slider_range[value]) for key, value in common_params_dict_definition.items()}
  
  common_params_dict['diamond_x'][:-1] *= my_default_demo_canvas_size[0]
  common_params_dict['diamond_y'][:-1] *= my_default_demo_canvas_size[1]

  if side == 'left':
    widget_left = 0.15
  else:
    widget_left = 0.65
  widget_left += count_shapes * 0.0001 # this tiny adjustment is needed to avoid a 

  button = Button(ax=plt.axes([widget_left, 0.025, 0.1, my_default_demo_widget_height]) , label='Reset')

  counter = MAX_WIDGET_QTY + 1
  sliders_specific = {}
  sliders_common = {}
  for param_params_dict, target in ((shape_params_dict, sliders_specific), (common_params_dict, sliders_common)):
    for param_name, param_params in param_params_dict.items():
      counter -= 1
      target[param_name] = Slider(ax=plt.axes([widget_left, (my_default_demo_widget_height + my_default_demo_widget_gap )*counter, 0.3, my_default_demo_widget_height]), label=param_name, valmin=param_params[0], valmax=param_params[1], valinit=param_params[2], valstep=param_params[3])
      target[param_name].label.set_size(my_default_demo_font_size)
      #target[param_name].val.set_size(my_default_demo_font_size)
      

  widgets_by_side_by_shapename[side][shapename] = {'sliders_specific': sliders_specific, 
                                                   'sliders_common': sliders_common, 
                                                   'button': button}
  colour_etc_kwargs = set_fill_in_outline_kwarg_defaults({}, defaults_for_demo=True)
  _shape = Shape(ax=ax, is_patch=True, **colour_etc_kwargs)
  shapes_by_side_by_shapename[side][shapename] = _shape

  def update(val):
    update_given_shapename_and_side(side=side, shapename=shapename)

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

for side in ['left', 'right']:
  for shapename in shape_names_params_dicts_definition.keys():
    place_shapes_and_widgets(side=side, shapename=shapename)
plt.draw()
plt.show(block=False)

for side in ['left', 'right']:
  for shapename in shape_names_params_dicts_definition.keys():
    update_given_shapename_and_side(side=side, shapename=shapename)
    switch_demo(side=side, shapename=shapename, switch_on=False)

def switch_demo_given_side(side):
  label = shape_switcher[side].value_selected
  switch_demo(side=side, shapename=active_shapename[side] , switch_on=False)
  switch_demo(side=side, shapename=label, switch_on=True)
  active_shapename[side] = label
  plt.draw()

def switch_demo_left(label):
  switch_demo_given_side(side='left')
def switch_demo_right(label):
  switch_demo_given_side(side='right')

shape_switcher['left'].on_clicked(switch_demo_left)
#shape_switcher['right'].on_clicked(switch_demo_right)

switch_demo_left(shape_switcher['left'].value_selected)
#switch_demo_right(shape_switcher['right'].value_selected)

fig.set_dpi(my_default_demo_dpi) 
fig.set_size_inches(my_default_demo_figsize)
plt.show()