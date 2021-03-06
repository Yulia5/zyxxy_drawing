
from zyxxy_canvas import create_canvas_and_axes, show_drawing_and_save_if_needed
from zyxxy_all_EXAMPLES import example_japanese_flag
from zyxxy_shape_functions import draw_a_circle

#######################################################
# Creating the canvas!                               ##
create_canvas_and_axes(canvas_width = 30,
                              canvas_height = 20,
                              tick_step = 2,
                              title = "My first Zyxxy drawing",
                              model = example_japanese_flag,
                              outlines_colour = "cyan"
                              )

#######################################################
# Now let's draw the shapes!                         ##
draw_a_circle(centre_x=8, centre_y=8, radius=8, colour='crimson') 

show_drawing_and_save_if_needed()