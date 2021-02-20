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

from zyxxy_utils import full_turn_angle
from zyxxy_canvas import create_canvas_and_axes
from functools import partial
from zyxxy_shape_class import Shape
from zyxxy_coordinates import zyxxy_line_shapes, shape_names_params_dicts_definition
from zyxxy_shape_functions import common_params_dict_definition, get_diamond_label
from MY_zyxxy_SETTINGS import my_default_demo_canvas_size, my_default_demo_figsize, my_default_demo_dpi, my_default_demo_tick_step, my_default_demo_radio_width, my_default_demo_widget_height, my_default_demo_radio_side_margin, my_default_demo_widget_gap, my_default_demo_plot_gap, my_default_demo_plot_bottom_gap, my_default_demo_font_size, my_default_demo_colours

import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons, CheckButtons
import numpy as np

plt.rcParams.update({'font.size': my_default_demo_font_size})

canvas_width = my_default_demo_canvas_size[0]
canvas_height = my_default_demo_canvas_size[1]
half_min_size = min(canvas_width, canvas_height) * 0.5

slider_range = {'half_min_size' : [0., half_min_size, int(half_min_size/2), 1],
                'plus_minus_half_min_size' : [-half_min_size, half_min_size, int(half_min_size/2), .1],
                'half_min_size_34' : [0., half_min_size, int(half_min_size*3/4), 1],
                'half_width'   : [0., canvas_width, int(canvas_width/2), 1],
                'half_height'  : [0., canvas_height, int(canvas_height/2), 1],
                'stretch'      : [0., 5, 1, 0.1],
                'turn'         : [0, full_turn_angle, 0, full_turn_angle/12],
                'double_turn'  : [0, 2*full_turn_angle, 0, full_turn_angle/12],
                'long_turn'    : [0, 5*full_turn_angle, 0, full_turn_angle/4],
                'half_turn'    : [0, full_turn_angle/2, 0, full_turn_angle/12],
                'quarter_turn' : [0, full_turn_angle/4, 0, full_turn_angle/12],
                'vertices'     : [1, 12, 5, 1],}

widget_lefts = {'left': 0.15, 'right' : 0.65}
#clip?

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

demo_rax_bottom = (MAX_WIDGET_QTY + 1) * (my_default_demo_widget_height + my_default_demo_widget_gap) + my_default_demo_plot_bottom_gap
# create the figure and the radio buttons
both_rax_x_left = {'left' : my_default_demo_radio_side_margin, 'right' : (1 - my_default_demo_radio_side_margin - my_default_demo_radio_width)}
shape_switcher = {}
colour_switcher = {}
fig = plt.figure()
for side, rax_x_left in both_rax_x_left.items():
  bottom_y = demo_rax_bottom
  for options, switcher in [[shape_names_params_dicts_definition.keys(), shape_switcher]]:
    rax = plt.axes([rax_x_left, bottom_y, my_default_demo_radio_width, my_default_demo_widget_height*len(options)])
    fig.add_axes(rax)
    switcher[side] = RadioButtons(rax, options, active=1)
    switcher[side].activecolor = my_default_demo_colours[side]["shape"]
    bottom_y += my_default_demo_widget_height * (len(options) + 0.2)
  
# Creating the canvas!

big_axes_width = 1-2*(my_default_demo_radio_width + my_default_demo_radio_side_margin+my_default_demo_plot_gap)
ax = plt.axes([my_default_demo_radio_side_margin+my_default_demo_radio_width+my_default_demo_plot_gap, demo_rax_bottom+my_default_demo_plot_bottom_gap, big_axes_width, 1-demo_rax_bottom-my_default_demo_plot_bottom_gap])
fig.add_axes(ax)

create_canvas_and_axes(canvas_width=my_default_demo_canvas_size[0],
                            canvas_height=my_default_demo_canvas_size[1], 
                            tick_step=my_default_demo_tick_step,
                            title="Try Out Shapes",
                            title_font_size = my_default_demo_font_size*1.5,
                            axes_label_font_size = my_default_demo_font_size,
                            axes_tick_font_size = my_default_demo_font_size,
                            ax=ax)

def update_given_shapename_and_side(side, shapename):
  global shapes_by_side_by_shapename
  global widgets_by_side_by_shapename
  _shape = shapes_by_side_by_shapename[side][shapename]
  _widgets = widgets_by_side_by_shapename[side][shapename]
  _sliders_specific = _widgets['sliders_specific']
  _sliders_common = _widgets['sliders_common']

  kwargs_shape = {key:_sliders_specific[key].val for key in _sliders_specific.keys()}
  kwargs_common= {key:_sliders_common[key].val for key in ['turn', 'stretch_x', 'stretch_y', 'diamond_x', 'diamond_y']}
  kwargs_common['flip'] = _widgets['flip_checkbox'].get_status()[0]
  _shape.update_xy_by_shapename(shapename, **kwargs_shape)
  _shape.move(**kwargs_common)
  plt.draw()

def get_axes_for_widget(counter, widget_left):
  return plt.axes([widget_left, (my_default_demo_widget_height + my_default_demo_widget_gap )*counter + my_default_demo_plot_bottom_gap, 0.3, my_default_demo_widget_height])

