#######################################################
## Importing functions that we will use below        ##

import numpy as np
from zyxxy_canvas import create_canvas_and_axes, show_drawing_and_save_if_needed
from zyxxy_shape_style import set_default_patch_style, set_default_outline_style, set_default_line_style, new_layer
from zyxxy_shape_functions import draw_a_circle, draw_a_triangle, draw_an_ellipse, draw_a_rectangle, draw_a_smile, draw_a_segment, draw_a_sector, draw_a_polygon, draw_a_broken_line, draw_an_eye
from zyxxy_coordinates import build_an_arc, link_contours, build_a_circle, build_a_zigzag
from zyxxy_shape_class import shift_layer, rotate_layer, stretch_layer, get_all_polygons_in_layers

#########################################################
## THE FLAGS                                           ##
#########################################################
def example_japanese_flag(axes=None):
  #####################################################
  # Creating the canvas!
  axes = create_canvas_and_axes(canvas_width = 30,
                                canvas_height = 20,
                                axes=axes)

  #######################################################
  # Now let's draw the shapes!                         ##
  draw_a_circle(ax=axes, centre_x=15, centre_y=10, radius=6, colour='crimson')   

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
  left_eye_white = draw_a_circle(ax=axes, centre_x=5, centre_y=5, radius=0.8, colour='white')
  right_eye_white= draw_a_circle(ax=axes, centre_x=7, centre_y=5, radius=0.8, colour='white')
  left_eye_black = draw_a_circle(ax=axes, centre_x=5, centre_y=5, radius=0.5, colour='black')
  right_eye_black= draw_a_circle(ax=axes, centre_x=7, centre_y=5, radius=0.5, colour='black')

  return left_eye_white, right_eye_white, left_eye_black, right_eye_black

#########################################################
## we will call this function if we want to animate Zyxxy
#########################################################
def example_animation_for_Zyxxy_the_mouse(axes=None):
  left_eye_white, right_eye_white, left_eye_black, right_eye_black = example_Zyxxy_the_mouse(axes=axes)
  left_eye_black.clip(clip_outline = left_eye_white)
  right_eye_black.clip(clip_outline = right_eye_white)

