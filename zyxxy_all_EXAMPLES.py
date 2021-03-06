#######################################################
## Importing functions that we will use below        ##

import numpy as np
from zyxxy_canvas import create_canvas_and_axes, show_drawing_and_save_if_needed
from zyxxy_shape_style import set_default_patch_style, set_default_outline_style, set_default_line_style, new_layer, get_width, get_height
from zyxxy_shape_functions import draw_a_circle, draw_a_square, draw_a_triangle, draw_an_ellipse, draw_a_rectangle, draw_a_smile, draw_a_segment, draw_a_sector, draw_a_polygon, draw_a_broken_line, draw_a_crescent, draw_a_star
from zyxxy_coordinates import build_an_arc, link_contours, build_a_circle, build_a_zigzag
from zyxxy_shape_functions import shift_layers, turn_layers, stretch_layers
from zyxxy_utils import random_element, random_number

#########################################################
## THE FLAGS                                           ##
#########################################################
def example_japanese_flag(axes=None):
  create_canvas_and_axes(canvas_width=30, canvas_height=20, axes=axes)
  draw_a_circle(centre_x=15, centre_y=10, radius=6, colour='crimson')   
  show_drawing_and_save_if_needed()

def example_belgian_flag(axes=None):
  create_canvas_and_axes(canvas_width=6, canvas_height=4, axes=axes)
  draw_a_square(left=0, bottom=0, side=2, colour='black')
  draw_a_square(left=0, bottom=2, side=2, colour='black')
  draw_a_square(left=2, bottom=0, side=2, colour='yellow')
  draw_a_square(left=2, bottom=2, side=2, colour='yellow')
  draw_a_square(left=4, bottom=0, side=2, colour='red')
  draw_a_square(left=4, bottom=2, side=2, colour='red')
  show_drawing_and_save_if_needed()

def example_cuban_flag(axes=None):
  create_canvas_and_axes(canvas_width=30, canvas_height=20, axes=axes)
  draw_a_rectangle(left=0, centre_y=10, width=30, height=4, colour='blue')
  draw_a_rectangle(left=0, bottom=0, width=30, height=4, colour='blue')
  draw_a_rectangle(left=0, top=20, width=30, height=4, colour='blue')
  draw_a_triangle(tip_x=17, tip_y=10, width=20, height=17, colour='red', turn=9)
  draw_a_star(centre_x=6, centre_y=10, radius_1=3, radius_2=1, ends_qty=5, colour='white') 
  show_drawing_and_save_if_needed()

def example_finnish_flag(axes=None): 
  create_canvas_and_axes(canvas_width=36, canvas_height=22, axes=axes)
  draw_a_rectangle(centre_x=13, bottom=0, width=6, height=22, colour='midnightblue')
  draw_a_rectangle(left=0, centre_y=11, width=36, height=6, colour='midnightblue')
  show_drawing_and_save_if_needed()

def example_japanese_naval_flag(axes=None):
  create_canvas_and_axes(canvas_width=30, canvas_height=20, axes=axes)
  draw_a_circle(centre_x=12, centre_y=10, radius=6, colour='crimson')
  for i in range(32):
    if i % 2 == 0:
      draw_a_triangle(tip_x=12, tip_y=10, height=30, width=6, turn=12/32*i, colour='crimson')
  show_drawing_and_save_if_needed()

def example_british_flag(axes=None):
  create_canvas_and_axes(canvas_width=18, canvas_height=12, axes=axes)

  draw_a_rectangle(centre_x=9, centre_y=6, width=18, height=12, colour='navy')

  draw_a_rectangle(centre_x=9, centre_y=6, width=22, height=3, colour='white', turn=7)
  draw_a_rectangle(centre_x=9, centre_y=6, width=22, height=1, colour='red', turn=7)
  draw_a_rectangle(centre_x=9, centre_y=6, width=22, height=3, colour='white', turn=5)
  draw_a_rectangle(centre_x=9, centre_y=6, width=22, height=1, colour='red', turn=5)

  draw_a_rectangle(centre_x=9, centre_y=6, width=18, height=4, colour='white')
  draw_a_rectangle(centre_x=9, centre_y=6, width=4, height=12, colour='white')
  draw_a_rectangle(centre_x=9, centre_y=6, width=18, height=2, colour='red')
  draw_a_rectangle(centre_x=9, centre_y=6, width=2, height=12, colour='red') 

  show_drawing_and_save_if_needed()


