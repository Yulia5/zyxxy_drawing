
from zyxxy_canvas import create_canvas_and_axes, show_drawing_and_save_if_needed
from zyxxy_shape_functions import draw_a_triangle, draw_a_rectangle, draw_a_star, draw_a_circle, draw_a_crescent, draw_an_ellipse, draw_an_egg, draw_a_segment, draw_an_arc, draw_a_smile, draw_a_polygon
from zyxxy_shape_style import set_default_patch_style, set_default_line_style, set_default_outline_style, new_layer
from zyxxy_colours import create_gradient_colours
from zyxxy_coordinates import build_an_egg
import numpy as np

#######################################################
# Creating the canvas!                               ##
ax = create_canvas_and_axes(  canvas_width = 30,
                              canvas_height = 40,
                              make_symmetric = True,
                              #tick_step = 2,
                              title = "Gradient Cat",
                              background_colour='aliceblue')

set_default_outline_style(linewidth=7)
set_default_line_style(linewidth=7)

body_shape = build_an_egg(power=5, height_widest_point=15, width=20, height=25)
body_shape[:, 1] *= -1

for e_start, p in enumerate(body_shape):
  if p[1] < -0.05:
    break
for e_end, p in enumerate(body_shape):
  if p[1] < -2:
    break

for lr in [-1, 1]:
  print( [3 * lr, 1])
  body_shape[lr*e_start, :] = [-4.5 * lr, 2]  
  print(e_start, e_end)
  body_shape = np.delete(body_shape, np.arange(lr*(e_start+1), lr*e_end, lr), axis=0)

body_shape[:, 1] += 25


body = draw_a_polygon(ax=ax, contour=body_shape, diamond_y=-9)

gradient_colours = create_gradient_colours(rgb_start=(205, 0, 255), rgb_end=[102, 0, 204])
grh = 27 / len(gradient_colours)
for i, gc in enumerate(gradient_colours):
  draw_a_rectangle(ax=ax, width=30, height=grh, centre_x=0, centre_y=18-i*grh, opacity=1, clip_outline=body, colour=gc, outline_linewidth=0, layer_nb=-1)

eye_height = 11
draw_a_segment(ax=ax, start_x=0, start_y=eye_height, turn=6, length=1.5)

aw = 1
wl = 7 # whiskers length
for lr in [-1, 1]:
  draw_a_circle(ax=ax, centre_x=lr*3, centre_y=eye_height, radius=1, colour='black')
  draw_a_smile(ax=ax, centre_x=lr*aw/2, centre_y=eye_height-1.5, width=aw, depth=0.5)

  draw_a_smile(ax=ax, centre_x=lr*(5+wl/2), centre_y=eye_height-0.5, width=wl, depth=-0.5)
  s2 = draw_a_smile(ax=ax, centre_x=lr*(5+wl/2), centre_y=eye_height+0.5, width=wl, depth=-0.5)
  s2.rotate(turn=-lr, diamond_override=[lr*5, eye_height+0.5])

show_drawing_and_save_if_needed()