#########################################################
## YELLOW CAT                                          ##
#########################################################
def example_yellow_cat(axes=None, cat_colour = 'Yellow', background_colour = 'SeaWave'):
  #######################################################
  ## CREATING THE DRAWING!                             ##
  #######################################################
  ## Creating the canvas!                              ##  
  axes = create_canvas_and_axes(canvas_width = 120,
                                canvas_height = 120,
                                background_colour = background_colour, 
                                axes = axes,
                                make_symmetric = 'x')
  #######################################################
  # Now let's draw the shapes!                         ##

   # settings
  set_default_outline_style(linewidth=2)
  set_default_line_style(linewidth=2)
  set_default_patch_style(colour=cat_colour)#darkorange

  # the tail
  tail_length = [30, 22, 20, 12, 10]
  for i, tl in enumerate(tail_length): 
    triangle_tail = draw_a_triangle(ax=axes, tip_x=38, tip_y=30, height=tl, width=tl/2, turn=7)
    if i%2 == 1:
      triangle_tail.set_style(colour='black')


  # the body
  height_body = [60, 57, 54, 38, 35, 19, 16]
  for i, bh in enumerate(height_body):
    triangle_body = draw_a_triangle(ax=axes, tip_x=0, tip_y=60, height=bh, width=bh, turn=6)
    if i%2 == 1:
      triangle_body.set_style(colour='black')

  # the feet
  draw_a_triangle(ax=axes, tip_x=-12, tip_y=20, height=20, width=20, turn=6)
  draw_a_triangle(ax=axes, tip_x= 12, tip_y=20, height=20, width=20, turn=6)

  head_layer = new_layer()

  # the ears
  et = 4.5
  draw_a_triangle(ax=axes, tip_x=-30, tip_y=114, height=50, width=30, turn=et)
  draw_a_triangle(ax=axes, tip_x=-22, tip_y=106, height=40, width=24, colour='black', turn=et)
  draw_a_triangle(ax=axes, tip_x= 30, tip_y=114, height=50, width=30, turn=-et)
  draw_a_triangle(ax=axes, tip_x= 22, tip_y=106, height=40, width=24, colour='black', turn=-et)

  #head
  head_circle = draw_a_circle(ax=axes, centre_x=0, centre_y=85, radius=25)

  #from this line, the default colour is black
  set_default_patch_style(colour='black')

  # neck
  draw_a_circle(ax=axes, centre_x=0, centre_y=60, radius=1)
  neck_coords = [0, 60]

  # stripes on the face

  # vertical stripes
  for c, b in [[-10, 101], [-5, 100], [0, 101]]:
    draw_a_rectangle(ax=axes, centre_x=c, bottom=b, width=3, height=20, clip_outline = head_circle)

  # horizontal stripes
  for c, x in [[70, 16], [75, 15], [80, 18]]:
    draw_a_rectangle(ax=axes, right=-x, centre_y=c, width=20, height=3, clip_outline = head_circle)
    draw_a_rectangle(ax=axes, left=+x, centre_y=c, width=20, height=3, clip_outline = head_circle)
    
  # eyes
  eyes = []
  for centre_x in [-12, 12]:
    eye_white= draw_an_eye(ax=axes, centre_x=centre_x, centre_y=90, width=16, depth_1=-8, depth_2=8, colour='white')
    draw_an_ellipse(ax=axes, centre_x=centre_x, centre_y=90, width=8, height=16, colour='BrightGreen', clip_outline = eye_white)
    draw_a_circle(ax=axes, centre_x=centre_x, centre_y=90, radius=3, colour='black', clip_outline = eye_white)
    # the following line is needed for animation
    eyes.append(eye_white)

  # nose
  draw_a_triangle(ax=axes, tip_x=0, tip_y=72, height=8, width=10, colour='BubblePink')

  # smile
  draw_a_segment(ax=axes, start_x=0, start_y=72, length=7, turn=6)
  smile = draw_a_smile(ax=axes, centre_x=0, centre_y=69, depth=4, width=20)

  return head_layer, neck_coords, eyes, smile


def example_yellow_cat_animation(axes=None, cat_colour='Yellow', background_colour='SeaWave', filename=None):
  
  head_layer, neck_coords, eyes, smile = example_yellow_cat(axes=axes, cat_colour=cat_colour, background_colour=background_colour)

  #nb_head_tilts = 6
  #angle_one_head_move = 1/12
  nb_eye_narrowing = 6
  depth_diff = 0.5
  nb_smile = 12
  smile_diff = 1/4
  nb_zoom = 4
  zoom_factor = 1.025

  def animate(k):

    # head nods
    #if i < 4 * nb_head_tilts:
    #  turn = angle_one_head_move if (nb_head_tilts <= i < 3*nb_head_tilts) else -angle_one_head_move
    #  rotate_layer(turn=turn, diamond=neck_coords, layer_nbs=[head_layer])
    
    # eye narrowing
    #k = i - 4 * nb_head_tilts
    depth_shifts = [-depth_diff] * nb_eye_narrowing + [depth_diff] * nb_eye_narrowing
    if 0 <= k < 2 * nb_eye_narrowing:
      for eye in eyes:
        eye.shift_shape_parameters(depth_1=-depth_shifts[k], depth_2=depth_shifts[k])

    # smile
    s = k - 2 * nb_eye_narrowing - 1
    if 0 < s <= nb_smile:
      smile.update_shape_parameters(depth=4+s*smile_diff)
      smile.shift(shift=[0, smile_diff])

    # zoom
    z = s - nb_smile - 1
    if 0 < z <= nb_zoom:
      stretch_layer(stretch_x=zoom_factor, stretch_y=zoom_factor, diamond=[0, 90])

  show_drawing_and_save_if_needed(filename=filename, animation_func = animate,
    nb_of_frames = 2 * nb_eye_narrowing + 1 + nb_smile + 1 + nb_zoom + 1, animation_interval=100)


