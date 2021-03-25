
from zyxxy_canvas import create_canvas_and_axes, show_drawing_and_save_if_needed
from zyxxy_all_EXAMPLES import example_finnish_flag
from zyxxy_shape_functions import draw_a_rectangle

#######################################################
# Creating the canvas!                               ##
create_canvas_and_axes(canvas_width = 36,
                              canvas_height = 22,
                              tick_step = 2,
                              title = "Flag Of Finland",
                              model = example_finnish_flag,
                              outlines_colour = "red")

#######################################################
# Now let's draw the shapes!                         ##
draw_a_rectangle(left=22, centre_y=11, width=6, height=10, colour='midnightblue') 

show_drawing_and_save_if_needed()
