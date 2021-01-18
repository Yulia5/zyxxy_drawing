#######################################################
## Importing functions that we will use below        ##
from zyxxy_canvas import create_canvas_and_axes, show_drawing_and_save_if_needed
from zyxxy_shapes import draw_a_circle, draw_a_rectangle, draw_a_sector, draw_a_polygon
from zyxxy_lines import draw_a_broken_line
from zyxxy_coordinates import build_arc, link_contours
from zyxxy_settings import set_line_style, new_layer
import numpy as np

def draw_leg(ax, x_coord, colour):

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
    draw_leg(ax=ax, x_coord=x+shift, colour=colour)

# body
draw_a_rectangle(ax=ax, left_x=left_body, bottom_y=bottom_body, height=top_body-bottom_body, width=right_body-left_body, colour='lime')

# backside
draw_a_sector(ax=ax, centre_x=left_body, centre_y=centre_backside, radius=centre_backside-bottom_body,angle_start=6, angle_end=12, colour='lime')

# tail
draw_a_rectangle(ax=ax, left_x=left_body, top_y=2*centre_backside-bottom_body, height=tail_width, width=tail_right-left_body, colour='lime')

draw_a_sector(ax=ax, centre_x=tail_right, centre_y=2*centre_backside-bottom_body, radius=tail_width,angle_start=3, angle_end=6, colour='lime')

draw_a_circle(ax=ax, centre_x=left_body, centre_y=(2*centre_backside-bottom_body-tail_width+top_body)/2, radius=(2*centre_backside-bottom_body-tail_width-top_body)/2, colour='skyblue')

# head
draw_a_rectangle(ax=ax, left_x=right_body, bottom_y=bottom_body, height=top_head-bottom_body, width=right_head-right_body, colour='lime')


# ... and the eyes, white circles with black circles on top
eye_y = top_body
for radius, colour in [[8, 'lime'], [5, 'white'], [3, 'black']]:
  for eye_x in [right_body, right_body+12]:
    draw_a_circle(ax=ax, centre_x=eye_x, centre_y=eye_y, radius=radius, colour=colour)

# ... and the nostrils
nostril_y = top_head
for nostril_x in [right_head-r_nostrils, right_head-3*r_nostrils]:
  draw_a_circle(ax=ax, centre_x=nostril_x, centre_y=nostril_y, radius=r_nostrils, colour='lime')
  draw_a_circle(ax=ax, centre_x=nostril_x, centre_y=nostril_y, radius=1, colour='green')

# ... and the teeth and the lip
# teeth
teeth_x = np.linspace(right_body-lip_r, right_head, 2*nb_teeth+1)
teeth = np.array([[teeth_x[t], lip_y - (t%2) * teeth_length] for t in range(2*nb_teeth+1)])
draw_a_polygon(ax=ax, contour=teeth, colour='white')
# upper lip
lipline_top = build_arc(centre_x=right_body-lip_r, centre_y=lip_y+lip_r, radius_x=lip_r, radius_y=lip_r, angle_start=6, angle_end=9)
lipline_top = link_contours([[right_head, lip_y]], lipline_top)
draw_a_broken_line(ax=ax, points=lipline_top, colour='green', linewidth=2)

show_drawing_and_save_if_needed(filename="croc")