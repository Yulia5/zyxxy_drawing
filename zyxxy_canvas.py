#####################################################
## don't change this file, please                  ##
#####################################################

import numpy as np
import matplotlib.pyplot as plt
from zyxxy_helpers import set_diamond_style
from zyxxy_shapes import draw_a_rectangle
from zyxxy_settings import set_shape_style, set_line_style

from zyxxy_MY_SETTINGS import  my_default_image_format,my_default_title_font_size,my_default_axes_label_font_size,my_default_axes_tick_font_size, my_default_figsize,my_default_dpi, my_default_figsize4saving, my_default_dpi4saving, my_default_margin_adjustments

background_rectangle = None

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

  # set line and outline styles
  set_shape_style(outline_colour='black', outline_width=0, outline_joinstyle='miter', outline_zorder=0, shape_zorder=0, shape_alpha=1.0)

  set_line_style(colour='black', linewidth=2, joinstyle='round', zorder=0)

  ax.set_title(title, fontdict={'size': title_font_size})

  if make_symmetric:
    left_x, right_x = -canvas_width/2, canvas_width/2
    bottom_y, top_y = -canvas_height/2, canvas_height/2
  else:
    left_x, right_x = 0, canvas_width
    bottom_y, top_y = 0, canvas_height

  if tick_step is not None:
    ax.grid(True)
    ax.set_xlabel("RULER FOR X's", fontsize=axes_label_font_size)
    ax.set_ylabel("RULER FOR Y's", fontsize=axes_label_font_size)
    ax.tick_params(axis='both', which='major', labelsize=axes_tick_font_size)
    x_ticks = np.arange(left_x, right_x, tick_step)
    ax.set_xticks(ticks = x_ticks)
    y_ticks = np.arange(bottom_y, top_y, tick_step)
    ax.set_yticks(ticks = y_ticks)
  else:
    ax.grid(False)
    ax.set_xticks(ticks = [])
    ax.set_yticks(ticks = [])
    if background_colour is not None:
      background_rectangle = draw_a_rectangle(ax=ax, left_x=left_x, bottom_y=bottom_y, height=canvas_height, width=canvas_width, colour=background_colour, zorder=-1)

  # show diamond points if and only if we show the axis and grid
  set_diamond_style(show = (tick_step is not None))

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
                           figsize4saving = my_default_figsize4saving,
                           dpi4saving = my_default_dpi4saving,
                           margin_adjustments = my_default_margin_adjustments):
  figure = plt.gcf()
  if (filename is not None) and (filename != ""):
    last_dot_position = filename.rfind(".")
    if last_dot_position < 0:
      filename += '.' + my_default_image_format
      last_dot_position = filename.rfind(".")
    figure.set_size_inches(figsize4saving)
    plt.savefig(fname = filename, 
                format = filename[last_dot_position+1:],
                dpi = dpi4saving)
  figure.set_dpi(dpi) 
  figure.set_size_inches(figsize)
  plt.subplots_adjust(**margin_adjustments)
  plt.show()

def set_background_colour(new_background_colour):
  global background_rectangle
  background_rectangle.set_fc(new_background_colour)
  background_rectangle.set_ec(new_background_colour)
