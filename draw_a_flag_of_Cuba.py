
from zyxxy_canvas import create_canvas_and_axes, show_drawing_and_save_if_needed
from zyxxy_all_EXAMPLES import example_cuban_flag
from zyxxy_shape_functions import draw_a_triangle, draw_a_rectangle, draw_a_star

#######################################################
# Creating the canvas!                               ##
ax = create_canvas_and_axes(  canvas_width = 30,
                              canvas_height = 20,
                              tick_step = 2,
                              title = "Flag Of Cuba",
                              model = example_cuban_flag,
                              show_outlines = True)

#######################################################
# Now let's draw the shapes!                         ##
draw_a_triangle(ax=ax, tip_x=5, tip_y=10, width=20, height=17, colour='red', turn=3)

draw_a_rectangle(ax=ax, centre_x=15, centre_y=12, width=30, height=4, colour='blue')

draw_a_star(ax=ax, centre_x=15, centre_y=8, radius_1=3, radius_2=1, ends_qty=8, colour='white')

show_drawing_and_save_if_needed()