def resize_1_checkbox(a_checkbox, left, bottom, width, height):
  r = a_checkbox.rectangles[0]
  r.set_x(left)
  r.set_y(bottom)
  r.set_width(width)
  r.set_height(height)

  l = a_checkbox.lines[0]
  l[0].set_data([left, left+width], [bottom+height, bottom])
  l[1].set_data([left, left+width], [bottom, bottom+height])

def place_shapes_and_widgets(side, shapename, count_shapes):
  this_shape_params_definition = shape_names_params_dicts_definition[shapename]
  shape_params_dict = {}
  for key, value in this_shape_params_definition.items():
    if isinstance(value, str):
      shape_params_dict[key] = np.copy(slider_range[value])
    else:
      shape_params_dict[key] = np.copy(slider_range[value[0]]) 
      shape_params_dict[key][2] = value[1]

  common_params_dict = {key:np.copy(slider_range[value]) for key, value in common_params_dict_definition.items()}

  _get_w_axes = partial(get_axes_for_widget, 
                        widget_left = widget_lefts[side] + count_shapes * 0.0001)
                           # this tiny adjustment is needed to avoid a matplotlib glitch

  shape_colour = my_default_demo_colours[side]["shape"]   
  diamond_colour = my_default_demo_colours[side]["diamond"]   

  flip_checkbox = None

  counter = MAX_WIDGET_QTY + 1
  sliders_specific = {}
  sliders_common = {}
  for param_params_dict, target in ((shape_params_dict, sliders_specific), (common_params_dict, sliders_common)):
    for param_name, param_params in param_params_dict.items():
      counter -= 1
      if param_name.startswith("diamond"):
        colour = diamond_colour
        label = get_diamond_label(shapename=shapename, original_label=param_name)
      else:
        colour = shape_colour
        label = param_name      
      target[param_name] = Slider(ax=_get_w_axes(counter), label=label, valmin=param_params[0], valmax=param_params[1], valinit=param_params[2], valstep=param_params[3], color=colour)
    if flip_checkbox is None:
      counter -= 1
      flip_checkbox = CheckButtons(_get_w_axes(counter), ('flip_upside_down', ), (False, ))
      resize_1_checkbox(a_checkbox=flip_checkbox, left=0.05, bottom=0.15, width=0.05, height=0.7)

  counter -= 1
  button = Button(ax=_get_w_axes(counter), label='Reset')

  widgets_by_side_by_shapename[side][shapename] = {'sliders_specific': sliders_specific, 
                                                   'flip_checkbox' : flip_checkbox,
                                                   'sliders_common': sliders_common, 
                                                   'button': button}
                                            
  _shape = Shape(ax=ax, is_patch_not_line=(shapename not in zyxxy_line_shapes), defaults_for_demo=True)
  _shape.set_style(colour=shape_colour, diamond_colour=diamond_colour)
  shapes_by_side_by_shapename[side][shapename] = _shape
    
  def update(val):
    update_given_shapename_and_side(side=side, shapename=shapename)

  def reset(event):
    for _slider in ([v for v in sliders_specific.values()] + [v for v in sliders_common.values()]):
      _slider.reset()
    if flip_checkbox.get_status()[0]:
      flip_checkbox.set_active(index=0)

  for _slider in ([v for v in sliders_specific.values()] + [v for v in sliders_common.values()]):
    _slider.on_changed(update)

  flip_checkbox.on_clicked(update)
  button.on_clicked(reset)

def switch_demo(side, shapename, switch_on):
  if shapename is None:
    return
  _shape = shapes_by_side_by_shapename[side][shapename]
  _shape.set_visible(switch_on)

  # widgets
  _widgets = widgets_by_side_by_shapename[side][shapename]
  all_widgets = [_widgets['button'], _widgets['flip_checkbox']] + [v for v in _widgets['sliders_specific'].values()] + [v for v in _widgets['sliders_common'].values()]
  for _s in all_widgets:
    _s.ax.set_visible(switch_on)

for side in ['left', 'right']:
  count_shapes = 0
  for shapename in shape_names_params_dicts_definition.keys():
    place_shapes_and_widgets(side=side, shapename=shapename, count_shapes=count_shapes)
    count_shapes += 1

def switch_demo_given_side(side):
  label = shape_switcher[side].value_selected
  switch_demo(side=side, shapename=active_shapename[side], switch_on=False)
  switch_demo(side=side, shapename=label, switch_on=True)
  active_shapename[side] = label
  plt.draw()

def switch_demo_left(label):
  switch_demo_given_side(side='left')
def switch_demo_right(label):
  switch_demo_given_side(side='right')

for side, func in [['left', switch_demo_left], ['right', switch_demo_right]]:
  for shapename in shape_names_params_dicts_definition.keys():
    update_given_shapename_and_side(side=side, shapename=shapename)
    switch_demo(side=side, shapename=shapename, switch_on=False)
  switch_demo_given_side(side=side)
  shape_switcher[side].on_clicked( func )

fig.set_dpi(my_default_demo_dpi) 
fig.set_size_inches(my_default_demo_figsize)
plt.show()