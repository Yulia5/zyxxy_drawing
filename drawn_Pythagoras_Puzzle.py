from zyxxy_canvas import create_canvas_and_axes, show_drawing_and_save_if_needed
from zyxxy_utils import atan_hours, wait_for_enter, is_running_tests, random_integer_number, calc_Pythagoras
from zyxxy_shape_functions import draw_a_square, clone_a_shape, draw_a_polygon
import matplotlib.pyplot as plt
from MY_zyxxy_SETTINGS import my_default_font_sizes

#######################################################
# Creating the canvas!                               ##
create_canvas_and_axes(canvas_width = 20,
                              canvas_height = 23,
                              tick_step = 1,
                              make_symmetric = True,
                              title = "Pythagoras Puzzle")

header_txts = [plt.text(x=plt.gca().get_xlim()[0]+1.5, y=plt.gca().get_ylim()[1]-i*1.53, s="", fontdict={'size': my_default_font_sizes['title']/2}) for i in range(1, 4)]

#######################################################

a = 6 # random_integer_number(max=8, min=3.)
b = 8 # random_integer_number(max=8, min=3.)
c = calc_Pythagoras(a=a, b=b)

print("a = ", a, ", b = ", b, ", c = ", c)

a_square = draw_a_square(side=c, centre_x=0, centre_y=0, colour='crimson')
triangle_1 = draw_a_polygon(contour=[[0, a], [0, 0], [b, 0]], colour='dodgerblue')
triangle_1.shift(shift=[-10, -10])

triangle_2 = clone_a_shape(triangle_1)
triangle_2.shift(shift=[0, 15])
#triangle_2.set_style(colour="royalblue")

triangle_3 = clone_a_shape(triangle_1)
triangle_3.shift(shift=[15, 15])
triangle_3.rotate(turn=1)

triangle_4 = clone_a_shape(triangle_1)
triangle_4.shift(shift=[15, 0])
triangle_4.rotate(turn=11)

#######################################################
# Kian's code  that puts all triangles together into a blue rectangle goes here ...
# Kian can use methods "shift" and "rotate", as above, to move TRIANGLES
# Hint: it only takes rotation by angles with integer values between 0 and 12
# Full angle = 12, like on the clock
#######################################################

header_txts[0].set_text("PART I: All Triangles Together -> A Rectangle")
header_txts[1].set_text("Area Of Blue Rectangle = " + str("???"))
header_txts[2].set_text("Area Of Red Square = " + str("???"))

show_drawing_and_save_if_needed(block=False)
wait_for_enter()

#######################################################
#######################################################

# turn the square by a magic angle, to make it easy to put together a big square
a_square.rotate(turn = atan_hours(a/b))

#######################################################
# Kian's code that puts [all triangles] + [a square] => [a bigger square] goes here ...
# Kian can use methods "shift" and "rotate", as above, to move TRIANGLES
# Hint: it only takes rotation by angles with integer values between 0 and 12
# Full angle = 12, like on the clock
#######################################################

#a_square.set_style(colour="violet")
header_txts[0].set_text("PART II: A Square + 4 Triangles Together")
header_txts[1].set_text(" -> A Bigger Square")
header_txts[2].set_text("Area Of The Big Mixed Colour Square = " + str("???"))

plt.show(block = not is_running_tests())