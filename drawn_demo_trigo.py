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

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
from zyxxy_utils import full_turn_angle, sin_hours, cos_hours
from zyxxy_canvas import create_canvas_and_axes, is_running_tests
from zyxxy_widgets import add_a_slider
from MY_zyxxy_SETTINGS_demo import figure_params
from MY_zyxxy_SETTINGS_widgets import widget_params
from zyxxy_shape_functions import draw_a_circle, draw_a_broken_line, draw_a_sector, draw_a_wave
from zyxxy_shape_style import set_default_line_style, set_default_outline_style, set_diamond_size_factor

plt.rcParams.update({'font.size': figure_params['font_size']})

##########################################################################################
# create the figure
fig = plt.figure()
canvas_width  = 5 * 2
canvas_height = 3.5 * 2
##########################################################################################
# Creating the canvas!
##########################################################################################

def get_max_specific_sliders():
  max_specific_sliders = 1
  return max_specific_sliders

def get_demo_rax_bottom():
  max_widget_qty = get_max_specific_sliders() 
  demo_rax_bottom = max_widget_qty * (widget_params['height'] + widget_params['gap']) 
  demo_rax_bottom += figure_params['plot_bottom_gap']
  return demo_rax_bottom

plot_ax_left   = figure_params['plot_gap']
plot_ax_bottom = get_demo_rax_bottom() + figure_params['plot_bottom_gap'] + 0.2
ax = plt.axes([plot_ax_left, plot_ax_bottom, 1 - 2 * plot_ax_left, 1 - plot_ax_bottom])

print([plot_ax_left, plot_ax_bottom, 1 - 2 * plot_ax_left, 1 - plot_ax_bottom])

set_diamond_size_factor(value=0.)

create_canvas_and_axes(canvas_width=canvas_width,
                            canvas_height=canvas_height, 
                            tick_step=figure_params['tick_step'],
                            title="Try Out Shapes",
                            make_symmetric = True,
                            title_font_size=figure_params['font_size']*1.5,
                            axes_label_font_size=figure_params['font_size'],
                            axes_tick_font_size=figure_params['font_size'],
                            axes=ax)

colour = {'angle' : 'violet', 'sinus' : 'dodgerblue', 'cosinus' : 'blueviolet'}

start_trigo = 1.5
wave_factor = 6
set_default_outline_style(linewidth=3)
set_default_line_style(linewidth=3)


segments = [None for _ in range(7)]

draw_a_circle(centre_x=0, centre_y=0, radius=1)

sector = draw_a_sector(centre_x=0, centre_y=0, radius=.2, angle_start=0, angle_end=0, colour=colour['angle'])
segments[0] = draw_a_broken_line(contour=[[0, 0]], colour='crimson')

set_default_outline_style(linewidth=0)

# cos
segments[1] = draw_a_broken_line(contour=[[0, 0]], colour=colour['cosinus'])
segments[2] = draw_a_broken_line(contour=[[0, 0]], colour=colour['sinus'])
segments[3] = draw_a_broken_line(contour=[[0, 0]], colour='black')
wave_sinus = draw_a_wave(start_x=start_trigo, start_y=1, width=1, height=2, angle_start=0, nb_waves=1, colour=colour['sinus'], turn=9)
dot_sinus = draw_a_circle(centre_x=0, centre_y=0, radius=.1, colour=colour['sinus'])

# sin
segments[4] = draw_a_broken_line(contour=[[0, 0]], colour=colour['sinus'])
segments[5] = draw_a_broken_line(contour=[[0, 0]], colour=colour['cosinus'])
segments[6] = draw_a_broken_line(contour=[[0, 0]], colour='black')
wave_cosinus = draw_a_wave(start_x=start_trigo+0, start_y=0, width=1, height=2, angle_start=3, nb_waves=1, colour=colour['cosinus'])
dot_cosinus = draw_a_circle(centre_x=0, centre_y=0, radius=.1, colour=colour['cosinus'])

# point
dot = draw_a_circle(centre_x=0, centre_y=0, radius=.1, colour='black')

def change_angle(angle):

  sin_angle, cos_angle = sin_hours(angle), cos_hours(angle)

  segment_coords = [[[0, 0], [sin_angle, cos_angle]],
                    [[0, 0], [0, cos_angle]],
                    [[0, cos_angle], [sin_angle, cos_angle]],
                    [[max(0, sin_angle), cos_angle], [start_trigo, cos_angle]],
                    [[0, 0], [sin_angle, 0]],
                    [[sin_angle, 0], [sin_angle, cos_angle]],
                    [[sin_angle, max(0, cos_angle)], [sin_angle, start_trigo]]]
  for i in range(7):
    segments[i].update_xy_by_shapename(shapename=segment_coords[i])

  sector.update_shape_parameters(angle_end=angle)
  dot.shift_to([sin_angle, cos_angle])

  dot_sinus.shift_to( [sin_angle, start_trigo])
  wave_sinus.shift_to([sin_angle, start_trigo])
  #wave_sinus.update_shape_parameters(width=angle/wave_factor) # , # nb_waves=angle/full_turn_angle
  print(wave_sinus.diamond_coords)

  dot_cosinus.shift_to( [start_trigo, cos_angle])
  wave_cosinus.shift_to([start_trigo, cos_angle])
  #wave_cosinus.update_shape_parameters(width=-angle/wave_factor, nb_waves=angle/full_turn_angle)
  print(wave_cosinus.diamond_coords)

angle = 12
change_angle(angle=angle)

dot_coords = [sin_hours(angle), cos_hours(angle)]
values =  {'angle' : angle, 'sinus' : sin_hours(angle), 'cosinus' : cos_hours(angle)}
colors = colour.values()
lines = [Line2D([0], [0], color=c, linewidth=3) for c in colors]
labels = [k + ('(' + str(angle) + 'h)' if k!= 'angle' else '') + '=' + str(round(values[k], 3)) + ('' if k!= 'angle' else 'h') for k in colour.keys()]

# a legend
plt.legend(lines, labels, loc='upper right') 

add_a_slider(w_left=plot_ax_left+.2, w_bottom=figure_params['plot_bottom_gap'], w_caption='angle', s_vals=[0, 36, 0, 0.2], on_click_or_change=change_angle)


fig.set_dpi(figure_params['dpi']) 
fig.set_size_inches(figure_params['figsize'] / 1.5 )
if not is_running_tests():
  plt.show()