#########################################################
## THE CROC                                            ##
#########################################################
def example_croc(axes=None):

  #########################################################
  ## CREATING THE DRAWING!                               ##
  #########################################################
  # Creating the canvas!                                 ##
  axes = create_canvas_and_axes(canvas_width = 190,
                                canvas_height = 100,
                                background_colour = 'PastelBlue', 
                                axes = axes)

  #######################################################
  # Now let's draw the shapes!                         ##
  
  left_body = 30
  bottom_body = 30
  right_body = 120
  right_head = 180
  top_body = 50
  top_head = bottom_body+15
  tail_right = 35 + left_body
  tail_width = 10
  centre_backside = 50
  r_nostrils = 3
  lip_y = 0.5 * (top_head + bottom_body)
  lip_r = 3 
  teeth_length = 5
  nb_teeth = 7
  leg_width = 10
  leg_length = 15
  feet_height = 5
  feel_length = 20
 
  #######################################################
  # Now let's draw the shapes!                         ## 

  set_default_patch_style(colour='BrightGreen')

  # legs 

  leg_layer_nb = new_layer()

  for shift, colour in [[0, 'green'], [-17, 'BrightGreen']]:
    for x in [50, 100]:
      # draw a leg
      draw_a_rectangle(ax=axes, left=x+shift, top=bottom_body, height=leg_length, width=leg_width, colour=colour)
      # draw a feet
      draw_a_sector(ax=axes, centre_x=x+shift+feel_length/2, centre_y=bottom_body-leg_length, radius=feel_length/2, stretch_y=feet_height/(feel_length/2), angle_start=9, angle_end=15, colour=colour)

  # body

  body_layer_nb = new_layer()

  draw_a_rectangle(ax=axes, left=left_body, bottom=bottom_body, height=top_body-bottom_body, width=right_body-left_body)

  # backside
  backside_clip_contour = build_a_circle(radius=centre_backside-bottom_body) + [left_body, centre_backside]
  draw_a_sector( ax=axes, centre_x=left_body, 
                 centre_y=(2*centre_backside-bottom_body-tail_width+top_body)/2, 
                 radius=(2*centre_backside-bottom_body-tail_width+top_body)/2-bottom_body, 
                 radius_2=(2*centre_backside-bottom_body-tail_width-top_body)/2, 
                 angle_start=6, angle_end=12, clip_outline=backside_clip_contour)

  # tail
  draw_a_rectangle(ax=axes, left=left_body, top=2*centre_backside-bottom_body, height=tail_width, width=tail_right-left_body)

  draw_a_sector(ax=axes, centre_x=tail_right, centre_y=2*centre_backside-bottom_body, radius=tail_width,angle_start=3, angle_end=6)

  # lower teeth and jaw
  upper_teeth = build_a_zigzag(width=right_head - (right_body-lip_r), height=teeth_length, angle_start=3, nb_segments=2*nb_teeth) + [right_body-lip_r, lip_y]

  lower_teeth = upper_teeth[1:-1] + [0, teeth_length]
  draw_a_polygon(ax=axes, contour=lower_teeth, colour='white')

  draw_a_rectangle(ax=axes, left=right_body, bottom=bottom_body, height=lip_y-bottom_body, width=right_head-right_body)

  # upper jaw
  upper_jaw_layer_nb = new_layer()

  draw_a_rectangle(ax=axes, left=right_body, bottom=lip_y, height=top_head-lip_y, width=right_head-right_body)

  # ... and the eyes, white circles with black circles on top
  eye_y = top_body
  for radius, colour in [[8, 'BrightGreen'], [5, 'white'], [3, 'black']]:
    for eye_x in [right_body, right_body+12]:
      draw_a_circle(ax=axes, centre_x=eye_x, centre_y=eye_y, radius=radius, colour=colour)

  # ... and the eyelids. Saving them in array for future use   
  eyelids = []
  eyelid_width = 12
  for eye_x in [right_body, right_body+12]:
    for td in [-1, 1]:
      mid_y = td * eyelid_width / 2
      eyelid = draw_an_eye(ax=axes, centre_x=eye_x, centre_y=eye_y, width=eyelid_width, depth_1=mid_y, depth_2=mid_y, colour='green')
      eyelids.append(eyelid)

  # ... and the nostrils
  nostril_y = top_head
  for nostril_x in [right_head-r_nostrils, right_head-3*r_nostrils]:
    draw_a_circle(ax=axes, centre_x=nostril_x, centre_y=nostril_y, radius=r_nostrils)
    draw_a_circle(ax=axes, centre_x=nostril_x, centre_y=nostril_y, radius=1, colour='green')

  # ... and the teeth and the lip
  # teeth
  draw_a_polygon(ax=axes, contour=upper_teeth, colour='white')
  # upper lip
  lipline_arc = build_an_arc(radius=lip_r, angle_start=6, angle_end=9) + [right_body-lip_r, lip_y+lip_r]
  lipline = link_contours([[right_head, lip_y]], lipline_arc)
  draw_a_broken_line(ax=axes, contour=lipline, colour='green', linewidth=2)

  upper_jaw_diamond = [right_body-lip_r, lip_y+lip_r]

  return leg_layer_nb, body_layer_nb, upper_jaw_layer_nb, eyelids, upper_jaw_diamond


