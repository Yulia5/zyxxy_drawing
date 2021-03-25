
from zyxxy_canvas import create_canvas_and_axes, show_drawing_and_save_if_needed
from zyxxy_all_EXAMPLES import example_belgian_flag
from zyxxy_shape_functions import draw_a_square

#######################################################
# Creating the canvas!                               ##
create_canvas_and_axes(  canvas_width = 6,
                         canvas_height = 4,
                         tick_step = 1,
                         title = "Belgian flag",
                         model = example_belgian_flag,
                         outlines_colour = "cyan")

#######################################################
# Now let's draw the shapes!                         ##
draw_a_square(left=1, bottom=0, side=2, colour='yellow')
draw_a_square(left=3, bottom=2, side=2, colour='yellow') 
draw_a_square(left=1, bottom=2, side=2, colour='red')
draw_a_square(left=3, bottom=0, side=2, colour='red')
draw_a_square(left=2, bottom=1, side=2, colour='black') 

show_drawing_and_save_if_needed()