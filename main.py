#######################################################
## Importing functions that we will use below        ##
from zyxxy_canvas import create_canvas_and_axes, show_drawing_and_save_if_needed
from zyxxy_shapes import draw_a_circle, draw_a_rectangle, draw_a_sector, draw_a_polygon
from zyxxy_lines import draw_a_broken_line
from zyxxy_coordinates import build_arc, link_contours
from zyxxy_settings import new_layer
from zyxxy_helpers import shift_layer, rotate_layer
import numpy as np
from matplotlib import animation
import matplotlib.pyplot as plt

def draw_a_leg(ax, x_coord, colour):

  draw_a_sector(ax=ax, centre_x=x_coord+feel_length/2, centre_y=bottom_body-leg_length, radius=feel_length/2, stretch_y=feet_height/(feel_length/2), angle_start=9, angle_end=3, colour=colour)

  draw_a_rectangle(ax=ax, left_x=x_coord, top_y=bottom_body, height=leg_length, width=leg_width, colour=colour)


#########################################################
## CREATING THE DRAWING!                               ##
#######################################################
# Creating the canvas!                               ##
ax = create_canvas_and_axes(canvas_width = 190,
                            canvas_height = 100,
                            background_colour = 'skyblue'
                            )

#######################################################
# Now let's draw the shapes!                         ##

left_body = 30
bottom_body = 30
right_body = 120
right_head = 180
top_body = 50
top_head = bottom_body+15
tail_right = 35 + left_body
tail_width = 10
centre_backside = 50
r_nostrils = 3
lip_y = 0.5 * (top_head + bottom_body)
lip_r = 3 
teeth_length = 5
nb_teeth = 7
leg_width = 10
leg_length = 15
feet_height = 5
feel_length = 20

# legs
for shift, colour in [[0, 'green'], [-17, 'lime']]:
  for x in [50, 100]:
    draw_a_leg(ax=ax, x_coord=x+shift, colour=colour)

new_layer()



nb_jaw_openings = 2
jaw_frames = 1
max_jaw_opening_angle = 1

nb_jumps = 2
prep_jump_frames = 1
jump_frames = 3
size_prep_jump = 5
size_jump = 15

def init():
  # do nothing
  shapes = rotate_layer(layer_nb=2, turn=0, diamond=[0, 0])
  return shapes

def animate(i):
  # upper jaw
  last_jaw_frame = nb_jaw_openings * 2 * jaw_frames
  if i < last_jaw_frame:
    this_jaw_move = i // jaw_frames
    if (this_jaw_move % 2) == 0:
      turn = -max_jaw_opening_angle / jaw_frames
    else:
      turn = max_jaw_opening_angle / jaw_frames
    print(i, turn)
    shapes = rotate_layer(layer_nb=2, turn=turn, diamond=[right_body-lip_r, lip_y+lip_r])
    return shapes

  # body jump
  if i % 2 == 0:
    shapes1 = shift_layer(layer_nb=1, shift=[0, 12])
    shapes2 = shift_layer(layer_nb=2, shift=[0, 12])
    print(i, 2)
  else:
    shapes1 = shift_layer(layer_nb=1, shift=[0,-12])
    shapes2 = shift_layer(layer_nb=2, shift=[0,-12])
    print(i, -2)
  

  return shapes1 + shapes2

total_nb_of_frames = nb_jaw_openings * 2 * jaw_frames + nb_jumps * (4 * prep_jump_frames + 2 * jump_frames)

nb_jumps = 2
prep_jump_frames = 1
jump_frames = 3


anim = animation.FuncAnimation(
         plt.gcf(), 
         animate, 
         init_func=init, 
         frames=total_nb_of_frames, 
         interval=200,
         blit=True)

show_drawing_and_save_if_needed(filename="")