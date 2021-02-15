
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

def build_a_shape(ax, shapename, shapetype, **kwargs):
  colour_etc_kwargs = {}
  _shape = Shape(ax=ax, **colour_etc_kwargs)
  _shape.set_visible(val)
  kwargs_shape = {}
  kwargs_common = {}
  _shape.update_given_shapename(shapename=shapename, kwargs_shape=kwargs_shape, kwargs_common=kwargs_common)


def draw_given_shapename(ax, is_patch, shapename, kwargs_shape, kwargs_common, **kwargs):
  new_shape = Shape(ax=ax, is_patch=is_patch, **kwargs)
  new_shape.update_given_shapename(shapename=shapename, kwargs_shape=kwargs_shape, kwargs_common=kwargs_common)
  return new_shape

def draw_given_contour(ax, is_patch, contour, diamond, stretch_x, stretch_y, turn, **kwargs):
  new_shape = Shape(ax=ax, is_patch=is_patch, **kwargs)
  new_shape.update_xy_given_contour(contour=contour)
  new_shape.shift(shift=diamond)
  new_shape.stretch(stretch_x=stretch_x, stretch_y=stretch_y)
  new_shape.rotate(turn=turn)
  return new_shape

def draw_a_rectangle(ax, width, height, left_x=None, centre_x=None, right_x=None, bottom_y=None, centre_y=None, top_y=None, **kwargs):
  #zyxxy_coordinates.build_a_rectangle
  diamond_best_guess, contour = Shape(  width=width, height=height, 
    left_x=left_x, centre_x=centre_x, right_x=right_x, bottom_y=bottom_y, centre_y=centre_y, top_y=top_y)
  draw_given_contour(ax=ax, is_patch=True, contour=contour, diamond_x=diamond_best_guess[0], diamond_y=diamond_best_guess[1], stretch_x=1.0, stretch_y=1.0, turn=0, **kwargs)

def draw_broken_line(contour, ax=None, diamond=None, stretch_x=1.0, stretch_y=1.0, turn=0, **kwargs):
  draw_given_contour(ax=ax, is_patch=False, contour=contour, diamond=diamond, stretch_x=stretch_x, stretch_y=stretch_y, turn=turn, **kwargs)