#######################################################
## Importing functions that we will use below        ##
from zyxxy_canvas import create_canvas_and_axes, show_drawing_and_save_if_needed
from zyxxy_shapes_colour_style import set_patch_style, set_outline_style,  set_line_style, new_layer
from zyxxy_shapes_functions import draw_a_circle, draw_a_triangle, draw_an_ellipse, draw_a_rectangle, draw_a_smile, draw_a_segment


#######################################################
## CREATING THE DRAWING!                             ##
#######################################################
## Creating the canvas!                               ##  
axes = create_canvas_and_axes(canvas_width = 120,
                                canvas_height = 120,
                                background_colour = 'lightyellow')
#######################################################
# Now let's draw the shapes!                         ##

# settings
set_outline_style(linewidth=2)
set_line_style(linewidth=2)
set_patch_style(colour='darkorange')

# the ears

draw_a_triangle(ax=axes, tip_x=20, tip_y=114, height=50, width=30, colour='darkorange', turn=4 + 1/2)
draw_a_triangle(ax=axes, tip_x=28, tip_y=106, height=40, width=24, colour='black', turn=4 + 1/2)
draw_a_triangle(ax=axes, tip_x=80, tip_y=114, height=50, width=30, colour='darkorange', turn=7 + 1/2)
draw_a_triangle(ax=axes, tip_x=72, tip_y=106, height=40, width=24, colour='black', turn=7 + 1/2)

# the tail

tail_length = [30, 22, 20, 12, 10]
for i, tl in enumerate(tail_length):
  if i%2 == 0:
    colour='darkorange'
  else:
    colour='black'
  draw_a_triangle(ax=axes, tip_x=88, tip_y=30, height=tl, width=tl/2, colour=colour, turn=7)

# next layer
new_layer()

# body
height_body = [60, 57, 54, 38, 35, 19, 16]
for i, bh in enumerate(height_body):
  if i%2 == 0:
    colour='darkorange'
  else:
    colour='black'
  draw_a_triangle(ax=axes, tip_x=50, tip_y=60, height=bh, width=bh, colour=colour, turn=6)

#head
contour_head = draw_a_circle(ax=axes, centre_x=50, centre_y=85, radius=25, colour='darkorange')

# neck
draw_a_circle(ax=axes, centre_x=50, centre_y=60, radius=1, colour='black')

# stripes on the face

#outlines are not clippable, so we will cancel them for now
set_outline_style(width=0)

# vertical stripes
for c, b in [[40, 101], [45, 100], [50, 101]]:
  draw_a_rectangle(ax=axes, centre_x=c, bottom=b, width=3, height=20, colour='black')#, clip_outline=contour_head)

# horizontal stripes
for c, x in [[70, 16], [75, 15], [80, 18]]:
  draw_a_rectangle(ax=axes, right=50-x, centre_y=c, width=20, height=3, colour='black')#, clip_outline=contour_head)
  draw_a_rectangle(ax=axes, left=50+x, centre_y=c, width=20, height=3, colour='black')#, clip_outline=contour_head)

# adding the outline back
set_outline_style(outline_width=2)

# next layer
new_layer()

# feet
draw_a_triangle(ax=axes, tip_x=38, tip_y=20, height=20, width=20, colour='darkorange', turn=6)
draw_a_triangle(ax=axes, tip_x=62, tip_y=20, height=20, width=20, colour='darkorange', turn=6)

# eyes
for centre_x in [38, 62]:
  draw_a_circle(ax=axes, centre_x=centre_x, centre_y=90, radius=8, colour='white')
  draw_an_ellipse(ax=axes, centre_x=centre_x, centre_y=90, width=8, height=16, colour='springgreen')
  draw_a_circle(ax=axes, centre_x=centre_x, centre_y=90, radius=2, colour='black')

# nose
draw_a_triangle(ax=axes, tip_x=50, tip_y=72, height=8, width=10, colour='pink')

# smile
draw_a_segment(ax=axes, start_x=50, start_y=72, length=7, linewidth=2, colour='black', turn=6)
draw_a_smile(ax=axes, centre_x=50, centre_y=72, depth=-7, width=20)

show_drawing_and_save_if_needed()
