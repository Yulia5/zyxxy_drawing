#######################################################
## Importing functions that we will use below        ##
from zyxxy_canvas import create_canvas_and_axes, show_drawing_and_save_if_needed
from zyxxy_shape_style import set_default_patch_style, set_default_outline_style, set_default_line_style, new_layer
from zyxxy_shape_functions import draw_a_circle, draw_a_triangle, draw_an_ellipse, draw_a_rectangle, draw_a_smile, draw_a_segment


#########################################################
## ZYXXY THE MOUSE                                     ##
#########################################################
def example_Zyxxy_the_mouse(axes=None):

  #########################################################
  ## CREATING THE DRAWING!                               ##
  #########################################################
  # Creating the canvas!                                 ##
  axes = create_canvas_and_axes(canvas_width = 12,
                                canvas_height = 10, 
                                title = "Hello, I am Zyxxy!", 
                                axes = axes)

  set_default_line_style(linewidth=2)
  #######################################################
  # Now let's draw the shapes!                         ##

  # Let's start with the whiskers! They need to be behind the head, 
  # so we will need to move these lines before the line
  # that draws the head of the mouse!
  draw_a_segment(axes, start_x=6, start_y=3, turn=3, length=2)
  draw_a_segment(axes, start_x=6, start_y=3, turn=4, length=2)
  draw_a_segment(axes, start_x=6, start_y=3, turn=9, length=2)
  draw_a_segment(axes, start_x=6, start_y=3, turn=8, length=2)

  # let's draw the head of the mouse
  draw_a_triangle(ax=axes, tip_x=6, tip_y=1, height=6, width=6, colour='plum')
  # ... and the nose, using a triangle with the same tip
  draw_a_triangle(ax=axes, tip_x=6, tip_y=1, height=1, width=1, colour='black')
  # ... and the ears
  draw_a_circle(ax=axes, centre_x=3, centre_y=7, radius=2, colour='plum')
  draw_a_circle(ax=axes, centre_x=9, centre_y=7, radius=2, colour='plum')
  # ... and the eyes, white circles with black circles on top
  draw_a_circle(ax=axes, centre_x=5, centre_y=5, radius=0.8, colour='white')
  draw_a_circle(ax=axes, centre_x=7, centre_y=5, radius=0.8, colour='white')
  draw_a_circle(ax=axes, centre_x=5, centre_y=5, radius=0.5, colour='black')
  draw_a_circle(ax=axes, centre_x=7, centre_y=5, radius=0.5, colour='black')

#########################################################
## YELLOW CAT                                          ##
#########################################################
def example_yellow_cat(axes=None):
  #######################################################
  ## CREATING THE DRAWING!                             ##
  #######################################################
  ## Creating the canvas!                              ##  
  axes = create_canvas_and_axes(canvas_width = 120,
                                canvas_height = 120,
                                background_colour = 'SeaWave', 
                                axes = axes)
  #######################################################
  # Now let's draw the shapes!                         ##

   # settings
  set_default_outline_style(linewidth=2)
  set_default_line_style(linewidth=2)
  set_default_patch_style(colour='Yellow')#darkorange

  # the tail
  tail_length = [30, 22, 20, 12, 10]
  for i, tl in enumerate(tail_length): 
    triangle_tail = draw_a_triangle(ax=axes, tip_x=88, tip_y=30, height=tl, width=tl/2, turn=7)
    if i%2 == 1:
      triangle_tail.set_style(colour='black')


  # body
  height_body = [60, 57, 54, 38, 35, 19, 16]
  for i, bh in enumerate(height_body):
    triangle_body = draw_a_triangle(ax=axes, tip_x=50, tip_y=60, height=bh, width=bh, turn=6)
    if i%2 == 1:
      triangle_body.set_style(colour='black')

  # feet
  draw_a_triangle(ax=axes, tip_x=38, tip_y=20, height=20, width=20, turn=6)
  draw_a_triangle(ax=axes, tip_x=62, tip_y=20, height=20, width=20, turn=6)

  # the ears

  draw_a_triangle(ax=axes, tip_x=20, tip_y=114, height=50, width=30, turn=4 + 1/2)
  draw_a_triangle(ax=axes, tip_x=28, tip_y=106, height=40, width=24, colour='black', turn=4 + 1/2)
  draw_a_triangle(ax=axes, tip_x=80, tip_y=114, height=50, width=30, turn=7 + 1/2)
  draw_a_triangle(ax=axes, tip_x=72, tip_y=106, height=40, width=24, colour='black', turn=7 + 1/2)

  #head
  head_circle = draw_a_circle(ax=axes, centre_x=50, centre_y=85, radius=25)

  #from this line, the default colour is black
  set_default_patch_style(colour='black')

  # neck
  draw_a_circle(ax=axes, centre_x=50, centre_y=60, radius=1)

  # stripes on the face

  stripes = []
  # vertical stripes
  for c, b in [[40, 101], [45, 100], [50, 101]]:
    stripe = draw_a_rectangle(ax=axes, centre_x=c, bottom=b, width=3, height=20)
    stripes += [stripe]

  # horizontal stripes
  for c, x in [[70, 16], [75, 15], [80, 18]]:
    stripe_l = draw_a_rectangle(ax=axes, right=50-x, centre_y=c, width=20, height=3)
    stripe_r = draw_a_rectangle(ax=axes, left=50+x, centre_y=c, width=20, height=3)
    stripes += [stripe_l, stripe_r]

  for stripe in stripes:
    stripe.clip(clip_outline = head_circle)

  # eyes
  for centre_x in [38, 62]:
    draw_a_circle(ax=axes, centre_x=centre_x, centre_y=90, radius=8, colour='white')
    draw_an_ellipse(ax=axes, centre_x=centre_x, centre_y=90, width=8, height=16, colour='BrightGreen')
    draw_a_circle(ax=axes, centre_x=centre_x, centre_y=90, radius=2, colour='black')

  # nose
  draw_a_triangle(ax=axes, tip_x=50, tip_y=72, height=8, width=10, colour='BubblePink')

  # smile
  draw_a_segment(ax=axes, start_x=50, start_y=72, length=7, linewidth=2, turn=6)
  draw_a_smile(ax=axes, centre_x=50, centre_y=72, depth=7, width=20)

  show_drawing_and_save_if_needed("yellow_cat")