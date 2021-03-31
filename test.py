
from zyxxy_canvas import create_canvas_and_axes, show_drawing_and_save_if_needed
from zyxxy_shape_functions import draw_a_wave, clone_a_shape, draw_a_segment

#######################################################
# Creating the canvas!                               ##
create_canvas_and_axes(canvas_width = 10,
                              canvas_height = 10,
                              tick_step = 2,
                              make_symmetric = True
                              )

w1 = draw_a_wave(start_x=0, start_y=0, width=1, height=2, angle_start=0, nb_waves=1, colour='red', turn=0)

w2 = draw_a_wave(start_x=0, start_y=0, width=1, height=2, angle_start=0, nb_waves=1, colour='blue', turn=9)

w8 = draw_a_wave(start_x=0, start_y=0, width=1, height=2, angle_start=0, nb_waves=1, colour='purple', flip_upside_down=True, turn=3)

w3 = clone_a_shape(w1)
w3.turn(9)
w3.shift([2, 2])
w3.set_style(colour="green")

show_drawing_and_save_if_needed()