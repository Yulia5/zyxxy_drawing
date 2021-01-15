#####################################################
## don't change this file, please                  ##
#####################################################

import numpy as np
import matplotlib.pyplot as plt
from zyxxy_helpers import set_diamond_style
from zyxxy_shapes import draw_rectangle
from zyxxy_settings import set_shape_style, set_line_style

_default_image_format = "png"
_default_title_font_size = 20
_default_axes_label_font_size = 14
_default_axes_tick_font_size = 10

# create the axis, set their sizes, 
# add the grid and ticks if needed
def create_canvas_and_axes(canvas_width,
                           canvas_height,
                           tick_step = None,
                           background_colour = None,
                           title = None,
                           title_font_size = _default_title_font_size,
                           axes_label_font_size = _default_axes_label_font_size,
                           axes_tick_font_size = _default_axes_tick_font_size,
                           ax = None):
  if ax is None:
    _, ax = plt.subplots()

  # set line and outline styles
  set_shape_style(outline_colour='black', outline_width=0, outline_joinstyle='miter', outline_zorder=0, shape_zorder=0, shape_alpha=1.0)

  set_line_style(colour='black', linewidth=2, joinstyle='round', zorder=0)

  ax.set_title(title, fontdict={'size': title_font_size})
  if tick_step is not None:
    ax.grid(True)
    ax.set_xlabel("RULER FOR X's", fontsize=axes_label_font_size)
    ax.set_ylabel("RULER FOR Y's", fontsize=axes_label_font_size)
    ax.tick_params(axis='both', which='major', labelsize=axes_tick_font_size)
    x_ticks = np.arange(0, canvas_width, tick_step)
    ax.set_xticks(ticks = x_ticks)
    y_ticks = np.arange(0, canvas_height, tick_step)
    ax.set_yticks(ticks = y_ticks)
  else:
    ax.grid(False)
    ax.set_xticks(ticks = [])
    ax.set_yticks(ticks = [])
    if background_colour is not None:
      draw_rectangle(ax=ax, centre_x=canvas_width/2, centre_y=canvas_height/2, height=canvas_height, width=canvas_width, colour=background_colour, zorder=-1)

  # show diamond points if and only if we show the axis and grid
  set_diamond_style(show = (tick_step is not None))

  # set axis limits
  ax.set_aspect('equal')
  ax.set_xlim(left=0, right=canvas_width)
  ax.set_ylim(bottom=0, top=canvas_height)

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
def show_drawing_and_save_if_needed(filename=None):
  if filename is not None:
    last_dot_position = filename.rfind(".")
    if last_dot_position < 0:
      filename += '.' + _default_image_format
      last_dot_position = filename.rfind(".")
    plt.savefig(fname = filename, 
                format = filename[last_dot_position+1:])
  plt.show()


def get_width(ax):
  xlims = ax.set_xlim()
  return (xlims[1] - xlims[0])

def get_height(ax):
  ylims = ax.set_ylim()
  return (ylims[1] - ylims[0])