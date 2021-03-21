
from zyxxy_canvas import create_canvas_and_axes, show_drawing_and_save_if_needed
from zyxxy_shape_functions import draw_a_rectangle, draw_a_circle, draw_an_ellipse, draw_an_egg, draw_an_arc, draw_a_smile, draw_a_polygon, draw_a_segment
from zyxxy_shape_style import set_default_line_style, set_default_outline_style
from zyxxy_colours import create_gradient_colours
from zyxxy_coordinates import build_an_egg, build_an_arc, link_contours
import numpy as np

#######################################################
# Creating the canvas!                               ##
ax = create_canvas_and_axes(  canvas_width = 30,
                              canvas_height = 40,
                              make_symmetric = True,
                              #tick_step = 2,
                              title = "Gradient Cat",
                              background_colour='aliceblue')

set_default_outline_style(linewidth=7*2)
set_default_line_style(linewidth=7)

body_height=25
eye_y = 11
ear_height = 2
aw = 1
whiskers_length = 7 # whiskers length
body_bottom = -9
tail_height = 3
tail_coeff = 1.5

tail_arc_1 = build_an_arc(angle_start=0, angle_end=6, radius=1)
tail_arc_1[:, 0] *= 5
tail_arc_1[:, 1] *= tail_height

tail_shape = link_contours(tail_arc_1, tail_arc_1[::-1, :] * tail_coeff) + [5, body_bottom]
tail = draw_a_polygon(ax=ax, contour=tail_shape)

# body shape
body_shape = build_an_egg(power=5, height_widest_point=-15, width=20, height=-body_height)

for e_start, p in enumerate(body_shape):
  if p[1] < -0.05:
    break
for e_end, p in enumerate(body_shape):
  if p[1] < -2:
    break

for lr in [-1, 1]:
  body_shape[lr*e_start, :] = [-4.5 * lr, ear_height]
  body_shape = np.delete(body_shape, np.arange(lr*(e_start+1), lr*e_end, lr), axis=0)

body_shape[:, 1] += body_height + body_bottom

body = draw_a_polygon(ax=ax, contour=body_shape)

#gradient rectangles
gradient_colours = create_gradient_colours(rgb_start=[255, 0, 255], rgb_end=(0, 0, 255))
gradient_bottom = body_bottom - tail_coeff * tail_height
grh = (ear_height + body_height + tail_coeff * tail_height) / len(gradient_colours)
for i, gc in enumerate(gradient_colours):
  draw_a_rectangle(ax=ax, width=30, height=grh, centre_x=0, centre_y=gradient_bottom+i*grh, opacity=1, clip_outline=body, colour=gc, outline_linewidth=0)
  draw_a_rectangle(ax=ax, width=30, height=grh, centre_x=0, centre_y=gradient_bottom+i*grh, opacity=1, clip_outline=tail_shape, colour=gc, outline_linewidth=0)

# a vertical line
draw_a_segment(ax=ax, start_x=0, start_y=eye_y, turn=6, length=1.5)

for lr in [-1, 1]:
  # an eye
  draw_a_circle(ax=ax, centre_x=lr*3, centre_y=eye_y, radius=1, colour='black')

  # mouth
  draw_a_smile(ax=ax, centre_x=lr*aw/2, centre_y=eye_y-1.5, width=aw, depth=0.5)

  # whiskers
  draw_a_smile(ax=ax, centre_x=lr*(5+whiskers_length/2), centre_y=eye_y-0.5, width=whiskers_length, depth=-0.5)
  s2 = draw_a_smile(ax=ax, centre_x=lr*(5+whiskers_length/2), centre_y=eye_y+0.5, width=whiskers_length, depth=-0.5)
  s2.rotate(turn=-lr, diamond_override=[lr*5, eye_y+0.5])

show_drawing_and_save_if_needed()