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

import numpy as np
from functools import partial
from math import floor
from matplotlib import animation
import matplotlib.pyplot as plt
import numpy as np

from zyxxy_shape_style import set_diamond_size_factor, set_outlines_colour, find_colour_code
from zyxxy_shape_class import get_all_polygons_in_layers
from zyxxy_external_images import filename_to_image, show_image
from zyxxy_utils import is_running_tests
from MY_zyxxy_SETTINGS import my_default_font_sizes, my_default_display_params, my_default_image_params, my_default_animation_params

def __prepare_axes(ax, canvas_width,
                       canvas_height, make_symmetric, axes_label_font_size, axes_tick_font_size, tick_step, background_colour):

  assert make_symmetric in ['x', 'y', True, False]

  # helper function to make sure the ticks are in the right place
  def get_round_multiple_range(min_, max_, step):
    if step is None:
      return []
    _sign = -1 if min_ < 0 else 1
    min_multiple = _sign * floor(abs(min_/step)) * abs(step)
    result = np.arange(min_multiple, max_, step)
    return result

  if make_symmetric in ['x', True]:
    left_x, right_x = -canvas_width/2, canvas_width/2
  else:
    left_x, right_x = 0, canvas_width
  if make_symmetric in ['y', True]: 
    bottom_y, top_y = -canvas_height/2, canvas_height/2
  else:
    bottom_y, top_y = 0, canvas_height

  ax.grid(tick_step is not None)
  if tick_step is None:
    ax.set_facecolor(find_colour_code(background_colour))
  else:
    ax.set_xlabel("RULER FOR X's", fontsize=axes_label_font_size)
    ax.set_ylabel("RULER FOR Y's", fontsize=axes_label_font_size)
    ax.tick_params(axis='both', which='major', labelsize=axes_tick_font_size)

  ax.set_xticks(ticks = get_round_multiple_range(left_x, right_x, tick_step))
  ax.set_yticks(ticks = get_round_multiple_range(bottom_y, top_y, tick_step))
  # set axis limits
  ax.set_xlim(left=left_x, right=right_x)
  ax.set_ylim(bottom=bottom_y, top=top_y)
  ax.set_aspect('equal')
    

# create the axis, set their sizes, 
# add the grid and ticks if needed
def create_canvas_and_axes(canvas_width,
                           canvas_height,
                           make_symmetric = False,
                           tick_step = None,
                           background_colour = 'none',
                           axes_label_font_size = my_default_font_sizes['axes_label'],
                           axes_tick_font_size = my_default_font_sizes['tick'],
                           title = "",
                           title_font_size = my_default_font_sizes['title'],
                           max_figsize = my_default_display_params['max_figsize'],
                           dpi = my_default_display_params['dpi'],
                           default_margin_adjustments = my_default_display_params['margin_adjustments'],
                           axes = None,
                           model = None,
                           outlines_colour = None):

  params_for_axes = {  'canvas_width'         : canvas_width,
                       'canvas_height'        : canvas_height, 
                       'make_symmetric'       : make_symmetric,
                       'tick_step'            : tick_step, 
                       'background_colour'    : background_colour, 
                       'axes_label_font_size' : axes_label_font_size, 
                       'axes_tick_font_size'  : axes_tick_font_size}

  if axes is not None:
    __prepare_axes(ax=axes, **params_for_axes)
    return axes

  margin_adjustments = {key:value for key, value in default_margin_adjustments.items() if key!='ticks'}
  if tick_step is not None:
    margin_adjustments['left']   += default_margin_adjustments['ticks']
    margin_adjustments['bottom'] += default_margin_adjustments['ticks']
  
  scale_horizontal = (margin_adjustments['right'] - margin_adjustments['left']) * max_figsize[0] / canvas_width
  scale_vertical = (margin_adjustments['top'] - margin_adjustments['bottom']) * max_figsize[1] / canvas_height
  figsize = max_figsize
  if model is not None:
      # decide if the model should be below (vertical) or to the right (horizontal) of the working axes
      scale_if_V_placement = min(scale_vertical/2, scale_horizontal)
      scale_if_H_placement = min(scale_vertical, scale_horizontal/2)

      place_model_H_not_V = (scale_if_H_placement > scale_if_V_placement)
      
      if place_model_H_not_V:
        figsize[1] *= scale_if_V_placement/scale_if_H_placement
        margin_adjustments['left'] /= 2.
        margin_adjustments['right'] = (1 + margin_adjustments['right']) / 2.
      else:
        figsize[0] *= scale_if_H_placement/scale_if_V_placement
        margin_adjustments['bottom'] /= 2.
        margin_adjustments['top'] = (1 + margin_adjustments['top']) / 2.

  else:
      if scale_horizontal < scale_vertical:
        figsize[1] *= scale_horizontal / scale_vertical
      else:
        figsize[0] *= scale_vertical / scale_horizontal

  spa = [] if model is None else ([1, 2] if place_model_H_not_V else [2, 1])
  figure, axs = plt.subplots(*spa)
  axes = axs if not isinstance(axs, np.ndarray) else axs[0]
  
  figure.subplots_adjust(**margin_adjustments)
  figure.set_dpi(dpi) 
  figure.set_size_inches(figsize)

  __prepare_axes(ax=axes, **params_for_axes)
  
  if model is not None:
    # handle the model drawing
    if isinstance(model, str):
      __prepare_axes(ax=axs[1], **params_for_axes)
      model_title = "Original Drawing"
      image = filename_to_image(filename=model)
      scaling_factor = min(canvas_width/image.shape[1], canvas_height/image.shape[0])
      # defining LB_position to center the model image
      LB_position=[axs[1].get_xticks()[0] + 0.5 * (canvas_width  - image.shape[1] * scaling_factor), 
                   axs[1].get_yticks()[0] + 0.5 * (canvas_height - image.shape[0] * scaling_factor)]
      # placing the image
      show_image(ax=axs[1], prepared_image=image, origin=[0, 0], zorder=0, scaling_factor=scaling_factor,  LB_position=LB_position)  
    else:
      model(axes=axs[1]) 
      model_title = "Completed Drawing"
      if outlines_colour is not None:
        set_outlines_colour(outlines_colour)
        set_diamond_size_factor(0)
        model(axes=axes)
        set_outlines_colour(None)
    axs[1].set_title(model_title, fontdict={'size': title_font_size})

  axes.set_title(title, fontdict={'size': title_font_size})

  # show diamond points and grid and axis if and only if tick_step is set
  set_diamond_size_factor(value=(tick_step is not None))

  return axes

