#######################################################
## Importing functions that we will use below        ##
from zyxxy_canvas import create_canvas_and_axes, show_drawing_and_save_if_needed
from zyxxy_shape_functions import draw_a_triangle, draw_a_circle, draw_a_segment
from zyxxy_shape_style import set_line_style, new_layer

#########################################################
## CREATING THE DRAWING!                               ##
#######################################################
# Creating the canvas!                               ##
ax = create_canvas_and_axes(canvas_width = 12,
                            canvas_height = 10, 
                            title = "Hello, I am Zyxxy!")

set_line_style(linewidth=2)
#######################################################
# Now let's draw the shapes!                         ##

# Let's start with the whiskers! They need to be behind the head, 
# so we will need to move these lines before the line
# that draws the head of the mouse!
draw_a_segment(ax, start_x=6, start_y=3, turn=3, length=2)
draw_a_segment(ax, start_x=6, start_y=3, turn=4, length=2)
draw_a_segment(ax, start_x=6, start_y=3, turn=9, length=2)
draw_a_segment(ax, start_x=6, start_y=3, turn=8, length=2)

# let's draw the head of the mouse
draw_a_triangle(ax=ax, tip_x=6, tip_y=1, height=6, width=6, colour='plum')
# ... and the nose, using a triangle with the same tip
draw_a_triangle(ax=ax, tip_x=6, tip_y=1, height=1, width=1, colour='black')
# ... and the ears
draw_a_circle(ax=ax, centre_x=3, centre_y=7, radius=2, colour='plum')
draw_a_circle(ax=ax, centre_x=9, centre_y=7, radius=2, colour='plum')
# ... and the eyes, white circles with black circles on top
draw_a_circle(ax=ax, centre_x=5, centre_y=5, radius=0.8, colour='white')
draw_a_circle(ax=ax, centre_x=7, centre_y=5, radius=0.8, colour='white')
draw_a_circle(ax=ax, centre_x=5, centre_y=5, radius=0.5, colour='black')
draw_a_circle(ax=ax, centre_x=7, centre_y=5, radius=0.5, colour='black')

show_drawing_and_save_if_needed(filename="zyxxy")