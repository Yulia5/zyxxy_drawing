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
from zyxxy_shape_style import joinstyle_types, capstyle_types
from zyxxy_coordinates import zyxxy_line_shapes, shape_names_params_dicts_definition
from zyxxy_shape_functions import common_params_dict_definition, get_diamond_label
from MY_zyxxy_demo_SETTINGS import figure_params, widget_params, patch_colours, line_colours, my_default_demo_colours

import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons, CheckButtons
import numpy as np

plt.rcParams.update({'font.size': figure_params['font_size']})

canvas_width  = figure_params['canvas_width']
canvas_height = figure_params['canvas_height']
half_min_size = min(canvas_width, canvas_height)/2

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

# finding the max number of widgets
MAX_WIDGET_QTY = 0
for spec_param_dict in shape_names_params_dicts_definition.values():
  if MAX_WIDGET_QTY < len(spec_param_dict):
    MAX_WIDGET_QTY = len(spec_param_dict)
MAX_WIDGET_QTY += len(common_params_dict_definition) + 1

# variables that will be populated later
sides = ['left', 'right']
all_shapenames = shape_names_params_dicts_definition.keys()

shapes_by_side_by_shapename = {side : {key : None for key in all_shapenames} for side in sides}
widgets_by_side_by_shapename = {side : {key : {} for key in all_shapenames} for side in sides}
active_shapename = {side : None for side in sides}


shape_switcher = {}
style_widgets = {side : {"patch" : {'text' : []}, "line" : {'text' : []}} for side in sides}


# create the figure
fig = plt.figure()
default_widget_width = None

def get_axes_for_widget(w_left, w_bottom, w_height=widget_params['height']):
  wax = plt.axes([w_left, w_bottom, default_widget_width, w_height]) 
  fig.add_axes(wax)
  new_bottom = w_height + w_bottom + widget_params['gap']
  return new_bottom, wax

def add_radio_buttons(w_left, w_bottom, w_caption, rb_options):
  new_bottom, rax = get_axes_for_widget(w_left=w_left, 
                                        w_bottom=w_bottom, 
                                        w_height=widget_params['height']*len(rb_options))
  result = RadioButtons(rax, rb_options, active=1)

  added_text = fig.text(w_left, new_bottom, w_caption)
  new_bottom += widget_params['height'] + widget_params['gap']

  return new_bottom, result, added_text

def add_a_slider(w_left, w_bottom, w_caption, s_vals, caption_in_the_same_line=True, **slider_qwargs):
  new_bottom, sax = get_axes_for_widget(w_left=w_left, 
                                        w_bottom=w_bottom)
  label = w_caption if caption_in_the_same_line else ""
  result = Slider(ax=sax, label=label, valmin=s_vals[0], valmax=s_vals[1], valinit=s_vals[2], valstep=s_vals[3], **slider_qwargs)

  if caption_in_the_same_line:
    added_text = None
  else:
    added_text = fig.text(w_left, new_bottom, w_caption)
    new_bottom += widget_params['height'] + widget_params['gap']

  return new_bottom, result, added_text

# create shapename radio buttons
demo_rax_bottom = (MAX_WIDGET_QTY + 1) * (widget_params['height'] + widget_params['gap']) + figure_params['plot_bottom_gap']

default_widget_width = widget_params['radio_width']

for side in sides:
  rax_left = widget_params['radio_side_margin'] * 2 + widget_params['radio_width']
  if side != 'left':
    rax_left = 1 - widget_params['radio_width'] - rax_left
  _, shape_switcher[side], _ = add_radio_buttons(rb_options=all_shapenames, w_left=rax_left, w_bottom=demo_rax_bottom, w_caption="shapenames")
  # shape_switcher[side].activecolor = my_default_demo_colours[side]["shape"]

# create shapestyle widgets
bottoms = {side : {st : figure_params['plot_bottom_gap'] for st in style_widgets[side].keys()} for side in sides}
lefts = {'left' : {'line' : widget_params['radio_side_margin'] + 0.00001, 
                   'patch' : widget_params['radio_side_margin']},
         'right' : {'line' : 1 - widget_params['radio_width'] - widget_params['radio_side_margin'] + 0.00001, 
                    'patch' : 1 - widget_params['radio_width'] - widget_params['radio_side_margin']}}

def add_style_widget(side, patch_or_line, caption, func_name, **other_kwargs):
  bottoms[side][patch_or_line], style_widgets[side][patch_or_line][caption], added_text = func_name(
                                                                           w_left=lefts[side][patch_or_line], 
                                                                           w_bottom=bottoms[side][patch_or_line], 
                                                                           w_caption=caption,
                                                                           **other_kwargs)
  if added_text is not None:
    style_widgets[side][patch_or_line]['text'].append(added_text)

