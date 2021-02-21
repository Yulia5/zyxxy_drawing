#######################################################
## Importing functions that we will use below        ##

import numpy as np
from zyxxy_canvas import create_canvas_and_axes, show_drawing_and_save_if_needed
from zyxxy_shape_style import set_default_patch_style, set_default_outline_style, set_default_line_style, new_layer
from zyxxy_shape_functions import draw_a_circle, draw_a_triangle, draw_an_ellipse, draw_a_rectangle, draw_a_smile, draw_a_segment, draw_a_sector, draw_a_polygon, draw_a_broken_line, draw_an_eye
from zyxxy_coordinates import build_an_arc, link_contours, build_an_eye, build_a_circle, build_a_zigzag
from zyxxy_shape_class import shift_layer, rotate_layer, get_all_shapes_in_layers

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
def example_animation_for_Zyxxy_the_mouse(left_eye_white, right_eye_white, left_eye_black, right_eye_black):
  left_eye_black.clip(clip_outline = left_eye_white)
  right_eye_black.clip(clip_outline = right_eye_white)

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
  eyes = []
  for centre_x in [38, 62]:
    eye_white= draw_an_eye(ax=axes, centre_x=centre_x, centre_y=90, depth_1=-8, depth_2=8, colour='white')
    eye_iris = draw_an_ellipse(ax=axes, centre_x=centre_x, centre_y=90, width=8, height=16, colour='BrightGreen')
    eye_pupil= draw_a_circle(ax=axes, centre_x=centre_x, centre_y=90, radius=2, colour='black')
    # the following 3 lines are needed for animation
    eye_iris.clip(clip_outline = eye_white)
    eye_pupil.clip(clip_outline = eye_white)
    eyes.append(eye_white)

  # nose
  draw_a_triangle(ax=axes, tip_x=50, tip_y=72, height=8, width=10, colour='BubblePink')

  # smile
  draw_a_segment(ax=axes, start_x=50, start_y=72, length=7, linewidth=2, turn=6)
  smile = draw_a_smile(ax=axes, centre_x=50, centre_y=72, depth=7, width=20)

  return eyes, smile


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

  backside = draw_a_sector(ax=axes, centre_x=left_body, 
                 centre_y=(2*centre_backside-bottom_body-tail_width+top_body)/2, 
                 radius=(2*centre_backside-bottom_body-tail_width+top_body)/2-bottom_body, 
                 radius_2=(2*centre_backside-bottom_body-tail_width-top_body)/2, 
                 angle_start=6, angle_end=12)

  clip_contour = build_a_circle(radius=centre_backside-bottom_body) + [left_body, centre_backside]
  backside.clip(clip_outline = clip_contour)

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
      mid_y = eye_y + td * eyelid_width / 2
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

  return leg_layer_nb, body_layer_nb, upper_jaw_layer_nb, eyelids, eyelid_width, upper_jaw_diamond


def example_animation_croc(leg_layer_nb, body_layer_nb, upper_jaw_layer_nb, eyelids, eyelid_width, upper_jaw_diamond):

  nb_blinks = 2
  blink_frames = 3

  nb_jaw_openings = 2
  jaw_frames = 3
  max_jaw_opening_angle = 1

  nb_jumps = 2
  prep_jump_frames = 1
  jump_frames = 3 
  size_jump = 20
  nb_wait_frames = 2

  # now for the animation!
  scenarios = {}

  eyelids_all_scenarios = []
  for eyelid_shape_nb in range(blink_frames):
    eyelid_depths=[]
    for eye_x in eyelids:
      for td in [-1, 1]:
        depth_1=td * eyelid_width / 2 * eyelid_shape_nb / (blink_frames-1) 
        eyelid_depths.append(depth_1)
    eyelids_all_scenarios.append(eyelid_depths)

  one_eyelid_blick = [i for i in range(blink_frames)] + [(blink_frames-1-i) for i in range(blink_frames)]
  all_eyelid_blick_scenarios = np.tile(one_eyelid_blick, nb_blinks)

  one_jaw_turn = [-1.] * jaw_frames + [1] * jaw_frames
  scenarios['jaw_turn'] = np.hstack((
    [0] * (all_eyelid_blick_scenarios.size),
    np.tile(one_jaw_turn, nb_jaw_openings)))

  one_jump = ([-1.] * prep_jump_frames + 
              [1] * (prep_jump_frames + jump_frames) + 
              [-1] * (prep_jump_frames + jump_frames) + 
              [1] * prep_jump_frames + 
              [0] * nb_wait_frames)
  scenarios['body_lift'] = np.hstack((
    [0] * scenarios['jaw_turn'].size, 
    np.tile(one_jump, nb_jumps)))

  one_leg_lift = ([0.] * 2 * prep_jump_frames + 
                [1] * jump_frames + 
                [-1] * jump_frames + 
                [0] * (2*prep_jump_frames + nb_wait_frames))
  scenarios['leg_lift'] = np.hstack(([0] * scenarios['jaw_turn'].size,
                                     np.tile(one_leg_lift, nb_jumps)))

  total_nb_of_frames = len(scenarios['leg_lift'])

  for key in scenarios.keys():
    scenarios[key] = np.hstack((scenarios[key], [0] * (total_nb_of_frames - scenarios[key].size)))

  #pad_with_zeros(scenarios['jaw_turn'], total_size=total_nb_of_frames)
  scenarios['jaw_turn'] *= max_jaw_opening_angle / jaw_frames
  scenarios['body_lift']*= size_jump / (prep_jump_frames+jump_frames)
  scenarios['leg_lift'] *= size_jump / (prep_jump_frames+jump_frames)

  def init():
    # return the list of the shapes that are moved by animation
    return get_all_shapes_in_layers(0, 1, 2)

  def animate(i):
    # eyelid blink  
    if i < len(all_eyelid_blick_scenarios):
      for eyelid_nb, eyelid_shape in enumerate(eyelids):
        eyelid_shape.change_parameter(depth_1=eyelids_all_scenarios[i][eyelid_nb])

    # lift legs
    shift_layer(layer_nb=leg_layer_nb, shift=[0, scenarios['leg_lift'][i]])
    # lift body, head & upper jaw
    shift_layer(layer_nb=body_layer_nb, shift=[0, scenarios['body_lift'][i]])
    shift_layer(layer_nb=upper_jaw_layer_nb, shift=[0, scenarios['body_lift'][i]])
    # upper jaw
    rotate_layer(layer_nb=upper_jaw_layer_nb, turn=scenarios['jaw_turn'][i], diamond=upper_jaw_diamond)
    # return the list of the shapes that are moved by animation
    return get_all_shapes_in_layers(0, 1, 2)

  show_drawing_and_save_if_needed( # filename="croc" , 
   animation_func = animate,  animation_init = init, nb_of_frames = total_nb_of_frames
    )