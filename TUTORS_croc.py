#######################################################
## Importing functions that we will use below        ##
import numpy as np

from zyxxy_canvas import create_canvas_and_axes, show_drawing_and_save_if_needed
from zyxxy_shape_functions import draw_a_circle, draw_a_rectangle, draw_a_sector, draw_a_polygon, draw_an_eye, draw_a_broken_line
from zyxxy_coordinates import build_an_arc, link_contours, build_an_eye, build_a_circle, build_a_zigzag
from zyxxy_shape_style import new_layer, set_default_patch_style
from zyxxy_shape_class import shift_layer, rotate_layer, get_all_shapes_in_layers


#########################################################
## CREATING THE DRAWING!                               ##
#######################################################
# Creating the canvas!                               ##
ax = create_canvas_and_axes(canvas_width = 190,
                            canvas_height = 100,
                            background_colour = 'PastelBlue')

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

set_default_patch_style(colour='BrightGreen')

# legs

leg_layer_nb = new_layer()

for shift, colour in [[0, 'green'], [-17, 'BrightGreen']]:
  for x in [50, 100]:
    # draw a leg
    draw_a_rectangle(ax=ax, left=x+shift, top=bottom_body, height=leg_length, width=leg_width, colour=colour)
    # draw a feet
    draw_a_sector(ax=ax, centre_x=x+shift+feel_length/2, centre_y=bottom_body-leg_length, radius=feel_length/2, stretch_y=feet_height/(feel_length/2), angle_start=9, angle_end=15, colour=colour)

# body

body_layer_nb = new_layer()

draw_a_rectangle(ax=ax, left=left_body, bottom=bottom_body, height=top_body-bottom_body, width=right_body-left_body)

# backside

backside = draw_a_sector(ax=ax, centre_x=left_body, 
centre_y=(2*centre_backside-bottom_body-tail_width+top_body)/2, 
radius=(2*centre_backside-bottom_body-tail_width+top_body)/2-bottom_body, 
radius_2=(2*centre_backside-bottom_body-tail_width-top_body)/2, 
angle_start=6, angle_end=12)

clip_contour = build_a_circle(radius=centre_backside-bottom_body) + [left_body, centre_backside]
backside.clip(clip_outline = clip_contour)

# tail
draw_a_rectangle(ax=ax, left=left_body, top=2*centre_backside-bottom_body, height=tail_width, width=tail_right-left_body)

draw_a_sector(ax=ax, centre_x=tail_right, centre_y=2*centre_backside-bottom_body, radius=tail_width,angle_start=3, angle_end=6)

# lower teeth and jaw
upper_teeth = build_a_zigzag(width=right_head - (right_body-lip_r), height=teeth_length, angle_start=3, nb_segments=2*nb_teeth) + [right_body-lip_r, lip_y]

lower_teeth = upper_teeth[1:-1] + [0, teeth_length]
draw_a_polygon(ax=ax, contour=lower_teeth, colour='white')

draw_a_rectangle(ax=ax, left=right_body, bottom=bottom_body, height=lip_y-bottom_body, width=right_head-right_body)

# upper jaw

upper_jaw_layer_nb = new_layer()

draw_a_rectangle(ax=ax, left=right_body, bottom=lip_y, height=top_head-lip_y, width=right_head-right_body)

# ... and the eyes, white circles with black circles on top
eye_y = top_body
for radius, colour in [[8, 'BrightGreen'], [5, 'white'], [3, 'black']]:
  for eye_x in [right_body, right_body+12]:
    draw_a_circle(ax=ax, centre_x=eye_x, centre_y=eye_y, radius=radius, colour=colour)

# ... and the eyelids. Saving them in array for future use   
eyelids = []
eyelid_width = 12
for eye_x in [right_body, right_body+12]:
  for td in [-1, 1]:
    mid_y = eye_y + td * eyelid_width / 2
    eyelid = draw_an_eye(ax=ax, centre_x=eye_x, centre_y=eye_y, width=eyelid_width, depth_1=mid_y, depth_2=mid_y, colour='green')
    eyelids.append(eyelid)

