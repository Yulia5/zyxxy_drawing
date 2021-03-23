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
import functools, inspect

from zyxxy_utils import full_turn_angle
from zyxxy_canvas import create_canvas_and_axes, is_running_tests
from zyxxy_shape_class import Shape
from zyxxy_coordinates import shape_names_params_dicts_definition, get_type_given_shapename
from zyxxy_shape_functions import common_params_dict_definition, get_diamond_label
from MY_zyxxy_SETTINGS import my_default_colour_etc_settings
from MY_zyxxy_demo_SETTINGS import figure_params, widget_params, demo_style_widgets_value_ranges, my_default_demo_shapes, my_default_demo_style

from zyxxy_shape_style import joinstyle_types, capstyle_types
demo_style_widgets_value_ranges["joinstyle"] = joinstyle_types
demo_style_widgets_value_ranges["capstyle"] = capstyle_types

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
common_widgets_by_side = {side : {} for side in sides}
specific_widgets_by_side = {side : [] for side in sides}                    # slider objects
specific_widgets_values_by_side_by_shapename= {side : {} for side in sides} # current values
specific_inputs_values_by_shapename = {}                                    # min, max etc. params

style_widgets_side_by_shapetype = {side : {st : {'text' : []} for st in shape_types} for side in sides}
shape_switchers = {side : None for side in sides}
buttons = {side : None for side in sides}

##########################################################################################
def fill_in_specific_inputs_values_by_shapename_widgets_values_by_side_by_shapename():
  global specific_inputs_values_by_shapename
  global specific_widgets_values_by_side_by_shapename
  # specific sliders # todo
  for shapename, shape_params in shape_names_params_dicts_definition.items():
    specific_inputs_values_by_shapename[shapename] = {}
    for side in sides:
        specific_widgets_values_by_side_by_shapename[side][shapename] = {}
    for param_name, param_name_range in shape_params.items():

      if isinstance(param_name_range, str):
        param_params = np.copy(slider_range[param_name_range])
      else:
        param_params = np.copy(slider_range[param_name_range[0]]) 
        param_params[2] = param_name_range[1] 

      specific_inputs_values_by_shapename[shapename][param_name] = {'valmin' : param_params[0], 
                                                                    'valmax' : param_params[1], 
                                                                    'valinit' : param_params[2], 
                                                                    'valstep' : param_params[3]}
      for side in sides:
        specific_widgets_values_by_side_by_shapename[side][shapename][param_name] = param_params[2]

fill_in_specific_inputs_values_by_shapename_widgets_values_by_side_by_shapename()

##########################################################################################
# create the figure
fig = plt.figure()
##########################################################################################
# Creating the canvas!
##########################################################################################

def get_max_specific_sliders():
  max_specific_sliders = 0
  for spec_param_dict in shape_names_params_dicts_definition.values():
    max_specific_sliders = max(max_specific_sliders, len(spec_param_dict))
  return max_specific_sliders

def get_demo_rax_bottom():
  max_widget_qty = get_max_specific_sliders() + len(common_params_dict_definition) + 2
  demo_rax_bottom = max_widget_qty * (widget_params['height'] + widget_params['gap']) 
  demo_rax_bottom += figure_params['plot_bottom_gap']
  return demo_rax_bottom

plot_ax_left   = 2 * (widget_params['radio_side_margin'] + widget_params['radio_width']) + figure_params['plot_gap']
plot_ax_bottom = get_demo_rax_bottom() + figure_params['plot_bottom_gap']
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


##########################################################################################
# widget-creating functions
##########################################################################################

default_widget_width = None

def get_axes_for_widget(w_left, w_bottom, w_height=widget_params['height']):
  wax = plt.axes([w_left, w_bottom, default_widget_width, w_height]) 
  #fig.add_axes(wax)
  new_bottom = w_height + w_bottom + widget_params['gap']
  return new_bottom, wax

def add_radio_buttons(w_left, w_bottom, w_caption, rb_options, active_option):
  
  new_bottom, rax = get_axes_for_widget(w_left=w_left, 
                                        w_bottom=w_bottom, 
                                        w_height=widget_params['height']*len(rb_options))

  #rax.set_aspect('auto')

  active = 1 if active_option is None else rb_options.index(active_option)
  result = RadioButtons(rax, rb_options, active=active, activecolor='black')

  added_text = fig.text(w_left, new_bottom, w_caption)
  new_bottom += widget_params['height'] + widget_params['gap']

  for circle in result.circles: # adjust radius here. The default is 0.05
    pass # circle.set_radius(widget_params['height']/2.)

  return new_bottom, result, added_text

def add_a_slider(w_left, w_bottom, w_caption, s_vals, caption_in_the_same_line=True, **slider_qwargs):
  _, sax = get_axes_for_widget(w_left=w_left, 
                               w_bottom=w_bottom)
  label = w_caption if caption_in_the_same_line else ""
  result = Slider(ax=sax, label=label, valmin=s_vals[0], valmax=s_vals[1], valinit=s_vals[2], valstep=s_vals[3], color='black', **slider_qwargs)

  new_bottom = sax.get_position().ymax + widget_params['gap']
  if caption_in_the_same_line:
    added_text = None
  else:
    added_text = fig.text(sax.get_position().xmin, new_bottom, w_caption)
    new_bottom += widget_params['height'] + widget_params['gap']

  return new_bottom, result, added_text

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
def get_active_shapetype(side):
  shapetype = get_type_given_shapename(shapename=active_shapename[side])
  return shapetype

