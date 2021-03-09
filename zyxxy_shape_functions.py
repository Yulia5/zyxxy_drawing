
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
                     'a_square' : ['left', 'bottom']} 

def get_diamond_label(shapename, original_label=None):
  if isinstance(shapename, str):   
    if shapename in bespoke_diamonds:
      result = bespoke_diamonds[shapename]
    else:
      result = 'centre'
  else:
    result = 'diamond'

  if original_label is not None:
    if isinstance(result, str):
      result += '_' + original_label[-1]
    else:
      if original_label == 'diamond_x':
        result = result[0]
      elif original_label == 'diamond_y':
        result = result[1]
      else:
        raise Exception(original_label, "is not a recognised diamond label")
  return result

def get_common_kwargs(kwargs, shapename):
  common_keys = {key : key for key in common_params_dict_definition.keys() if not key.startswith('diamond_')}
  common_keys['diamond_x'] = get_diamond_label(shapename=shapename, original_label='diamond_x')
  common_keys['diamond_y'] = get_diamond_label(shapename=shapename, original_label='diamond_y')
  used_keys = []
  common_kwargs = {}
  for key, value in common_keys.items():
    if value in kwargs:
      common_kwargs[key] = kwargs[value]
      used_keys.append(value)
  return used_keys, common_kwargs

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

  kwargs_common = {}
  if isinstance(shapename, str):
    admissible_shape_args = [k for k in zyxxy_coordinates.shape_names_params_dicts_definition[shapename].keys()]
    if shapename == "a_rectangle":
      admissible_shape_args += ['left', 'right', 'bottom', 'top']
    kwargs_shape = {key : value for key, value in kwargs.items() if key in admissible_shape_args}
    param_names_used += [k for k in kwargs_shape.keys()]
    _shape.update_xy_by_shapename(shapename=shapename, **kwargs_shape)
  else:
    _shape.update_xy_by_shapename(shapename=shapename)

  used_common_keys, kwargs_common = get_common_kwargs(kwargs=kwargs, shapename=shapename)
  _shape.move(**kwargs_common)
  param_names_used += used_common_keys

  raise_Exception_if_not_processed(kwarg_keys=kwargs.keys(), allowed_keys=param_names_used)
  
  return _shape

# code for three special draw_* functions
def draw_a_rectangle(width, height, left=None, centre_x=None, right=None, bottom=None, centre_y=None, top=None, ax=None, **kwargs):
  contour = zyxxy_coordinates.build_a_rectangle(width=width, height=height, 
    left=left, centre_x=centre_x, right=right, bottom=bottom, centre_y=centre_y, top=top)
  result = draw_a_shape(ax=ax, shapename=contour, shapetype="patch", **kwargs)
  return result

def draw_a_broken_line(contour, ax=None, **kwargs):
  _shape = draw_a_shape(ax=ax, shapename=contour, shapetype="line", **kwargs)
  return _shape

def draw_a_polygon(contour, ax=None, **kwargs):
  _shape = draw_a_shape(ax=ax, shapename=contour, shapetype="patch", **kwargs)
  return _shape

# autogenerate all other draw_* functions
for shapename in zyxxy_coordinates.shape_names_params_dicts_definition.keys():
  if shapename != "a_rectangle":
    globals()["draw_" + shapename] = partial(draw_a_shape, shapename=shapename)