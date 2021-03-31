
from zyxxy_canvas import create_canvas_and_axes, show_drawing_and_save_if_needed
from zyxxy_shape_functions import draw_a_wave, clone_a_shape, draw_a_segment
import numpy as np
from zyxxy_utils import wait_for_enter

#######################################################
# Creating the canvas!                               ##
create_canvas_and_axes(canvas_width = 10,
                              canvas_height = 10,
                              tick_step = 2,
                              make_symmetric = True
                              )

w1 = draw_a_wave(start_x=0, start_y=0, width=1, height=2, angle_start=0, nb_waves=1, colour='red', turn=0)

w2 = draw_a_wave(start_x=0, start_y=0, width=1, height=2, angle_start=0, nb_waves=1, colour='blue', turn=9) # draw_a_segment(start_x=0, start_y=0, length=1, colour='blue', turn=9) # 

w8 = draw_a_wave(start_x=0, start_y=0, width=1, height=2, angle_start=0, nb_waves=1, colour='purple', flip_upside_down=True, turn=3)

w3 = clone_a_shape(w1)
w3.turn(9)
w3.shift([2, 2])
w3.set_style(colour="green")


for z in np.arange(2, 5, 0.1):
  w2.update_shape_parameters(angle_start=3-z, width=z, nb_waves=z/2) # length=z)#
  print(w2.move_matrix) 
  print(w2.get_xy())

  #w2.shift_to([z-5, z-5])
  #w2.stretch(stretch_x=1+.1/z)
  wait_for_enter()

show_drawing_and_save_if_needed()