def get_active_shape(side):
  _shape = shapes_by_side_by_shapetype[side][get_active_shapetype(side=side)]
  return _shape

##########################################################################################
def get_common_kwarg_key(shapename, common_label):
  if common_label in ["diamond_x", "diamond_y"]:
    return get_diamond_label(shapename=shapename, original_label=common_label)
  return common_label

##########################################################################################
def update_shape_form_given_side(_, side):

  shapename = active_shapename[side]
  _shape = get_active_shape(side=side)

  kwargs_shape = {silder_.label : silder_.val for silder_ in specific_widgets_by_side[side] if silder_.ax.get_visible()}
  
  _widgets_common = common_widgets_by_side[side]
  kwargs_common= {key : get_value(_widgets_common[key]) for key in _widgets_common.keys()}
  kwargs_common2= {get_common_kwarg_key(shapename=shapename, common_label=key) : value for key, value in kwargs_common.items()}

  _shape.update_xy_by_shapename(active_shapename[side], **kwargs_shape)
  _shape.adjust_the_diamond(**kwargs_common2)
  _shape.move(**kwargs_common)

  fig.canvas.draw_idle()


#specific_widgets_by_side = {side : [] for side in sides}                    # slider objects
#specific_widgets_values_by_side_by_shapename= {side : {} for side in sides} # current values
#specific_inputs_values_by_shapename = {}  # min, max etc. params

##########################################################################################
def update_visibility(side, switch_on):

  #shape visibility
  _shape = shapes_by_side_by_shapetype[side][get_active_shapetype(side=side)]
  _shape.set_visible(switch_on)

  spec_param_dict = specific_inputs_values_by_shapename[active_shapename[side]]
  current_slider_nb = 0
  
  for param_name, slider_params in spec_param_dict.items():
    current_slider_nb -= 1
    current_slider = specific_widgets_by_side[side][current_slider_nb]
    current_slider.ax.set_visible(switch_on)
    if switch_on:
      for attr_name, attr_value in spec_param_dict[param_name].items():
        setattr(current_slider, attr_name, attr_value)
      current_slider.val = specific_widgets_values_by_side_by_shapename[side][active_shapename[side]][param_name]
      current_slider.label = param_name  
    else:
      specific_widgets_values_by_side_by_shapename[side][active_shapename[side]][param_name] = current_slider.val
    
  for i in range(get_max_specific_sliders() + current_slider_nb):
    specific_widgets_by_side[side][i].ax.set_visible(False)
  

  # style widgets visibility
  patch_or_line = get_active_shapetype(side=side)
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
    common_widgets_by_side[side][diam_name].label.set_text(shape_specific_label)

  update_shape_form_given_side(None, side=side)
  fig.canvas.draw_idle()

##########################################################################################
def reset(_, side):
  for w in specific_widgets_by_side[side]:
    w.reset()
  for w in common_widgets_by_side[side].values():
    if isinstance(w, Slider):
      w.reset()
    elif isinstance(w, CheckButtons):
      if w.get_status()[0]:
        w.set_active(index=0)
    else:
      raise Exception(type(w), "type not recognized")

##################################################################################
# create shapestyle widgets  

def place_style_widgets(side, shapetype, arg_category, w_left, w_bottom):

  captions_init_values = my_default_demo_style[side][arg_category]
  if arg_category != 'diamond':
    for key, value in my_default_colour_etc_settings[arg_category].items():
      if key not in captions_init_values:
        captions_init_values[key] = value

  where_to_add =  style_widgets_side_by_shapetype[side][shapetype] # a shortcut
  for argname, init_value in captions_init_values.items():
    w_options = demo_style_widgets_value_ranges[argname]
    
    if not isinstance(w_options[0], str): 
      w_options[2] = init_value
      func_name = functools.partial(add_a_slider, s_vals=w_options, caption_in_the_same_line=False)
    else:
      func_name = functools.partial(add_radio_buttons, rb_options=w_options, active_option=init_value)

    prefixed_caption = argname if arg_category not in ["diamond", "outline"] else arg_category+"_"+argname
    w_bottom, where_to_add[prefixed_caption], added_text = func_name(w_left=w_left, w_bottom=w_bottom, w_caption=prefixed_caption)

    on_click_or_change = functools.partial(update_shape_style, side=side, shapetype=shapetype, argname=prefixed_caption)
    if isinstance(where_to_add[prefixed_caption], RadioButtons):
      where_to_add[prefixed_caption].on_clicked(on_click_or_change)
    elif isinstance(where_to_add[prefixed_caption], Slider):
      where_to_add[prefixed_caption].on_changed(on_click_or_change)

    if added_text is not None:
      where_to_add['text'].append(added_text)

  return w_bottom