def example_us_flag(axes=None):
  create_canvas_and_axes(canvas_width = 19*13*2, canvas_height = 10*13*2, axes=axes)

  for stripe_nb in range(7):
    draw_a_rectangle(centre_x=19*13, centre_y=10+2*20*stripe_nb, width=19*13*2, height=20, colour='red')
    
  draw_a_rectangle(centre_x=100, centre_y=190, width=200, height=140, colour='navy')   

  for row in range(9): # there are 9 rows of stars
    # let's define how many stars are in this row
    # and where is the centre_x of the first star    
    if row%2==0: # if row number is even
      stars_qty=6
      first_star_centre_x = 15 
    else:        # if row number is odd
      stars_qty=5
      first_star_centre_x = 33 
    # centre_y=260-(row+1)*14 because we are counting star rows from the top
    for column in range(stars_qty):
        draw_a_star(centre_x=first_star_centre_x+column*34, centre_y=260-(row+1)*14, radius_1=9, radius_2=3, ends_qty=5, colour='white') 

  show_drawing_and_save_if_needed()              

#########################################################
## ZYXXY THE MOUSE                                     ##
#########################################################
def example_Zyxxy_the_mouse(axes=None, model="https://i.pinimg.com/564x/35/4c/5c/354c5c04a1f72100ca1b110007730257.jpg",
                           block=False):
  create_canvas_and_axes(canvas_width = 36,
                                canvas_height = 36, 
                                title = "Hello, I am Zyxxy!", 
                                model=model,
                                axes = axes)

  set_default_line_style(linewidth=2)
  #######################################################
  # Now let's draw the shapes!                         ##

  # Let's start with the whiskers! They need to be behind the head, 
  # so we will need to move these lines before the line
  # that draws the head of the mouse!
  draw_a_segment(start_x=18, start_y=12, turn=3, length=6)
  draw_a_segment(start_x=18, start_y=12, turn=4, length=6)
  draw_a_segment(start_x=18, start_y=12, turn=9, length=6)
  draw_a_segment(start_x=18, start_y=12, turn=8, length=6)

  # let's draw the head of the mouse
  draw_a_triangle(tip_x=18, tip_y=6, height=18, width=18, colour='plum')
  # ... and the nose, using a triangle with the same tip
  draw_a_triangle(tip_x=18, tip_y=6, height=3, width=3, colour='black')
  # ... and the ears
  draw_a_circle(centre_x=9, centre_y=24, radius=6, colour='plum')
  draw_a_circle(centre_x=27, centre_y=24, radius=6, colour='plum')
  # ... and the eyes, white circles with black circles on top
  left_eye_white = draw_a_circle(centre_x=15, centre_y=18, radius=2, colour='white')
  right_eye_white= draw_a_circle(centre_x=21, centre_y=18, radius=2, colour='white')
  left_eye_black = draw_a_circle(centre_x=15, centre_y=18, radius=1, colour='black')
  right_eye_black= draw_a_circle(centre_x=21, centre_y=18, radius=1, colour='black')

  show_drawing_and_save_if_needed(block=block)

  eyes = {'left'  : {'black':left_eye_black,  'white':left_eye_white}, 
          'right' : {'black':right_eye_black, 'white':right_eye_white}}

  return eyes

#########################################################
def example_animation_Zyxxy_the_mouse():
  eyes = example_Zyxxy_the_mouse(model=None)

  for eye in eyes.values():
    eye['black'].clip(clip_outline = eye['white'])

  black_eyes = [eye['black'] for eye in eyes.values()]

  nb_shifts = 20
  nb_rolls = 33

  def animate(l):
    # right
    if 0 < l <= nb_shifts:
      for beye in black_eyes:
        beye.shift(shift=[1/nb_shifts, 0])

    # roll
    if nb_shifts < l <= nb_rolls + nb_shifts:
      for eye in eyes.values():
        eye['black'].turn(turn=3/nb_rolls, 
                            diamond_override=eye['white'].diamond_coords)

    # up
    if nb_rolls + nb_shifts < l <= nb_rolls + nb_shifts * 2:
      for beye in black_eyes:
        beye.shift(shift=[0, 1/nb_shifts])

  show_drawing_and_save_if_needed(animation_func = animate,
    nb_of_frames = 1 + 2 * nb_shifts + nb_rolls, animation_interval=1000/24)

