
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

from zyxxy_shapes_base import Shape
from functools import partial
import zyxxy_coordinates
from zyxxy_shapes_colour_style import set_fill_in_outline_kwarg_defaults, raise_Exception_if_not_processed

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

def _get_diamond_label(shapename):
  if isinstance(shapename, str):
    for key, value in bespoke_diamonds.items():
      if key == shapename:
        return value
    return 'centre'
  return 'diamond'

def get_diamond_label(shapename, original_label=None):
  result = _get_diamond_label(shapename=shapename)
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

def draw_a_shape(ax, is_patch_not_line, shapename, **kwargs):
  # get colour params
  param_names_used_colour, colour_etc_kwargs = set_fill_in_outline_kwarg_defaults(kwargs=kwargs)
  param_names_used = param_names_used_colour

  # create a shape
  _shape = Shape(ax=ax, **colour_etc_kwargs)
  _shape.set_visible(val=is_patch_not_line)

  kwargs_common = {}
  if isinstance(shapename, str):
    kwargs_shape = {key : value for key, value in kwargs.items() if key in zyxxy_coordinates.shape_names_params_dicts_definition[shapename].keys()}
    param_names_used += [k for k in kwargs_shape.keys()]
    _shape.update_xy_by_shapename(shapename=shapename, **kwargs_shape)
  else:
    _shape.update_xy_given_contour(contour=shapename)

  used_common_keys, kwargs_common = get_common_kwargs(kwargs=kwargs, shapename=shapename)
  _shape.move(**kwargs_common)
  param_names_used += used_common_keys

  raise_Exception_if_not_processed(kwarg_keys=kwargs.keys(), processed_keys=param_names_used)
  
  return _shape

def draw_a_rectangle(width, height, left=None, centre_x=None, right=None, bottom=None, centre_y=None, top=None, ax=None, **kwargs):
  contour = zyxxy_coordinates.build_a_rectangle(width=width, height=height, 
    left_x=left, centre_x=centre_x, right_x=right, bottom_y=bottom, centre_y=centre_y, top_y=top)
  result = draw_a_shape(ax=ax, shapename=contour, is_patch_not_line=True, **kwargs)
  return result

def draw_a_broken_line(contour, ax=None, **kwargs):
  draw_a_shape(ax=ax, shapename=contour, is_patch_not_line=False, **kwargs)

def draw_a_polygon(contour, ax=None, **kwargs):
  draw_a_shape(ax=ax, shapename=contour, is_patch_not_line=True, **kwargs)

for shapename in zyxxy_coordinates.shape_names_params_dicts_definition.keys():
  if shapename == "a_rectangle":
    pass
  is_patch_not_line = not (shapename in zyxxy_coordinates.zyxxy_line_shapes)
  globals()["draw_" + shapename] = partial(
      draw_a_shape,
      shapename=shapename,
      is_patch_not_line=is_patch_not_line,
    )