# ... and the nostrils
nostril_y = top_head
for nostril_x in [right_head-r_nostrils, right_head-3*r_nostrils]:
  draw_a_circle(ax=ax, centre_x=nostril_x, centre_y=nostril_y, radius=r_nostrils)
  draw_a_circle(ax=ax, centre_x=nostril_x, centre_y=nostril_y, radius=1, colour='green')

# ... and the teeth and the lip
# teeth
draw_a_polygon(ax=ax, contour=upper_teeth, colour='white')
# upper lip
lipline_arc = build_an_arc(radius=lip_r, angle_start=6, angle_end=9) + [right_body-lip_r, lip_y+lip_r]
lipline = link_contours([[right_head, lip_y]], lipline_arc)
draw_a_broken_line(ax=ax, contour=lipline, colour='green', linewidth=2)

# now for the animation!
scenarios = {}

eyelid_outlines_all_scenarios = []
for eyelid_shape_nb in range(blink_frames):
  eyelid_outlines = []
  for eye_x in [right_body, right_body+12]:
    for td in [-1, 1]:
      eyelid_outline = build_an_eye(width=eyelid_width,  
      depth_1=eye_y + td * eyelid_width / 2, 
      depth_2=eye_y + td * eyelid_width / 2 * eyelid_shape_nb / (blink_frames-1)) + [eye_x, eye_y]
      eyelid_outlines.append(eyelid_outline)
  eyelid_outlines_all_scenarios.append(eyelid_outlines)

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
scenarios['leg_lift'] = np.hstack((
[0] * scenarios['jaw_turn'].size,
np.tile(one_leg_lift, nb_jumps)))

total_nb_of_frames = len(scenarios['leg_lift'])

for key in scenarios.keys():
  scenarios[key] = np.hstack((scenarios[key], 
  [0] * (total_nb_of_frames - scenarios[key].size)))

#pad_with_zeros(scenarios['jaw_turn'], total_size=total_nb_of_frames)
scenarios['jaw_turn'] *= max_jaw_opening_angle / jaw_frames
scenarios['body_lift']*= size_jump / (prep_jump_frames+jump_frames)
scenarios['leg_lift'] *= size_jump / (prep_jump_frames+jump_frames)

def init():
  # return the list of the shapes that are moved by animation
  return get_all_shapes_in_layers(0, 1, 2)

def animate(i):
  # eyelid blink  
  if i < all_eyelid_blick_scenarios.size:
    eyelid_outlines_this_scenario = eyelid_outlines_all_scenarios[all_eyelid_blick_scenarios[i]]
    for eyelid_nb, eyelid_shape in enumerate(eyelids):
      try:
        set_xy(something=eyelid_shape, 
             xy=eyelid_outlines_this_scenario[eyelid_nb])
      except:
        raise Exception((eyelid_shape))
  # lift legs
  shift_layer(layer_nb=leg_layer_nb, shift=[0, scenarios['leg_lift'][i]])
  # lift body, head & upper jaw
  shift_layer(layer_nb=body_layer_nb, shift=[0, scenarios['body_lift'][i]])
  shift_layer(layer_nb=upper_jaw_layer_nb, shift=[0, scenarios['body_lift'][i]])
  # upper jaw
  rotate_layer(layer_nb=upper_jaw_layer_nb, turn=scenarios['jaw_turn'][i], diamond=[right_body-lip_r, lip_y+lip_r])
  # return the list of the shapes that are moved by animation
  return get_all_shapes_in_layers(0, 1, 2)

show_drawing_and_save_if_needed(filename="croc" 
 # , animation_func = animate,  animation_init = init, nb_of_frames = total_nb_of_frames
  )