#########################################################
## THE PENGUINS                                        ##
#########################################################
def example_penguins(axes=None):
  
  def draw_half_circle(turn, **kwargs):
    draw_a_sector(angle_start=turn, angle_end=turn+6, **kwargs)
  #######################################################
  # Creating the canvas!                               ##  
  create_canvas_and_axes(canvas_width = 320,
                                canvas_height = 180,
                                title = "Penguin Conversation",
                                #tick_step = 10,
                                #model="https://i.pinimg.com/564x/fc/90/7d/fc907dc3638cfd64aa2c3ba56e216b92.jpg",
                                background_colour = 'lightskyblue',
                                axes=axes)

  #######################################################
  # Now let's draw the shapes!                         ##
  # snowflakes
  for s in range(150):
    draw_a_star(centre_x=random_number(max = get_width(axes)), 
                       centre_y=random_number(max = get_height(axes)), 
                       radius_1=1, radius_2=3, ends_qty=8, colour='aliceblue')

  # ice
  ice_colours = ['aliceblue', 'steelblue', 'skyblue']
  for s in range(1500):
    draw_a_triangle(tip_x=random_number(max = get_width(axes)), 
                    tip_y=0.2*random_number(max = get_height(axes)),
                    height=random_number(30), 
                    width=random_number(15), 
                    turn=random_element(range(2, 11)),
                    colour = random_element(ice_colours)) 

  # penguins!

  # the penguin on the left
  # body
  draw_a_circle(centre_x=60, centre_y=40, radius=20, colour='white')
  # feet
  draw_half_circle(centre_x=54, centre_y=16, radius=6, colour='orangered', turn=8.5)
  draw_half_circle(centre_x=66, centre_y=16, radius=6, colour='orangered', turn=9.5)
  # wings
  draw_half_circle(centre_x=31, centre_y=60, radius=30, colour='black', turn=2)
  draw_half_circle(centre_x=89, centre_y=60, radius=30, colour='black', turn=4)
  # head
  draw_a_circle(centre_x=60, centre_y=80, radius=15, colour='black')
  # eyes
  draw_a_circle(centre_x=55, centre_y=85, radius=3, colour=None, outline_colour='white', outline_linewidth=2)
  draw_a_circle(centre_x=65, centre_y=85, radius=3, colour=None, outline_colour='white', outline_linewidth=2)
  # beck
  draw_a_sector(centre_x=58, centre_y=76, angle_start=0, angle_end=3, radius=6, stretch_x=1.5, turn=0.5, colour='orangered')

  # the penguin on the right
  # first foot 
  draw_half_circle(centre_x=270, centre_y=16, radius=6, colour='orangered', turn=9)
  # body - white
  draw_half_circle(centre_x=280, centre_y=50, radius=30, colour='white', turn=5)
  # second foot 
  draw_half_circle(centre_x=280, centre_y=15, radius=6,  colour='orangered', turn=8)
  # body - black
  draw_half_circle(centre_x=290, centre_y=50, radius=30, colour='black', turn=5)
  # beck
  draw_half_circle(centre_x=255, centre_y=75, radius=6, colour='orangered', turn=8 + 1/2)
  # head
  draw_a_circle(centre_x=270, centre_y=80, radius=15, colour='black')
  # an eye
  draw_a_circle(centre_x=263, centre_y=85, radius=3, colour=None, outline_colour='white', outline_linewidth=2)

  show_drawing_and_save_if_needed()


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
                                model = "https://i.pinimg.com/564x/40/9b/98/409b988980f55f10b588a21b28f15665.jpg",
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
    eye_white= draw_a_crescent(ax=axes, centre_x=centre_x, centre_y=90, width=16, depth_1=-8, depth_2=8, colour='white')
    draw_an_ellipse(ax=axes, centre_x=centre_x, centre_y=90, width=8, height=16, colour='BrightGreen', clip_outline = eye_white)
    draw_a_circle(ax=axes, centre_x=centre_x, centre_y=90, radius=3, colour='black', clip_outline = eye_white)
    # the following line is needed for animation
    eyes.append(eye_white)

  # nose
  draw_a_triangle(ax=axes, tip_x=0, tip_y=72, height=8, width=10, colour='BubblePink')

  # smile
  draw_a_segment(ax=axes, start_x=0, start_y=72, length=7, turn=6)
  smile = draw_a_smile(ax=axes, centre_x=0, centre_y=69, depth=4, width=20)

  show_drawing_and_save_if_needed()

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
      stretch_layers(stretch_x=zoom_factor, stretch_y=zoom_factor, diamond=[0, 90])

  show_drawing_and_save_if_needed(filename=filename, animation_func = animate,
    nb_of_frames = 2 * nb_eye_narrowing + 1 + nb_smile + 1 + nb_zoom + 1, animation_interval=100)