# this function shows the drawing 
# and saves if as a file if requested
# more information in the document below
# https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.savefig.html#matplotlib.pyplot.savefig 

# assumes that there is only one set of axes - to be reviewed

def default_animation_init():
  # return the list of the shapes that are moved by animation
  return get_all_polygons_in_layers()

def envelope_animate(i, anim_func):
  result = anim_func(i)
  if result is not None:
    return result
  # return the list of the shapes that are moved by animation
  return get_all_polygons_in_layers()

def show_drawing_and_save_if_needed(filename=None,
                           dpi4saving = my_default_image_params['dpi'],
                           image_format = my_default_image_params['format'],
                           animation_file_dpi = my_default_animation_params['dpi'],
                           animation_interval = my_default_animation_params['interval'],
                           animation_blit = my_default_animation_params['blit'],
                           animation_repeat = my_default_animation_params['repeat'],
                           animation_FPS = my_default_animation_params['FPS'],
                           animation_writer = my_default_animation_params['writer'],
                           animation_format = my_default_animation_params['format'],
                           animation_func = None,
                           animation_init = default_animation_init,
                           nb_of_frames = None,
                           block=True):
  figure = plt.gcf()
  current_dpi = figure.get_dpi() 

  if (animation_func is None) != (nb_of_frames is None):
    raise Exception("Either both animation_func and nb_of_frames, or none, should be specified.")
  if animation_func is None:
    if (filename is not None) and (filename != ""):
      last_dot_position = filename.rfind(".")
      if last_dot_position < 0:
        filename += '.' + image_format
        last_dot_position = filename.rfind(".")
      plt.savefig(fname="images_videos/"+filename, 
                  format = filename[last_dot_position+1:],
                  dpi = dpi4saving)
  else:
    figure.set_dpi(animation_file_dpi) 
    # writer = animation.writers[animation_writer](fps=animation_FPS)
    writer = animation.FFMpegWriter(fps=animation_FPS) 
    anim = animation.FuncAnimation( fig=figure, 
                                    func=partial(envelope_animate, anim_func=animation_func), 
                                    init_func=animation_init,  
                                    frames=nb_of_frames, 
                                    interval=animation_interval,
                                    blit=animation_blit, 
                                    repeat=animation_repeat)
    if (filename is not None) and (filename != ""):
      anim.save("images_videos/"+filename+'.'+animation_format, writer=writer)
      return
  figure.set_dpi(current_dpi) 

  if not is_running_tests():
    plt.show(block=block)