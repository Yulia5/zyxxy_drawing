
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

from zyxxy_shape_class import Shape
from functools import partial
import zyxxy_coordinates
from zyxxy_shape_style import raise_Exception_if_not_processed, extract_colour_etc_kwargs

common_params_dict_definition = {'stretch_x' : 'stretch',
                                 'stretch_y' : 'stretch',
                                 'turn' : 'turn',
                                 'diamond_x' : 'half_width', 
                                 'diamond_y' : 'half_height'}

bespoke_diamonds = { 'a_coil' : 'start',
                     'a_wave' : 'start',
                     'a_segment' : 'start',
                     'a_zigzag' : 'start',
                     'a_heart' : 'tip',
                     'a_triangle' : 'tip',
                     'an_elliptic_drop' : 'tip',
                     'an_egg' : 'tip',
                     'a_square' : [['left', 'centre_x', 'right'], ['bottom', 'centre_y', 'top']],
                     'a_rectangle' : [['centre_x', 'left', 'right'], ['centre_y', 'bottom', 'top']]} 

def get_diamond_label(shapename, original_label=None, available_arguments=None):
  # get the first part of the label, without the axis
  if isinstance(shapename, str):   
    if shapename in bespoke_diamonds:
      result = bespoke_diamonds[shapename]
    else:
      result = 'centre'
  else:
    result = 'diamond'

  # modify the result by adding the axis based on original_label, or find the right label
  assert original_label in ['diamond_x', 'diamond_y']
  if isinstance(result, str): 
    result += '_' + original_label[-1]
    return result
  
  i1 = 0 if original_label == 'diamond_x' else 1
  if isinstance(result[0], str):
    return result[i1]
  
  # assume this is an array of arrays
  if available_arguments is None:
    return result[i1][0]
  else:
    intersection_arguments = [a for a in available_arguments if a in result[i1]]
    if len(intersection_arguments) == 0:
      raise Exception("Among the arguments provided,", available_arguments, "there are no suitable candidates,", result[i1])
    if len(intersection_arguments) > 1:
      raise Exception("In the arguments provided,", available_arguments, "there is more than one suitable candidate,", result[i1])
    return intersection_arguments[0]

def draw_a_shape(ax, shapename, **kwargs):
  param_names_used = []
  # create a shape
  if isinstance(shapename, str):
    shapetype = zyxxy_coordinates.get_type_given_shapename(shapename=shapename)
  else:
    shapetype = kwargs['shapetype']
    param_names_used += ['shapetype']

  _shape = Shape(ax=ax, shapetype=shapetype)

  # get colour params
  colour_etc_kwargs = extract_colour_etc_kwargs(kwargs)
  _shape.set_style(**colour_etc_kwargs)
  param_names_used += [k for k in colour_etc_kwargs.keys()]

  
  if isinstance(shapename, str):
    admissible_shape_args = [k for k in zyxxy_coordinates.shape_names_params_dicts_definition[shapename].keys()]
    kwargs_shape = {key : value for key, value in kwargs.items() if key in admissible_shape_args}
    param_names_used += [k for k in kwargs_shape.keys()]
    _shape.update_xy_by_shapename(shapename=shapename, **kwargs_shape)
  else:
    _shape.update_xy_by_shapename(shapename=shapename)

  # adjust the diamond
  _shape.adjust_the_diamond(**kwargs)

  # apply common arguments
  def get_common_kwargs(kwargsss):
    common_keys = {key : key for key in common_params_dict_definition.keys() if not key.startswith('diamond_')}
    for dk in ['diamond_x', 'diamond_y']:
      common_keys[dk] = get_diamond_label(shapename=shapename, original_label=dk, available_arguments=kwargs.keys())
  
    used_keys = []
    common_kwargs = {}
    for key, value in common_keys.items():
      if value in kwargsss.keys():
        common_kwargs[key] = kwargsss[value]
        used_keys.append(value)
    return used_keys, common_kwargs

  kwargs_common = {}
  used_common_keys, kwargs_common = get_common_kwargs(kwargsss=kwargs)
  _shape.move(**kwargs_common)
  param_names_used += used_common_keys

  if 'clip_outline' in kwargs:
    _shape.clip(clip_outline=kwargs['clip_outline'])
    param_names_used.append('clip_outline')

  raise_Exception_if_not_processed(kwarg_keys=kwargs.keys(), allowed_keys=param_names_used)
  
  return _shape

# code for four special draw_* functions
def __draw_a_rectangle(width, height, left=None, centre_x=None, right=None, bottom=None, centre_y=None, top=None, ax=None, **kwargs):
  contour, diamond = zyxxy_coordinates.build_a_rectangle_and_its_diamond(width=width, height=height, 
    left=left, centre_x=centre_x, right=right, bottom=bottom, centre_y=centre_y, top=top)
  result = draw_a_shape(ax=ax, shapename=contour, shapetype="patch", diamond_x=diamond[0], diamond_y=diamond[1], **kwargs)
  return result

def __draw_a_square(side, **kwargs):
  result = __draw_a_rectangle(width=side, height=side, **kwargs)
  return result

def draw_a_broken_line(contour, ax=None, **kwargs):
  _shape = draw_a_shape(ax=ax, shapename=contour, shapetype="line", **kwargs)
  return _shape

def draw_a_polygon(contour, ax=None, **kwargs):
  _shape = draw_a_shape(ax=ax, shapename=contour, shapetype="patch", **kwargs)
  return _shape

# autogenerate all other draw_* functions
for shapename in zyxxy_coordinates.shape_names_params_dicts_definition.keys():
  #if shapename not in ["a_rectangle", "a_square"]:
    globals()["draw_" + shapename] = partial(draw_a_shape, shapename=shapename)