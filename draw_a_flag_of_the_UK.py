
from zyxxy_canvas import create_canvas_and_axes, show_drawing_and_save_if_needed
from zyxxy_all_EXAMPLES import example_british_flag
from zyxxy_shape_functions import draw_a_rectangle

#######################################################
# Creating the canvas!                               ##
axes = create_canvas_and_axes(canvas_width = 18,
                              canvas_height = 12,
                              tick_step = 1,
                              title = "Flag Of The U.K.",
                              model = example_british_flag,
                              show_outlines = True)

#######################################################
# Now let's draw the shapes!                         ##
draw_a_rectangle(ax=axes, centre_x=9, centre_y=2, width=22, height=1, colour='red', turn=6)

draw_a_rectangle(ax=axes, centre_x=3, centre_y=2, width=22, height=2, colour='red', turn=3)

draw_a_rectangle(ax=axes, centre_x=9, centre_y=6, width=8, height=6, colour='navy')

draw_a_rectangle(ax=axes, centre_x=9, centre_y=6, width=22, height=3, colour='white', turn=6)

show_drawing_and_save_if_needed()