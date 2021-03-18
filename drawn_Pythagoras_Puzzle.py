from zyxxy_canvas import create_canvas_and_axes, show_drawing_and_save_if_needed
from zyxxy_utils import atan_hours
from zyxxy_shape_functions import draw_a_square, clone_a_shape, draw_a_polygon
import matplotlib.pyplot as plt
from MY_zyxxy_SETTINGS import my_default_font_sizes

ax_side= 12

#######################################################
# Creating the canvas!                               ##
axes = create_canvas_and_axes(canvas_width = ax_side,
                              canvas_height = ax_side+3,
                              tick_step = 1,
                              title = "Pythagoras Puzzle")

a_square = draw_a_square(ax=axes, side=5, centre_x=ax_side/2, centre_y=ax_side/2, colour='crimson', turn=atan_hours(3/4))
triangle_1 = draw_a_polygon(ax=axes, contour=[[0, 3], [0, 0], [4, 0]], colour='dodgerblue')

triangle_2 = clone_a_shape(triangle_1)
triangle_2.shift(shift=[0, 8])

triangle_3 = clone_a_shape(triangle_1)
triangle_3.shift(shift=[8, 8])
triangle_3.rotate(turn=1)

triangle_4 = clone_a_shape(triangle_1)
triangle_4.shift(shift=[8, 0])
triangle_4.rotate(turn=11)

header_txts = [plt.text(x=0, y=ax_side+yp, s=s, fontdict={'size': my_default_font_sizes['title']/2}) for  s, yp in [["All Triangles Together", 1.5], [" -> A Rectangle", 0]]]

#######################################################
# Kian's code  that puts all triangles together into a rectangle goes here ...
# Kian can use methods "shift" and "rotate", as above, to move TRIANGLES
#######################################################

show_drawing_and_save_if_needed(block=False)
input("Press ENTER when you are ready ...")

#######################################################
# Kian's code that puts [all triangles] + [a square] => [a bigger square] goes here ...
# Kian can use methods "shift" and "rotate", as above, to move TRIANGLES
#######################################################

a_square.set_style(colour="violet")
header_txts[0].set_text("A Square + 4 Triangles Together")
header_txts[1].set_text(" -> A Bigger Square")

plt.show()