##########################################################################################
def update_shape_style(_, side, shapetype, argname):
  argvalue = get_value(style_widgets_side_by_shapetype[side][shapetype][argname])
  style_kwargs = {argname : argvalue}
  shapes_by_side_by_shapetype[side][shapetype].set_style(**style_kwargs)
  fig.canvas.draw_idle()

##################################################################################
def place_shapes_and_widgets(side):
  # placing the shapes_by_side_by_shapetype
  shapes_by_side_by_shapetype[side] = {shapetype : Shape(ax=ax, shapetype=shapetype) for shapetype in shape_types}

  # adding style widgets
  global default_widget_width
  default_widget_width = widget_params['radio_width'] * .9
  w_left =  widget_params['radio_side_margin']
  if side == "right":
    w_left = 1 - widget_params['radio_width'] - widget_params['radio_side_margin']

  new_bottom = place_style_widgets( side=side, shapetype='line', arg_category='diamond', 
                                    w_left=w_left, 
                                    w_bottom=figure_params['plot_bottom_gap']+0.00001)

  _ = place_style_widgets(          side=side, shapetype='line', arg_category='line', 
                                    w_left=w_left, 
                                    w_bottom=new_bottom)
  

  new_bottom = place_style_widgets( side=side, shapetype='patch', arg_category='diamond', 
                                    w_left=w_left, 
                                    w_bottom=figure_params['plot_bottom_gap'])

  new_bottom = place_style_widgets( side=side, shapetype='patch', arg_category='outline', 
                                    w_left=w_left, 
                                    w_bottom=new_bottom)

  _          = place_style_widgets( side=side, shapetype='patch', arg_category='patch', 
                                    w_left=w_left, 
                                    w_bottom=new_bottom)


  # adding shapename switchers
  default_widget_width = widget_params['radio_width']
  rax_left = widget_params['radio_side_margin'] * 2 + widget_params['radio_width']
  if side != 'left':
    rax_left = 1 - widget_params['radio_width'] - rax_left
  _, shape_switchers[side], _ = add_radio_buttons(rb_options=[k for k in shape_names_params_dicts_definition.keys()], w_left=rax_left, w_bottom=get_demo_rax_bottom(), w_caption="shapenames", active_option=my_default_demo_shapes[side])

  shape_switchers[side].on_clicked(functools.partial(switch_active_shapename_given_side, side=side) )

  # adding common form parameters sliders 
  default_widget_width = widget_params['width']
  
  new_bottom = figure_params['plot_bottom_gap']
  w_left =  figure_params['widget_lefts'][side]

  new_bottom, b_axes = get_axes_for_widget(w_bottom=new_bottom, w_left=w_left)
  buttons[side] = Button(ax=b_axes, label='Reset')
  buttons[side].on_clicked(functools.partial(reset, side=side))
   
  _cpdd = [[key, value] for key, value in common_params_dict_definition.items()]
  for param_name, slider_range_name in _cpdd[::-1]:
    new_bottom, c_slider, _ = add_a_slider( w_bottom=new_bottom, w_left=w_left,
                                   w_caption=param_name, 
                                   s_vals=np.copy(slider_range[slider_range_name]))
    c_slider.on_changed(functools.partial(update_shape_form_given_side, side=side))
    common_widgets_by_side[side][param_name] = c_slider  

  start_bottom_for_specific, w_axes = get_axes_for_widget(w_bottom=new_bottom, w_left=w_left)
  flip_checkbox = CheckButtons(w_axes, ('flip_upside_down', ), (False, ))
  resize_1_checkbox(a_checkbox=flip_checkbox, left=0.05, bottom=0.15, width=0.05, height=0.7)
  flip_checkbox.on_clicked(functools.partial(update_shape_form_given_side, side=side))
  common_widgets_by_side[side]['flip'] = flip_checkbox

  # ... and specific sliders
  w_bottom = start_bottom_for_specific
  for s in range(get_max_specific_sliders()):
    w_bottom, s_slider, _ = add_a_slider(w_left=figure_params['widget_lefts'][side],
                                         w_bottom=w_bottom,
                                         w_caption="Dummy", #todo: add dummies
                                         s_vals=[0, 1, 1/2, 1/2])
    specific_widgets_by_side[side] += [s_slider]
    s_slider.on_changed(functools.partial(update_shape_form_given_side, side=side))

  # ... and style!
  for st in shape_types:
    style_widgets = style_widgets_side_by_shapetype[side][st]
    kwargs_style = {key : get_value(style_widgets[key]) for key in style_widgets.keys() if key != 'text'}
    shapes_by_side_by_shapetype[side][st].set_style(**kwargs_style)

  # Now switch off all the shapes' visibility
  for shapename in shape_names_params_dicts_definition.keys():
    active_shapename[side] = shapename
    update_visibility(side=side, switch_on=False)
 
  # ... and  switch on those that need to be active!
  switch_active_shapename_given_side(label=my_default_demo_shapes[side], side=side)
  

# placing the shapes and widgets
for side in sides:
  place_shapes_and_widgets(side=side)

fig.set_dpi(figure_params['dpi']) 
fig.set_size_inches(figure_params['figsize'])
if not is_running_tests():
  plt.show()