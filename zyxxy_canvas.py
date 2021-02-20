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
from matplotlib import animation
import matplotlib.pyplot as plt
from zyxxy_shape_style import set_diamond_style

from MY_zyxxy_SETTINGS import my_default_image_format,my_default_title_font_size,my_default_axes_label_font_size,my_default_axes_tick_font_size, my_default_figsize,my_default_dpi, my_default_image_file_figsize, my_default_image_file_dpi, my_default_margin_adjustments, my_default_animation_file_figsize, my_default_animation_file_dpi, my_default_animation_interval, my_default_animation_blit, my_default_animation_repeat, my_default_animation_FPS, my_default_background_settings

background_rectangle = None

def set_background_colour(new_background_colour):
  global background_rectangle
  if background_rectangle is not None:
    if new_background_colour is not None:
      background_rectangle.set_fc(new_background_colour)

# create the axis, set their sizes, 
# add the grid and ticks if needed
def create_canvas_and_axes(canvas_width,
                           canvas_height,
                           make_symmetric = False,
                           tick_step = None,
                           background_colour = None,
                           title = None,
                           title_font_size = my_default_title_font_size,
                           axes_label_font_size = my_default_axes_label_font_size,
                           axes_tick_font_size = my_default_axes_tick_font_size,
                           ax = None):
  global background_rectangle

  if ax is None:
    _, ax = plt.subplots()

  ax.set_title(title, fontdict={'size': title_font_size})

  if make_symmetric:
    left_x, right_x = -canvas_width/2, canvas_width/2
    bottom_y, top_y = -canvas_height/2, canvas_height/2
  else:
    left_x, right_x = 0, canvas_width
    bottom_y, top_y = 0, canvas_height

  # show diamond points and grid and axis if and only if tick_step is set
  set_diamond_style(show = (tick_step is not None))
  ax.grid(tick_step is not None)
  if tick_step is not None:
    ax.set_xlabel("RULER FOR X's", fontsize=axes_label_font_size)
    ax.set_ylabel("RULER FOR Y's", fontsize=axes_label_font_size)
    ax.tick_params(axis='both', which='major', labelsize=axes_tick_font_size)
    ax.set_xticks(ticks = np.arange(left_x, right_x, tick_step))
    ax.set_yticks(ticks = np.arange(bottom_y, top_y, tick_step))
  else:
    ax.set_xticks(ticks = [])
    ax.set_yticks(ticks = [])
    background_rectangle = plt.Polygon([[left_x, bottom_y], 
                                       [left_x+canvas_width, bottom_y], 
                                       [left_x+canvas_width, bottom_y+canvas_height], 
                                       [left_x, bottom_y+canvas_height]], 
                                       **my_default_background_settings)
    ax.add_patch(background_rectangle)
    set_background_colour(new_background_colour=background_colour)

  # set axis limits
  ax.set_aspect('equal')
  ax.set_xlim(left=left_x, right=right_x)
  ax.set_ylim(bottom=bottom_y, top=top_y)

  return ax

# this function creates two axes sets
def create_model_and_result_axes(method1, method2):
  _, axs = plt.subplots(2)
  plt.subplots_adjust(hspace=0.8)
  method1(ax=axs[0], title="Model To Start With", axes_tick_font_size=7, axes_label_font_size=10)
  method2(ax=axs[1], title="Completed Drawing")  

# this function shows the drawing 
# and saves if as a file if requested
# more information in the document below
# https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.savefig.html#matplotlib.pyplot.savefig 
def show_drawing_and_save_if_needed(filename=None,
                           figsize = my_default_figsize,
                           dpi = my_default_dpi,
                           figsize4saving = my_default_image_file_figsize,
                           dpi4saving = my_default_image_file_dpi,
                           margin_adjustments = my_default_margin_adjustments,
                           animation_file_figsize = my_default_animation_file_figsize,
                           animation_file_dpi = my_default_animation_file_dpi,
                           animation_interval = my_default_animation_interval,
                           animation_blit = my_default_animation_blit,
                           animation_repeat = my_default_animation_repeat,
                           animation_FPS = my_default_animation_FPS,
                           animation_func = None,
                           animation_init = None,
                           nb_of_frames = None):
  figure = plt.gcf()
  if (animation_func is None) != (nb_of_frames is None):
    raise Exception("Either both animation_func and nb_of_frames, or none, should be specified.")
  if (filename is not None) and (filename != ""):
    if animation_func is None:
      last_dot_position = filename.rfind(".")
      if last_dot_position < 0:
        filename += '.' + my_default_image_format
        last_dot_position = filename.rfind(".")
      figure.set_size_inches(figsize4saving)
      plt.savefig(fname="images_videos/"+filename, 
                  format = filename[last_dot_position+1:],
                  dpi = dpi4saving)
    else:
      figure.set_dpi(my_default_animation_file_dpi) 
      figure.set_size_inches(my_default_animation_file_figsize)
      anim = animation.FuncAnimation(
         fig=figure, 
         func=animation_func, 
         init_func=animation_init, 
         frames=nb_of_frames, 
         interval=animation_interval,
         blit=animation_blit, 
         repeat=animation_repeat)
      writer = animation.writers['ffmpeg'](fps=animation_FPS)
      anim.save("images_videos/"+filename+'.mp4', writer=writer)
  figure.set_dpi(dpi) 
  figure.set_size_inches(figsize)
  plt.subplots_adjust(**margin_adjustments)
  plt.show()