default_widget_width = widget_params['radio_width']
                                                                
for side in sides:
  for st in style_widgets[side].keys():
    add_style_widget(side=side, patch_or_line=st, caption="joinstyle", func_name=add_radio_buttons, rb_options=joinstyle_types)
  add_style_widget(side=side, patch_or_line="line", caption="capstyle", func_name=add_radio_buttons, rb_options=capstyle_types)
  add_style_widget(side=side, patch_or_line="patch", caption="colour", func_name=add_radio_buttons, rb_options=patch_colours) 
  add_style_widget(side=side, patch_or_line="line", caption="colour", func_name=add_radio_buttons, rb_options=line_colours)
  add_style_widget(side=side, patch_or_line="patch", caption="outline_colour", func_name=add_radio_buttons, rb_options=line_colours)
  for patch_or_line, caption in {"line" : "linewidth", "patch" : "outline_linewidth"}.items():
    add_style_widget(side=side, patch_or_line=patch_or_line, caption=caption, func_name=add_a_slider, s_vals=[0, 10, 1, 1], caption_in_the_same_line=False)
  add_style_widget(side=side, patch_or_line="patch", caption="opacity", func_name=add_a_slider, s_vals=[0, 1, 1, 0.1], caption_in_the_same_line=False)
  
# Creating the canvas!
plot_ax_left  = 2 * (widget_params['radio_side_margin'] + widget_params['radio_width']) + figure_params['plot_gap']
plot_ax_bottom= demo_rax_bottom + figure_params['plot_bottom_gap']
ax = plt.axes([plot_ax_left, plot_ax_bottom, 1 - 2 * plot_ax_left, 1 - plot_ax_bottom])
fig.add_axes(ax)

create_canvas_and_axes(canvas_width=canvas_width,
                            canvas_height=canvas_height, 
                            tick_step=figure_params['tick_step'],
                            title="Try Out Shapes",
                            title_font_size=figure_params['font_size']*1.5,
                            axes_label_font_size=figure_params['font_size'],
                            axes_tick_font_size=figure_params['font_size'],
                            axes=ax)

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


def resize_1_checkbox(a_checkbox, left, bottom, width, height):
  r = a_checkbox.rectangles[0]
  r.set_x(left)
  r.set_y(bottom)
  r.set_width(width)
  r.set_height(height)

  l = a_checkbox.lines[0]
  l[0].set_data([left, left+width], [bottom+height, bottom])
  l[1].set_data([left, left+width], [bottom, bottom+height])

def get_left_bottom(counter):
  return {'w_left'   : figure_params['widget_lefts'][side] + count_shapes * 0.0001, 
          'w_bottom' : (widget_params['height']+widget_params['gap'])*counter+ figure_params['plot_bottom_gap']}

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

  shape_colour = my_default_demo_colours[side]["shape"]   
  diamond_colour = my_default_demo_colours[side]["diamond"]   

  flip_checkbox = None

  counter = MAX_WIDGET_QTY + 1

  sliders_specific = {}
  sliders_common = {}

  global default_widget_width
  default_widget_width = widget_params['width']

  for param_params_dict, target in ((shape_params_dict, sliders_specific), (common_params_dict, sliders_common)):
    for param_name, param_params in param_params_dict.items():
      counter -= 1
      
      if param_name.startswith("diamond"):
        colour = diamond_colour
        label = get_diamond_label(shapename=shapename, original_label=param_name)
      else:
        colour = shape_colour
        label = param_name      
      _, target[param_name], _ = add_a_slider(**get_left_bottom(counter),
                                              w_caption=label, 
                                              s_vals=param_params, 
                                              color=colour)
    if flip_checkbox is None:
      counter -= 1
      flip_checkbox = CheckButtons(get_axes_for_widget(**get_left_bottom(counter))[1], ('flip_upside_down', ), (False, ))
      resize_1_checkbox(a_checkbox=flip_checkbox, left=0.05, bottom=0.15, width=0.05, height=0.7)

  counter -= 1
  button = Button(ax=get_axes_for_widget(**get_left_bottom(counter))[1], label='Reset')

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

  patch_or_line = "line" if (shapename in zyxxy_line_shapes) else "patch"
  for key, sw_or_all_texts in style_widgets[side][patch_or_line].items():
    if key == "text":
      for t in sw_or_all_texts:
        t.set_visible(switch_on)
    else:
      sw_or_all_texts.ax.set_visible(switch_on)


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

fig.set_dpi(figure_params['dpi']) 
fig.set_size_inches(figure_params['figsize'])
plt.show()