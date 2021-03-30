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
from MY_zyxxy_SETTINGS_demo import figure_params
from MY_zyxxy_SETTINGS_widgets import widget_params
from zyxxy_shape_functions import draw_a_circle, draw_a_segment, draw_a_sector, draw_a_wave
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
plot_ax_bottom = get_demo_rax_bottom() + figure_params['plot_bottom_gap']
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

colour = {'angle' : 'violet', 'sinus' : 'blue', 'cosinus' : 'red'}
angle = 0
dot_coords = [sin_hours(angle), cos_hours(angle)]
values =  {'angle' : angle, 'sinus' : sin_hours(angle), 'cosinus' : cos_hours(angle)}
start_trigo = 1.5
wave_factor = 6
set_default_outline_style(linewidth=3)
set_default_line_style(linewidth=3)

colors = colour.values()
lines = [Line2D([0], [0], color=c, linewidth=3) for c in colors]
labels = [k + ('(' + str(angle) + 'h)' if k!= 'angle' else '') + '=' + str(round(values[k], 3)) + ('' if k!= 'angle' else 'h') for k in colour.keys()]


draw_a_circle(centre_x=0, centre_y=0, radius=1)

draw_a_sector(centre_x=0, centre_y=0, radius=.2, angle_start=0, angle_end=angle, colour=colour['angle'])
draw_a_segment(start_x=0, start_y=0, length=1, turn=angle)

# cos
set_default_line_style(colour=colour['cosinus'])
draw_a_segment(start_x=0, start_y=0, length=cos_hours(angle), turn=full_turn_angle/4)
set_default_line_style(colour=colour['sinus'])
draw_a_segment(start_x=cos_hours(angle), start_y=0, length=sin_hours(angle), turn=0)
set_default_line_style(colour='black')
draw_a_segment(start_x=cos_hours(angle), start_y=max(0, sin_hours(angle)), length=start_trigo-max(0, sin_hours(angle)), turn=0)
set_default_line_style(colour=colour['cosinus'])
draw_a_wave(start_x=start_trigo+angle/wave_factor, start_y=1, width=-angle/wave_factor, height=2, angle_start=3, nb_waves=angle/full_turn_angle)

# sin
set_default_line_style(colour=colour['sinus'])
draw_a_segment(start_x=0, start_y=0, length=sin_hours(angle), turn=0)
set_default_line_style(colour=colour['cosinus'])
draw_a_segment(start_x=0, start_y=sin_hours(angle), length=cos_hours(angle), turn=full_turn_angle/4)
set_default_line_style(colour='black')
draw_a_segment(start_x=max(0, cos_hours(angle)), start_y=sin_hours(angle), length=start_trigo-max(0, cos_hours(angle)), turn=full_turn_angle/4)

set_default_line_style(colour=colour['sinus'])
sinus_wave = draw_a_wave(start_x=start_trigo+angle/wave_factor, start_y=0, width=-angle/wave_factor, height=2, angle_start=0, nb_waves=angle/full_turn_angle)
sinus_wave.flip()
sinus_wave.rotate(turn=9, diamond_override=[0, 0])

# point
draw_a_circle(centre_x=dot_coords[0], centre_y=dot_coords[1], radius=.1, colour='black')
draw_a_circle(centre_x=start_trigo, centre_y=sin_hours(angle), radius=.1, colour=colour['sinus'])
draw_a_circle(centre_x=cos_hours(angle), centre_y=start_trigo, radius=.1, colour=colour['cosinus'])

# a legend
plt.legend(lines, labels, loc='upper right') 

#draw_a_segment(start_x=0, start_y=dot_coords[0], length=dot_coords[1], turn=3)
fig.set_dpi(figure_params['dpi']) 
fig.set_size_inches(figure_params['figsize'] /2 )
if not is_running_tests():
  plt.show()