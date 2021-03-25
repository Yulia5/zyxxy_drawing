
from zyxxy_canvas import create_canvas_and_axes, show_drawing_and_save_if_needed
from zyxxy_all_EXAMPLES import example_japanese_naval_flag
from zyxxy_shape_functions import draw_a_circle, draw_a_triangle

#######################################################
# Creating the canvas!                               ##
axes = create_canvas_and_axes(canvas_width = 30,
                              canvas_height = 20,
                              tick_step = 2,
                              title = "Flag Of Japanese Navy",
                              model = example_japanese_naval_flag
                              #, outlines_colour = "cyan"
                              )


draw_a_circle(ax=axes, centre_x=20, centre_y=12, radius=6, colour='crimson')
for i in range(3):
  draw_a_triangle(ax=axes, tip_x=9, tip_y=7, height=30, width=6, turn=i*12/3, colour='crimson')  

show_drawing_and_save_if_needed()