#########################################################
## THE CROC                                            ##
#########################################################
def example_croc(axes=None, 
                 model = "https://i.pinimg.com/564x/a5/b7/92/a5b792acaf4c776302be5bd79da8ddbd.jpg"):

  #########################################################
  ## CREATING THE DRAWING!                               ##
  #########################################################
  # Creating the canvas!                                 ##
  axes = create_canvas_and_axes(canvas_width = 190,
                                canvas_height = 100,
                                background_colour = 'PastelBlue', 
                                model = model,
                                model_zoom = 1.7,
                                axes = axes)

  #######################################################
  # Now let's draw the shapes!                         ##
  
  left_body = 45
  bottom_body = 30
  right_body = 120
  right_head = 170
  top_body = 50
  top_head = bottom_body+15
  tail_right = 25 + left_body
  tail_width = 15
  centre_backside = 55
  r_nostrils = 3
  lip_y = 0.5 * (top_head + bottom_body)
  lip_r = 3 
  teeth_length = 5
  nb_teeth = 7
  leg_width = 10
  leg_length = 15
  feet_height = 5
  feel_length = 18
 
  #######################################################
  # Now let's draw the shapes!                         ## 

  set_default_patch_style(colour='BrightGreen')

  # legs 

  leg_layer_nb = new_layer()

  for shift, colour in [[8, 'green'], [-5, 'BrightGreen']]:
    for x in [left_body+10, left_body+55]:
      # draw a leg
      draw_a_rectangle(ax=axes, left=x+shift, top=bottom_body, height=leg_length, width=leg_width, colour=colour)
      # draw a feet
      draw_a_sector(ax=axes, centre_x=x+shift+feel_length/2, centre_y=bottom_body-leg_length, radius=feel_length/2, stretch_y=feet_height/(feel_length/2), angle_start=9, angle_end=15, colour=colour)

  # body

  body_layer_nb = new_layer()

  draw_a_rectangle(ax=axes, left=left_body-0.1, bottom=bottom_body, height=top_body-bottom_body, width=right_body-left_body+0.2)

  # backside
  backside_clip_contour = build_a_circle(radius=centre_backside-bottom_body) + [left_body, centre_backside]
  draw_a_sector( ax=axes, centre_x=left_body, 
                 centre_y=(2*centre_backside-bottom_body-tail_width+top_body)/2, 
                 radius=(2*centre_backside-bottom_body-tail_width+top_body)/2-bottom_body, 
                 radius_2=(2*centre_backside-bottom_body-tail_width-top_body)/2, 
                 angle_start=6, angle_end=12, clip_outline=backside_clip_contour)

  # tail
  draw_a_rectangle(ax=axes, left=left_body-0.1, top=2*centre_backside-bottom_body, height=tail_width, width=tail_right-left_body+0.2)

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
      eyelid = draw_a_crescent(ax=axes, centre_x=eye_x, centre_y=eye_y, width=eyelid_width, depth_1=mid_y, depth_2=mid_y, colour='green')
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
  draw_a_broken_line(ax=axes, contour=lipline, colour='green', linewidth=8)

  upper_jaw_diamond = [right_body-lip_r, lip_y+lip_r]

  show_drawing_and_save_if_needed("croc")

  return leg_layer_nb, body_layer_nb, upper_jaw_layer_nb, eyelids, upper_jaw_diamond

###################################################################################################

def example_animated_croc(axes=None):

  leg_layer_nb, body_layer_nb, upper_jaw_layer_nb, eyelids, upper_jaw_diamond = example_croc(axes=axes, model=None)

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
      turn_layers(turn=one_jaw_turn[t1]*size_turn, diamond=upper_jaw_diamond, layer_nbs=[upper_jaw_layer_nb])
    # jump
    j = t - len(one_jaw_turn) * nb_jaw_openings
    if 0 <= j < len(one_jump) * nb_jumps:
      j1 = j % len(one_jump)
      shift_layers(shift=[0, one_leg_lift[j1]*size_shift], layer_nbs=[leg_layer_nb])
      shift_layers(shift=[0, one_jump[j1]*size_shift]    , layer_nbs=[body_layer_nb, upper_jaw_layer_nb])

  total_frames = len(one_eyelid_blick) * nb_blinks + len(one_jaw_turn) * nb_jaw_openings + len(one_jump) * nb_jumps

  show_drawing_and_save_if_needed(animation_func=animate, nb_of_frames=total_frames)