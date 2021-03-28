from zyxxy_canvas import create_canvas_and_axes
from zyxxy_shape_functions import draw_a_circle
import math
from zyxxy_utils import wait_for_enter
import numpy as np

#######################################################
# Creating the canvas!                               ##
create_canvas_and_axes(canvas_width = 24,
                              canvas_height = 24,
                              #tick_step = 1,
                              make_symmetric = True,
                              title = "Circle Puzzle (Pythagoras Helps!)")

draw_a_circle(centre_x=0, centre_y=0, radius=10, colour='crimson')

wait_for_enter()
print("Now we will let's draw some circles ")

for cx in np.arange(-9, 9.1, 0.2): # cx = -9, -8.8, -8.6, -8.4, -8.2, ... 
  draw_a_circle(centre_x=cx, centre_y=0, radius=1, colour='gold', opacity=0.3)
  draw_a_circle(centre_x=cx, centre_y=0, radius=1, colour='gold', opacity=0.3)

wait_for_enter()