def example_animated_croc(axes=None, filename=None):

  leg_layer_nb, body_layer_nb, upper_jaw_layer_nb, eyelids, upper_jaw_diamond = example_croc(axes=axes)

  nb_blinks = 2
  blink_frames = 6

  nb_jaw_openings = 2
  jaw_frames = 3
  max_jaw_opening_angle = 1

  nb_jumps = 2
  prep_jump_frames = 1
  jump_frames = 3 
  size_jump = 20
  nb_wait_frames = 2

  one_eyelid_blick = [-1.] * blink_frames + [1] * blink_frames
  one_jaw_turn  = [-1.] * jaw_frames + [1] * jaw_frames

  one_jump      = [-1.] * prep_jump_frames + [1] * (prep_jump_frames + jump_frames) 
  one_leg_lift  = [0.] * 2 * prep_jump_frames + [1] * jump_frames
  one_jump     += [-v for v in     one_jump[::-1]] + [0] * nb_wait_frames
  one_leg_lift += [-v for v in one_leg_lift[::-1]] + [0] * nb_wait_frames

  size_shift = size_jump / (prep_jump_frames+jump_frames)
  size_turn =  max_jaw_opening_angle / jaw_frames

  def animate(i):
    # eyelid blink  
    if i < len(one_eyelid_blick) * nb_blinks:
      i2 = i % len(one_eyelid_blick)
      for e, eyelid in enumerate(eyelids):
        depth_change_sign = -1 if e%2 == 0 else 1
        eyelid.shift_shape_parameters(depth_1=depth_change_sign*one_eyelid_blick[i2])
    # jaw turn
    t = i - len(one_eyelid_blick) * nb_blinks
    if 0 <= t < len(one_jaw_turn) * nb_jaw_openings:
      t1 = t % len(one_jaw_turn)
      rotate_layer(turn=one_jaw_turn[t1]*size_turn, diamond=upper_jaw_diamond, layer_nbs=[upper_jaw_layer_nb])
    # jump
    j = t - len(one_jaw_turn) * nb_jaw_openings
    if 0 <= j < len(one_jump) * nb_jumps:
      j1 = j % len(one_jump)
      shift_layer(shift=[0, one_leg_lift[j1]*size_shift], layer_nbs=[leg_layer_nb])
      shift_layer(shift=[0, one_jump[j1]*size_shift]    , layer_nbs=[body_layer_nb, upper_jaw_layer_nb])

  total_frames = len(one_eyelid_blick) * nb_blinks + len(one_jaw_turn) * nb_jaw_openings + len(one_jump) * nb_jumps

  show_drawing_and_save_if_needed(filename=filename, animation_func = animate, nb_of_frames =total_frames)