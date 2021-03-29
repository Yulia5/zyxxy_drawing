
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
import matplotlib.pyplot as plt


def draw_a_shape(shapename, ax=None, **kwargs):
  if ax is None:
    ax = plt.gcf().gca() # get current axes

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
  used_common_keys = _shape.move(**kwargs)
  param_names_used += used_common_keys

  if 'clip_outline' in kwargs:
    _shape.clip(clip_outline=kwargs['clip_outline'])
    param_names_used.append('clip_outline')

  raise_Exception_if_not_processed(kwarg_keys=kwargs.keys(), allowed_keys=param_names_used)
  
  return _shape

def clone_a_shape(init_shape):
   _shape = Shape(init_shape=init_shape)
   return _shape

# code for two special draw_* functions
def draw_a_broken_line(contour, ax=None, **kwargs):
  _shape = draw_a_shape(ax=ax, shapename=contour, shapetype="line", **kwargs)
  return _shape

def draw_a_polygon(contour, ax=None, **kwargs):
  _shape = draw_a_shape(ax=ax, shapename=contour, shapetype="patch", **kwargs)
  return _shape

# autogenerate all other draw_* functions
for shapename in zyxxy_coordinates.shape_names_params_dicts_definition.keys():
  globals()["draw_" + shapename] = partial(draw_a_shape, shapename=shapename)