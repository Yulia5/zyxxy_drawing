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

import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons, CheckButtons
import numpy as np
import functools

from zyxxy_utils import full_turn_angle
from zyxxy_canvas import create_canvas_and_axes
from zyxxy_shape_class import Shape
from zyxxy_shape_style import joinstyle_types, capstyle_types
from zyxxy_coordinates import shape_names_params_dicts_definition, get_type_given_shapename
from zyxxy_shape_functions import common_params_dict_definition, get_diamond_label
from MY_zyxxy_demo_SETTINGS import figure_params, widget_params, patch_colours, line_colours, my_default_demo_colours

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

# variables that will be populated later
sides = ['left', 'right']
shape_types = ["patch", "line"]

active_shapename = {side : None for side in sides}
shapes_by_side_by_shapetype = {side : {st : None for st in shape_types} for side in sides}
common_widgets_by_side_by_shapetype = {side : {st : {} for st in shape_types} for side in sides}
specific_widgets_by_side_by_shapename = {side : {} for side in sides}
style_widgets_side_by_shapetype = {side : {st : {'text' : []} for st in shape_types} for side in sides}

##########################################################################################
# create the figure
fig = plt.figure()
fig.set_dpi(figure_params['dpi']) 
fig.set_size_inches(figure_params['figsize'])

##########################################################################################
# widget-creating functions
##########################################################################################

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

def add_a_slider2(sax, w_caption, s_vals, caption_in_the_same_line=True, **slider_qwargs):
  new_bottom = sax.get_position().ymin

  label = w_caption if caption_in_the_same_line else ""
  result = Slider(ax=sax, label=label, valmin=s_vals[0], valmax=s_vals[1], valinit=s_vals[2], valstep=s_vals[3], **slider_qwargs)

  if caption_in_the_same_line:
    added_text = None
  else:
    added_text = fig.text(w_left, new_bottom, w_caption)
    new_bottom += widget_params['height'] + widget_params['gap']

  return new_bottom, result, added_text

def add_a_slider(w_left, w_bottom, w_caption, s_vals, caption_in_the_same_line=True, **slider_qwargs):
  new_bottom, sax = get_axes_for_widget(w_left=w_left, 
                                        w_bottom=w_bottom)
  return add_a_slider2(sax, w_caption, s_vals, caption_in_the_same_line=True, **slider_qwargs)

def resize_1_checkbox(a_checkbox, left, bottom, width, height):
  r = a_checkbox.rectangles[0]
  r.set_x(left)
  r.set_y(bottom)
  r.set_width(width)
  r.set_height(height)

  l = a_checkbox.lines[0]
  l[0].set_data([left, left+width], [bottom+height, bottom])
  l[1].set_data([left, left+width], [bottom, bottom+height])

def get_value(a_widget):
  if isinstance(a_widget, Slider):
    return a_widget.val
  if isinstance(a_widget, CheckButtons):
    return a_widget.get_status()[0]
  if isinstance(a_widget, RadioButtons):
    return a_widget.value_selected
  raise Exception(type(a_widget), "is not handled")

##########################################################################################
def get_active_shapetype():
  shapetype = get_type_given_shapename(shapename=active_shapename[side])
  return shapetype

##########################################################################################
def update_shape_style_given_side(_, side):
  shapetype = get_active_shapetype()
  style_widgets = style_widgets_side_by_shapetype[side][shapetype]
  kwargs_style = {key : get_value(style_widgets[key]) for key in style_widgets.key() if key != 'text'}
  _shape.set_style(**kwargs_style)

##########################################################################################
def update_shape_form_given_side(_, side):

  shapename = active_shapename[side]
  shapetype = get_type_given_shapename(shapename)

  _shape = shapes_by_side_by_shapetype[side][shapetype]

  _sliders_specific = specific_widgets_by_side_by_shapename[side][shapename]
  kwargs_shape = {key : _sliders_specific[key].val for key in _sliders_specific.keys()}
  _shape.update_xy_by_shapename(shapename, **kwargs_shape)

  _widgets_common = common_widgets_by_side_by_shapetype[side][shapetype]
  kwargs_common= {key : get_value(_widgets_common[key]) for key in _widgets_common.key()}
  _shape.move(**kwargs_common)

  plt.draw()

