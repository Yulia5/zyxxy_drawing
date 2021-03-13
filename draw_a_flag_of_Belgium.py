
from zyxxy_canvas import create_canvas_and_axes, show_drawing_and_save_if_needed
from zyxxy_all_EXAMPLES import example_belgian_flag
from zyxxy_shape_functions import draw_a_square

#######################################################
# Creating the canvas!                               ##
ax = create_canvas_and_axes(  canvas_width = 6,
                              canvas_height = 4,
                              tick_step = 1,
                              title = "Belgian flag",
                              model = example_belgian_flag,
                              show_outlines = True)

#######################################################
# Now let's draw the shapes!                         ##
draw_a_square(ax=ax, left=1, bottom=0, side=2, colour='yellow')
draw_a_square(ax=ax, left=3, bottom=2, side=2, colour='yellow') 
draw_a_square(ax=ax, left=1, bottom=2, side=2, colour='red')
draw_a_square(ax=ax, left=3, bottom=0, side=2, colour='red')
draw_a_square(ax=ax, left=2, bottom=1, side=2, colour='black') 

show_drawing_and_save_if_needed()