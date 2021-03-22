
from zyxxy_canvas import create_canvas_and_axes, show_drawing_and_save_if_needed
from zyxxy_shape_functions import draw_a_triangle, draw_a_rectangle, draw_a_star, draw_a_circle, draw_a_crescent, draw_an_ellipse, draw_an_egg, draw_a_segment
from zyxxy_shape_style import set_default_patch_style, set_default_line_style, set_default_outline_style, new_layer

#######################################################
# Creating the canvas!                               ##
ax = create_canvas_and_axes(  canvas_width = 30,
                              canvas_height = 20,
                              make_symmetric = 'x',
                              #tick_step = 2,
                              title = "Excited Cat",
                              model = 'https://i.pinimg.com/564x/de/21/fd/de21fdb9fa70d9d54ce7e4c0f07910d5.jpg',
                              background_colour='aliceblue')

#######################################################
# Now let's draw the shapes!                         ##

# the body
set_default_patch_style(colour="yellow", layer_nb=2)
set_default_outline_style(linewidth=4,   layer_nb=1)

body = draw_an_egg(ax=ax, power=3, height_widest_point=3, width=4, height=5, tip_x=0, tip_y=14, stretch_x=3, stretch_y=-3)

for y in [1.5, 6, 10.5]:  
  draw_a_rectangle(ax=ax, width=16, height=2, centre_x=0, centre_y=y, opacity=0.3, clip_outline=body, colour='orange', outline_linewidth=0)

# the head

set_default_patch_style(  layer_nb=4)
set_default_outline_style(layer_nb=3)

head = draw_a_circle(ax=ax, centre_x=0, centre_y=14, radius=4.2)

# the ears, using the "eye" shape
draw_a_crescent(ax=ax, width=6, depth_1=1, depth_2=3, centre_x=-4, centre_y=16, turn=9)
draw_a_crescent(ax=ax, width=6, depth_1=1, depth_2=3, centre_x=4, centre_y=16, turn=3)

new_layer()

# the stripes
for y in [10.5, 15]:  
  draw_a_rectangle(ax=ax, width=16, height=2, centre_x=0, centre_y=y, opacity=0.3, clip_outline=head, colour='orange', outline_linewidth=0)

# change outlines style
set_default_outline_style(linewidth=2)

# the eyes
eye_height = 15
for centre_x in [-2, 2]:
  draw_a_crescent(ax=ax, centre_x=centre_x, centre_y=eye_height, width=2, depth_1=-1, depth_2=1, colour='white')
  draw_an_ellipse(ax=ax, centre_x=centre_x, centre_y=eye_height, width=1, height=2, colour='red')
  draw_a_circle(ax=ax, centre_x=centre_x, centre_y=eye_height, radius=0.5, colour='black')

draw_a_triangle(ax=ax, width=2, height=1, tip_x=0, tip_y=eye_height-2.5, colour='black')
draw_a_segment(ax=ax, start_x= 2, start_y=eye_height-2, turn=3, length=3.5)
draw_a_segment(ax=ax, start_x= 2, start_y=eye_height-3, turn=4, length=3.5)
draw_a_segment(ax=ax, start_x=-2, start_y=eye_height-2, turn=9, length=3.5)
draw_a_segment(ax=ax, start_x=-2, start_y=eye_height-3, turn=8, length=3.5)

# the mouth
draw_a_crescent(ax=ax, width=2, depth_1=1, depth_2=1.5, centre_x=0, centre_y=12.5, colour='pink')

draw_a_star(ax=ax, centre_x=-8, centre_y=18, radius_1=3, radius_2=1, ends_qty=8, colour='red')

show_drawing_and_save_if_needed(filename="PopCat")