##########################################################################################
def update_visibility(side, switch_on):
  shapename = active_shapename[side]

  #shape visibility
  _shape = shapes_by_side_by_shapetype[side][get_active_shapetype()]
  _shape.set_visible(switch_on)  

  # shape-specific form widgets visibility
  for _s in specific_widgets_by_side_by_shapename[side][shapename].values():
    _s.ax.set_visible(switch_on)

  # style widgets visibility
  patch_or_line = get_active_shapetype()
  for key, sw_or_all_texts in style_widgets_side_by_shapetype[side][patch_or_line].items():
    if key == "text":
      for t in sw_or_all_texts:
        t.set_visible(switch_on)
    else:
      sw_or_all_texts.ax.set_visible(switch_on)

##########################################################################################
def switch_active_shapename_given_side(label, side):

  update_visibility(side=side, switch_on=False)
  active_shapename[side] = label
  update_visibility(side=side, switch_on=True)

  # update diamond labels
  for diam_name in ["diamond_x", "diamond_y"]:
    shape_specific_label = get_diamond_label(shapename=active_shapename[side], original_label=diam_name)
    common_widgets_by_side_by_shapetype[side][active_shapename[side]][diam_name].set_caption(shape_specific_label)

  update_shape_form_given_side(side=side)
  plt.draw()

##########################################################################################
def reset(event, side):
  for w in specific_widgets_by_side_by_shapename[active_shapename[side]].values():
    w.reset()
  for w in common_widgets_by_side_by_shapetype.values():
    if isinstance(w, Slider):
      w.reset()
    elif isinstance(w, CheckButtons):
      if w.get_status()[0]:
        w.set_active(index=0)
    else:
      raise Exception(type(w), "type not recognized")

##########################################################################################

# create shapename radio buttons
# finding the max number of widgets
max_widget_qty = 0
for spec_param_dict in shape_names_params_dicts_definition.values():
  max_widget_qty = max(max_widget_qty, len(spec_param_dict))
demo_rax_bottom = (max_widget_qty + len(common_params_dict_definition) + 2) * (widget_params['height'] + widget_params['gap']) + figure_params['plot_bottom_gap']


# create shapestyle widgets
bottoms = {side : {st : figure_params['plot_bottom_gap'] for st in style_widgets_side_by_shapetype[side].keys()} for side in sides}
lefts = {'left' : {'line' : widget_params['radio_side_margin'] + 0.00001, 
                   'patch' : widget_params['radio_side_margin']},
         'right' : {'line' : 1 - widget_params['radio_width'] - widget_params['radio_side_margin'] + 0.00001, 
                    'patch' : 1 - widget_params['radio_width'] - widget_params['radio_side_margin']}}

def add_style_widget(side, patch_or_line, caption, func_name, **other_kwargs):
  bottoms[side][patch_or_line], style_widgets_side_by_shapetype[side][patch_or_line][caption], added_text = func_name(
                                                                           w_left=lefts[side][patch_or_line], 
                                                                           w_bottom=bottoms[side][patch_or_line], 
                                                                           w_caption=caption,
                                                                           **other_kwargs)
  if added_text is not None:
    style_widgets_side_by_shapetype[side][patch_or_line]['text'].append(added_text)

  
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

