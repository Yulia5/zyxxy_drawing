
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
from zyxxy_shapes_base import Shape
import zyxxy_coordinates
from zyxxy_shapes_colour_style import set_fill_in_outline_kwarg_defaults

common_params_dict_definition = {'stretch_x' : 'stretch',
                                 'stretch_y' : 'stretch',
                                 'turn' : 'turn',
                                 'diamond_x' : 'half_width', 
                                 'diamond_y' : 'half_height'}


shape_names_params_dicts_definition = {
                            'a_segment' : {'length': 'half_min_size'},               
                            'a_triangle': {'width' : 'half_min_size', 'height' : 'half_min_size'}, 
                            'a_square': {'side' : 'half_min_size'}, 
                            'a_rectangle': {'width' : 'half_min_size', 'height' : 'half_min_size'}, 
                            'a_rhombus' : {'width' : 'half_min_size', 'height' : 'half_min_size'},
                            'a_circle': {'radius' : 'half_min_size'},
                            'an_ellipse': {'width' : 'half_min_size', 'height' : 'half_min_size'}, 
                            'an_arc' : {'angle_start' : ['turn', full_turn_angle/4], 'angle_end' : ['turn', full_turn_angle/2], 'radius' : 'half_min_size'},
                            'an_elliptic_drop': {'width' : 'half_min_size', 'height' : 'half_min_size_34'},
                            'a_smile': {'width' : 'half_min_size', 'depth' : 'plus_minus_half_min_size'},
                            'a_star': {'ends_qty' : 'vertices', 'radius_1' : 'half_min_size_34', 'radius_2' : 'half_min_size'},
                            'a_regular_polygon': {'radius' : 'half_min_size', 'vertices_qty' : 'vertices'},
                            'an_eye': {'width' : 'half_min_size', 'depth_1' : ['plus_minus_half_min_size', -2], 'depth_2' : ['plus_minus_half_min_size', 2]},
                            'a_heart': {'angle_top_middle' : ['quarter_turn', 3], 'tip_addon' : 'stretch'},
                            'an_egg' : {'power' : ['vertices', 3], 'height_widest_point': ['half_height', 3], 'width' : ['half_width', 4], 'height' : ['half_height', 5]},
                            'a_sector': {'angle_start' : 'turn', 'angle_end' : ['double_turn', 3], 'radius_1' : 'half_min_size', 'radius_2' : 'half_min_size_34'},
                            'a_zigzag' : {'width': 'half_min_size', 'height': 'half_min_size', 'angle_start': 'turn', 'nb_segments': 'vertices'},
                            'a_wave' : {'width': 'half_min_size', 'height': 'half_min_size', 'angle_start': 'turn', 'nb_waves': 'vertices'},
                            'a_coil' : {'angle_start' : 'turn', 'nb_turns' : ['stretch', 3], 'speed_x' : 'stretch', 'speed_out' : ['stretch', 1.2]},
                            'an_arc_multispeed': {'angle_start' : ['turn', 0], 'angle_end' : ['double_turn', 24], 'speed_x' : ['stretch', 3], 'width' : 'half_width', 'height' : 'half_height'}}

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

def get_diamond_alias(shapename):
  return {get_diamond_label(shapename=shapename, original_label='diamond_x') : 'diamond_x',
          get_diamond_label(shapename=shapename, original_label='diamond_y') : 'diamond_y'}


def draw_a_shape(ax, is_patch_not_line, shapename, **kwargs):
  # get colour params
  colour_etc_kwargs = set_fill_in_outline_kwarg_defaults(kwargs=kwargs)

  # create a shape
  _shape = Shape(ax=ax, **colour_etc_kwargs)
  _shape.set_visible(val=is_patch_not_line)
  

  kwargs_common = {}
  if isinstance(shapename, str):
    kwargs_shape = {}
    _shape.update_given_shapename(shapename=shapename, kwargs_shape=kwargs_shape, kwargs_common=kwargs_common)
  else:
    _shape.update_xy_given_contour(contour=shapename)
    _shape.move(**kwargs_common)
  
  return _shape

def draw_a_rectangle(width, height, left=None, centre_x=None, right=None, bottom=None, centre_y=None, top=None, ax=None, **kwargs):
  contour = zyxxy_coordinates.build_a_rectangle(width=width, height=height, 
    left_x=left, centre_x=centre_x, right_x=right, bottom_y=bottom, centre_y=centre_y, top_y=top)
  result = draw_a_shape(ax=ax, shapename=contour, is_patch_not_line=True, **kwargs)
  return result

def draw_a_broken_line(contour, ax=None, **kwargs):
  draw_a_shape(ax=ax, shapename=contour, is_patch_not_line=False, **kwargs)

def draw_a_patch(contour, ax=None, **kwargs):
  draw_a_shape(ax=ax, shapename=contour, is_patch_not_line=True, **kwargs)