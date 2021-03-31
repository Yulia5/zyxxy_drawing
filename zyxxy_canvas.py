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

import inspect
import ntpath
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

USE_PLT_SHOW = True

def __prepare_axes(ax, canvas_width, canvas_height, make_symmetric, tick_step, 
                       title_font_size, axes_label_font_size, axes_tick_font_size, 
                       title=None, background_colour=None):

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
    if background_colour is not None:
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

  if title is not None: 
    ax.set_title(title, fontdict={'size': title_font_size})
    

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
                           dpi = 100,
                           margin_side = my_default_display_params['margin_side'],
                           axes = None,
                           model = None,
                           model_zoom = 1.,
                           outlines_colour = None):

  params_for_axes = {  'canvas_width'         : canvas_width,
                       'canvas_height'        : canvas_height, 
                       'make_symmetric'       : make_symmetric,
                       'tick_step'            : tick_step, 
                       'axes_label_font_size' : axes_label_font_size, 
                       'axes_tick_font_size'  : axes_tick_font_size,
                       'title_font_size'      : title_font_size}

  if axes is not None: # only needed for demo and when called inside models
    plt.gcf().sca(axes)
    __prepare_axes(ax=axes, **params_for_axes)
    return axes

  axis_width_add = 2 * margin_side
  axis_height_add = 2 * margin_side + title_font_size/72
  axis_left, axis_bottom = margin_side, margin_side
  if tick_step is not None:
    axis_width_add  += (axes_label_font_size + axes_tick_font_size) / 72
    axis_height_add += (axes_label_font_size + axes_tick_font_size) / 72
    axis_left       += (axes_label_font_size + axes_tick_font_size) / 72
    axis_bottom     += (axes_label_font_size + axes_tick_font_size) / 72

  figsize = max_figsize
  figure = plt.figure(1)

  if model is not None:

      scale_horizontal = (max_figsize[0] - axis_width_add) / canvas_width
      scale_vertical = (max_figsize[1] - axis_height_add) / canvas_height
      scale_horizontal_2 = (max_figsize[0]/2 - axis_width_add) / canvas_width
      scale_vertical_2 = (max_figsize[1]/2 - axis_height_add) / canvas_height

      # decide if the model should be below (vertical) or to the right (horizontal) of the working axes
      scale_if_V_placement = min(scale_vertical_2, scale_horizontal)
      scale_if_H_placement = min(scale_vertical, scale_horizontal_2)

      place_model_H_not_V = (scale_if_H_placement > scale_if_V_placement)
      scale = max(scale_if_V_placement, scale_if_H_placement)
      figsize = [canvas_width * scale + axis_width_add, canvas_height * scale + axis_height_add]
      
      if place_model_H_not_V:
        figsize[0] *= 2
      else:
        figsize[1] *= 2

      axes = plt.axes([axis_left/figsize[0], axis_bottom/ figsize[1],
                     canvas_width * scale/figsize[0], canvas_height * scale/ figsize[1]])
      axes_model = plt.axes([axis_left/figsize[0]+ 0.5 * place_model_H_not_V, 
                             axis_bottom/figsize[1] + 0.5 * (1 - place_model_H_not_V),
                             canvas_width * scale/figsize[0], canvas_height * scale/ figsize[1]])

      if not place_model_H_not_V:
        axes_model, axes = axes, axes_model
  else:
    scale_horizontal = (max_figsize[0] - axis_width_add) / canvas_width
    scale_vertical = (max_figsize[1] - axis_height_add) / canvas_height
    scale = min(scale_horizontal, scale_vertical)
    figsize = [canvas_width * scale + axis_width_add, canvas_height * scale + axis_height_add]
    axes = plt.axes([axis_left/figsize[0], axis_bottom / figsize[1], canvas_width * scale / figsize[0], canvas_height * scale / figsize[1]])

  figure.set_dpi(dpi) 
  figure.set_size_inches(figsize)
  
  if model is not None:

    # halve the font size
    global my_default_font_sizes
    for l in ['axes_label', 'tick', 'title']:
      my_default_font_sizes[l] /= 2

    # handle the model drawing
    if isinstance(model, str):
      __prepare_axes(ax=axes_model, title = "Original Drawing", **params_for_axes)
      image = filename_to_image(filename=model)
      scaling_factor = model_zoom * min(canvas_width/image.shape[1], canvas_height/image.shape[0])
      # defining LB_position to center the model image
      LB_position=[axes_model.get_xlim()[0] + 0.5 * (canvas_width  - image.shape[1] * scaling_factor), 
                   axes_model.get_ylim()[0] + 0.5 * (canvas_height - image.shape[0] * scaling_factor)]
      # placing the image
      show_image(ax=axes_model, prepared_image=image, origin=[0, 0], zorder=0, scaling_factor=scaling_factor,  LB_position=LB_position)  
    else:
      global USE_PLT_SHOW
      USE_PLT_SHOW = False
      plt.gcf().sca(axes_model)
      model(axes=axes_model) 
      USE_PLT_SHOW = True
      if outlines_colour is not None:
        set_outlines_colour(outlines_colour)
        set_diamond_size_factor(0)
        USE_PLT_SHOW = False
        plt.gcf().sca(axes)
        model(axes=axes)
        USE_PLT_SHOW = True
        set_outlines_colour(None)
      __prepare_axes(ax=axes_model, title = "Completed Drawing", **params_for_axes)
 
  __prepare_axes(ax=axes, title=title, background_colour=background_colour, **params_for_axes)
  set_diamond_size_factor(value=(tick_step is not None))

  plt.gcf().sca(axes)

  return axes