for side in sides:

  # placing the shapes_by_side_by_shapetype
  shape_colour = my_default_demo_colours[side]["shape"]   
  diamond_colour = my_default_demo_colours[side]["diamond"] 
  for st in shape_types:                                          
    _shape = Shape(ax=ax, is_patch_not_line=(st == "patch"), defaults_for_demo=True)
    _shape.set_style(colour=shape_colour, diamond_colour=diamond_colour)
    shapes_by_side_by_shapetype[side][st] = _shape

  # adding style widgets
  default_widget_width = widget_params['radio_width']
  for st in style_widgets_side_by_shapetype[side].keys():
    add_style_widget(side=side, patch_or_line=st, caption="layer_nb", func_name=add_a_slider, s_vals=[0, 3, 1, 1], caption_in_the_same_line=False)
    add_style_widget(side=side, patch_or_line=st, caption="joinstyle", func_name=add_radio_buttons, rb_options=joinstyle_types)
  add_style_widget(side=side, patch_or_line="line", caption="capstyle", func_name=add_radio_buttons, rb_options=capstyle_types)
  add_style_widget(side=side, patch_or_line="patch", caption="colour", func_name=add_radio_buttons, rb_options=patch_colours) 
  add_style_widget(side=side, patch_or_line="line", caption="colour", func_name=add_radio_buttons, rb_options=line_colours)
  add_style_widget(side=side, patch_or_line="patch", caption="outline_colour", func_name=add_radio_buttons, rb_options=line_colours)
  for patch_or_line, caption in {"line" : "linewidth", "patch" : "outline_linewidth"}.items():
    add_style_widget(side=side, patch_or_line=patch_or_line, caption=caption, func_name=add_a_slider, s_vals=[0, 10, 1, 1], caption_in_the_same_line=False)
  add_style_widget(side=side, patch_or_line="patch", caption="opacity", func_name=add_a_slider, s_vals=[0, 1, 1, 0.1], caption_in_the_same_line=False)

  # adding shapename switchers
  default_widget_width = widget_params['radio_width']
  rax_left = widget_params['radio_side_margin'] * 2 + widget_params['radio_width']
  if side != 'left':
    rax_left = 1 - widget_params['radio_width'] - rax_left
  _, shape_switcher_side, _ = add_radio_buttons(rb_options=shape_names_params_dicts_definition.keys(), w_left=rax_left, w_bottom=demo_rax_bottom, w_caption="shapenames")
  # shape_switcher_side.activecolor = my_default_demo_colours[side]["shape"]
  shape_switcher_side.on_clicked(functools.partial(switch_active_shapename_given_side, side=side) )

  # adding common form parameters sliders 
  default_widget_width = widget_params['width']
  
  new_bottom = figure_params['plot_bottom_gap']
  w_left =  figure_params['widget_lefts'][side]

  new_bottom, b_axes = get_axes_for_widget(w_bottom=new_bottom, w_left=w_left)
  button = Button(ax=b_axes, label='Reset')
  button.on_clicked(functools.partial(reset, side=side))

  for param_name, slider_range_name in common_params_dict_definition.items():
    new_bottom, w_axes = get_axes_for_widget(w_bottom=new_bottom, w_left=w_left)
    _, c_slider, _ = add_a_slider2(w_axes,
                                   w_caption=param_name, 
                                   s_vals=np.copy(slider_range[slider_range_name]), 
                                   color=my_default_demo_colours[side]["shape"])
    c_slider.on_changed(functools.partial(update_shape_form_given_side, side=side))
    common_widgets_by_side_by_shapetype[param_name] = c_slider  

  start_bottom_for_specific, w_axes = get_axes_for_widget(w_bottom=new_bottom, w_left=w_left)
  flip_checkbox = CheckButtons(w_axes, ('flip_upside_down', ), (False, ))
  resize_1_checkbox(a_checkbox=flip_checkbox, left=0.05, bottom=0.15, width=0.05, height=0.7)
  flip_checkbox.on_clicked(functools.partial(update_shape_form_given_side, side=side))
  common_widgets_by_side_by_shapetype['flip'] = flip_checkbox

  # ... and specific sliders
  for sh_counter, shapename in enumerate(shape_names_params_dicts_definition.keys()):
    specific_widgets_by_side_by_shapename[side][shapename] = {}
    w_left = figure_params['widget_lefts'][side] + sh_counter * 0.0001
    param_counter = -1
    for param_name, param_name_range in shape_names_params_dicts_definition[shapename].items():
      param_counter += 1
      if isinstance(param_name_range, str):
        param_params = np.copy(slider_range[param_name_range])
      else:
        param_params = np.copy(slider_range[param_name_range[0]]) 
        param_params[2] = param_name_range[1] 
   
      w_bottom = (widget_params['height']+widget_params['gap'])*param_counter+ figure_params['plot_bottom_gap']
      _, s_slider, _ = add_a_slider(w_left=w_left,
                                              w_bottom=w_bottom,
                                              w_caption=param_name, 
                                              s_vals=param_params, 
                                              color=my_default_demo_colours[side]["shape"])
      s_slider.on_changed(functools.partial(update_shape_form_given_side, side=side))

      specific_widgets_by_side_by_shapename[side][shapename][param_name] = s_slider

  # ... and update the visibility !
  for shapename in shape_names_params_dicts_definition.keys():
    active_shapename[side] = shapename
    update_visibility(side=side, switch_on=False)
  switch_active_shapename_given_side(label="a_circle", side=side)
  

##########################################################################################

plt.show()