
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

from zyxxy_shape_class import Shape, get_all_shapes_in_layers
from functools import partial
import zyxxy_coordinates
from zyxxy_shape_style import raise_Exception_if_not_processed, get_admissible_style_arguments
import matplotlib.pyplot as plt

########################################################################
def draw_a_shape(shapename, ax=None, **kwargs):
  param_names_used = []
  # create a shape
  if isinstance(shapename, str):
    shapetype = zyxxy_coordinates.get_type_given_shapename(shapename=shapename)
  else:
    shapetype = kwargs['shapetype']
    param_names_used += ['shapetype']

  _shape = Shape(ax=ax, shapetype=shapetype)

  allowed_keys = ['clip_outline', 'shapetype']

  # get colour params
  admissible_style_arguments = get_admissible_style_arguments(shapetype=shapetype)
  allowed_keys += admissible_style_arguments
  colour_etc_kwargs = {k:v for k, v in kwargs.items() if k in admissible_style_arguments}
  _shape.set_style(**colour_etc_kwargs)
  
  if isinstance(shapename, str):
    admissible_shape_args = [k for k in zyxxy_coordinates.shape_names_params_dicts_definition[shapename].keys()]
    allowed_keys += admissible_shape_args
    kwargs_shape = {key : value for key, value in kwargs.items() if key in admissible_shape_args}
    _shape.update_xy_by_shapename(shapename=shapename, **kwargs_shape)
  else:
    _shape.update_xy_by_shapename(shapename=shapename)



  # apply common arguments
  common_keys_for_shape = zyxxy_coordinates.get_common_keys_for_shape(
        shapename=shapename, 
        available_arguments=kwargs)
  kwargs_common = {key : value for key, value in kwargs.items() if key in common_keys_for_shape.values()}
  allowed_keys += [v for v in common_keys_for_shape.values()]

  # move
  _shape.move(**kwargs_common)

  if 'clip_outline' in kwargs:
    _shape.clip(clip_outline=kwargs['clip_outline'])
    param_names_used.append('clip_outline')

  raise_Exception_if_not_processed(kwarg_keys=kwargs.keys(), allowed_keys=allowed_keys)
  
  return _shape

########################################################################
def clone_a_shape(init_shape):
   _shape = Shape(init_shape=init_shape)
   return _shape

########################################################################
# code for two special draw_* functions
def draw_a_broken_line(contour, ax=None, **kwargs):
  for c in ['x', 'y']:
    if 'diamond_'+c not in kwargs:
      kwargs['diamond_'+c] = 0.

  _shape = draw_a_shape(ax=ax, shapename=contour, shapetype="line", **kwargs)
  return _shape

def draw_a_polygon(contour, ax=None, **kwargs):
  for c in ['x', 'y']:
    if 'diamond_'+c not in kwargs:
      kwargs['diamond_'+c] = 0.

  _shape = draw_a_shape(ax=ax, shapename=contour, shapetype="patch", **kwargs)
  return _shape

########################################################################
# autogenerate all other draw_* functions
for shapename in zyxxy_coordinates.shape_names_params_dicts_definition.keys():
  globals()["draw_" + shapename] = partial(draw_a_shape, shapename=shapename)

########################################################################
# handling shapes per layers
########################################################################
def shift_layers(shift, layer_nbs=[]):
  _shapes = get_all_shapes_in_layers(*layer_nbs)
  for shape in _shapes:
    shape.shift(shift=shift)

########################################################################
def turn_layers(turn, diamond, layer_nbs=[]):
  _shapes = get_all_shapes_in_layers(*layer_nbs)
  for shape in _shapes:
    shape.rotate(turn=turn, diamond_override=diamond)

########################################################################
def stretch_layers(diamond, stretch_x=1., stretch_y=1., layer_nbs=[]):
  _shapes = get_all_shapes_in_layers(*layer_nbs)
  for shape in _shapes:
    shape.stretch(diamond_override=diamond, stretch_x=stretch_x, stretch_y=stretch_y)