# this function shows the drawing 
# and saves if as a file if requested
# more information in the document below
# https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.savefig.html#matplotlib.pyplot.savefig 

# assumes that there is only one set of axes - to be reviewed

def __default_animation_init():
  # return the list of the shapes that are moved by animation
  return get_all_polygons_in_layers()

def __envelope_animate(i, anim_func):
  result = anim_func(i)
  if result is not None:
    return result
  # return the list of the shapes that are moved by animation
  return get_all_polygons_in_layers()

def show_drawing_and_save_if_needed(save=True,
                           filename=None,
                           #dpi4saving = my_default_image_params['dpi'], causes spurious image resizing
                           image_format = my_default_image_params['format'],
                           animation_file_dpi = my_default_animation_params['dpi'],
                           animation_interval = my_default_animation_params['interval'],
                           animation_blit = my_default_animation_params['blit'],
                           animation_repeat = my_default_animation_params['repeat'],
                           animation_FPS = my_default_animation_params['FPS'],
                           animation_writer = my_default_animation_params['writer'],
                           animation_format = my_default_animation_params['format'],
                           animation_func = None,
                           animation_init = __default_animation_init,
                           nb_of_frames = None,
                           block=True):

  if save and USE_PLT_SHOW: # and not is_running_tests():
    if filename is None:
      frame = inspect.stack()[1]
      module = inspect.getmodule(frame[0])
      if module is not None:
        caller_filename = ntpath.basename(module.__file__)
      else:
        curframe = inspect.currentframe()
        caller_filename = inspect.getouterframes(curframe)[1].filename
      if caller_filename == "zyxxy_all_EXAMPLES.py":
        filename = frame.function
      else:
        caller_filename = caller_filename[:-3] # to remove ".py"
        for prefix_ in ["draw_", "drawn_"]:
          if caller_filename.startswith(prefix_):
            filename = caller_filename[len(prefix_):] # remove the prefix

    figure = plt.gcf()
    
    if (animation_func is None) != (nb_of_frames is None):
      raise Exception("Either both animation_func and nb_of_frames, or none, should be specified.")

    if animation_func is None:
      if (filename is not None) and (filename != ""):
        last_dot_position = filename.rfind(".")
        if last_dot_position < 0:
          filename += '.' + image_format
          last_dot_position = filename.rfind(".")
        plt.savefig(fname="images_videos/"+filename, 
                    format = filename[last_dot_position+1:]
                    # , dpi = dpi4saving
                    )
        #figure.set_dpi(150)
    else:
      figure.set_dpi(animation_file_dpi) 
      writer = animation.writers[animation_writer](fps=animation_FPS)
      # writer = animation.FFMpegWriter(fps=animation_FPS) 
      anim = animation.FuncAnimation( fig=figure, 
                                      func=partial(__envelope_animate, anim_func=animation_func), 
                                      init_func=animation_init,  
                                      frames=nb_of_frames, 
                                      interval=animation_interval,
                                      blit=animation_blit, 
                                      repeat=animation_repeat)
      if (filename is not None) and (filename != ""):
        anim.save("images_videos/"+filename+'.'+animation_format, writer=writer)
      figure.set_dpi(100) 

  if USE_PLT_SHOW and not is_running_tests():
    plt.show(block=(block and USE_PLT_SHOW))