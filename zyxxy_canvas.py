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

from zyxxy_shape_style import set_diamond_size_factor, set_outlines_colour, find_colour_code
from zyxxy_shape_class import get_all_polygons_in_layers
from zyxxy_external_images import filename_to_image, show_image
from zyxxy_utils import is_running_tests
from MY_zyxxy_SETTINGS import my_default_font_sizes, my_default_display_params, my_default_image_params, my_default_animation_params

# create the axis, set their sizes, 
# add the grid and ticks if needed
def create_canvas_and_axes(canvas_width,
                           canvas_height,
                           make_symmetric = False,
                           tick_step = None,
                           background_colour = 'none',
                           title = None,
                           title_font_size = my_default_font_sizes['title'],
                           axes_label_font_size = my_default_font_sizes['axes_label'],
                           axes_tick_font_size = my_default_font_sizes['tick'],
                           figsize = my_default_display_params['max_figsize'],
                           dpi = my_default_display_params['dpi'],
                           margin_adjustments = my_default_display_params['margin_adjustments'],
                           axes = None,
                           model = None,
                           outlines_colour = None):

  # helper function to make sure the ticks are in the right place
  def get_round_multiple_range(min_, max_, step):
    _sign = -1 if min_ < 0 else 1
    min_multiple = _sign * floor(abs(min_/step)) * abs(step)
    result = np.arange(min_multiple, max_, step)
    return result

  assert make_symmetric in ['x', 'y', True, False]

  if make_symmetric in ['x', True]:
    left_x, right_x = -canvas_width/2, canvas_width/2
  else:
    left_x, right_x = 0, canvas_width
  if make_symmetric in ['y', True]: 
    bottom_y, top_y = -canvas_height/2, canvas_height/2
  else:
    bottom_y, top_y = 0, canvas_height

  all_axes = []
  if axes is None:
    if model is None:
      _, axes = plt.subplots()
      all_axes.append(axes)
    else:
      if True:
        _, axs = plt.subplots(1, 2)
      else:
        _, axs = plt.subplots(2, 1)
      all_axes += [axs[0], axs[1]]
      axes = axs[0]

  for a_ in all_axes:
    a_.grid(tick_step is not None)
    if tick_step is not None:
      a_.set_xlabel("RULER FOR X's", fontsize=axes_label_font_size)
      a_.set_ylabel("RULER FOR Y's", fontsize=axes_label_font_size)
      a_.tick_params(axis='both', which='major', labelsize=axes_tick_font_size)
      a_.set_xticks(ticks = get_round_multiple_range(left_x, right_x, tick_step))
      a_.set_yticks(ticks = get_round_multiple_range(bottom_y, top_y, tick_step))
    else:
      a_.set_xticks(ticks = [])
      a_.set_yticks(ticks = [])
    # set axis limits
    a_.set_aspect('equal')
    a_.set_xlim(left=left_x, right=right_x)
    a_.set_ylim(bottom=bottom_y, top=top_y)

  if tick_step is None:
    axes.set_facecolor(find_colour_code(background_colour))
  
  if model is not None:
    # handle the model drawing
    if isinstance(model, str):
      model_title = "Original Drawing"
      image = filename_to_image(filename=model)
      scaling_factor = min(canvas_width/image.shape[1], canvas_height/image.shape[0])
      # defining LB_position to center the model image
      LB_position=[left_x   + 0.5 * (canvas_width  - image.shape[1] * scaling_factor), 
                   bottom_y + 0.5 * (canvas_height - image.shape[0] * scaling_factor)]
      # placing the image
      show_image(ax=axs[1], prepared_image=image, origin=[0, 0], zorder=0, scaling_factor=scaling_factor,  LB_position=LB_position)  
    else:
      model(axes=axs[1]) 
      model_title = "Completed Drawing"

    if True:
      
      margin_adjustments['left'] /= 2.
      margin_adjustments['right'] = (1 + margin_adjustments['right']) / 2.
    else:
      
      margin_adjustments['bottom'] /= 2.
      margin_adjustments['top'] = (1 + margin_adjustments['top']) / 2.

    axs[1].set_title(model_title, fontdict={'size': title_font_size})
    if outlines_colour is not None and model is not None and not isinstance(model, str):
      set_outlines_colour(outlines_colour)
      set_diamond_size_factor(0)
      model(axes=axes)
      axes.set_title("") # remove the title if needed
      set_outlines_colour(None)

  axes.set_title(title, fontdict={'size': title_font_size})

  # show diamond points and grid and axis if and only if tick_step is set
  set_diamond_size_factor(value=(tick_step is not None))

  plt.subplots_adjust(**margin_adjustments)
  figure = plt.gcf()
  figure.set_dpi(dpi) 
  figure.set_size_inches(figsize)

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
                           figsize4saving = my_default_image_params['figsize'],
                           dpi4saving = my_default_image_params['dpi'],
                           image_format = my_default_image_params['format'],
                           animation_file_figsize = my_default_animation_params['figsize'],
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
  current_figsize = figure.get_size_inches()

  if (animation_func is None) != (nb_of_frames is None):
    raise Exception("Either both animation_func and nb_of_frames, or none, should be specified.")
  if animation_func is None:
    if (filename is not None) and (filename != ""):
      last_dot_position = filename.rfind(".")
      if last_dot_position < 0:
        filename += '.' + image_format
        last_dot_position = filename.rfind(".")
      figure.set_size_inches(figsize4saving)
      plt.savefig(fname="images_videos/"+filename, 
                  format = filename[last_dot_position+1:],
                  dpi = dpi4saving)
  else:
    figure.set_dpi(animation_file_dpi) 
    figure.set_size_inches(animation_file_figsize)
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
  figure.set_size_inches(current_figsize)
  if not is_running_tests():
    plt.show(block=block)