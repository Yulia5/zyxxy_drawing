#######################################################
## Importing functions that we will use below        ##
from zyxxy_canvas import create_canvas_and_axes, show_drawing_and_save_if_needed
from zyxxy_shapes import draw_a_circle, draw_a_rectangle, draw_a_sector, draw_a_polygon, draw_a_double_smile
from zyxxy_lines import draw_a_broken_line
from zyxxy_coordinates import build_an_arc, link_contours, build_a_double_smile
from zyxxy_settings import new_layer
from zyxxy_helpers import shift_layer, rotate_layer, get_all_shapes_in_layers, set_xy
import numpy as np

#########################################################
## CREATING THE DRAWING!                               ##
#######################################################
# Creating the canvas!                               ##
ax = create_canvas_and_axes(canvas_width = 190,
                            canvas_height = 100,
                            background_colour = 'skyblue')

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

# legs
for shift, colour in [[0, 'green'], [-17, 'lime']]:
  for x in [50, 100]:
    x_coord = x + shift
    # draw a leg
    draw_a_rectangle(ax=ax, left_x=x_coord, top_y=bottom_body, height=leg_length, width=leg_width, colour=colour)
    # draw a feet
    draw_a_sector(ax=ax, centre_x=x_coord+feel_length/2, centre_y=bottom_body-leg_length, radius=feel_length/2, stretch_y=feet_height/(feel_length/2), angle_start=9, angle_end=3, colour=colour)

new_layer()

# body
draw_a_rectangle(ax=ax, left_x=left_body, bottom_y=bottom_body, height=top_body-bottom_body, width=right_body-left_body, colour='lime')

# backside
draw_a_sector(ax=ax, centre_x=left_body, centre_y=centre_backside, radius=centre_backside-bottom_body,angle_start=6, angle_end=12, colour='lime')

# tail
draw_a_rectangle(ax=ax, left_x=left_body, top_y=2*centre_backside-bottom_body, height=tail_width, width=tail_right-left_body, colour='lime')

draw_a_sector(ax=ax, centre_x=tail_right, centre_y=2*centre_backside-bottom_body, radius=tail_width,angle_start=3, angle_end=6, colour='lime')

draw_a_circle(ax=ax, centre_x=left_body, centre_y=(2*centre_backside-bottom_body-tail_width+top_body)/2, radius=(2*centre_backside-bottom_body-tail_width-top_body)/2, colour='skyblue')

# lower teeth and jaw
teeth_x = np.linspace(right_body-lip_r, right_head, 2*nb_teeth+1)
upper_teeth = np.array([[teeth_x[t], lip_y - (t%2) * teeth_length] for t in range(2*nb_teeth+1)])
lower_teeth = link_contours(upper_teeth[1:,:] + [0, teeth_length], [[teeth_x[-1], lip_y]])
draw_a_polygon(ax=ax, contour=lower_teeth, colour='white')

draw_a_rectangle(ax=ax, left_x=right_body, bottom_y=bottom_body, height=lip_y-bottom_body, width=right_head-right_body, colour='lime')

new_layer()

# upper jaw
draw_a_rectangle(ax=ax, left_x=right_body, bottom_y=lip_y, height=top_head-lip_y, width=right_head-right_body, colour='lime')

# ... and the eyes, white circles with black circles on top
eye_y = top_body
for radius, colour in [[8, 'lime'], [5, 'white'], [3, 'black']]:
  for eye_x in [right_body, right_body+12]:
    draw_a_circle(ax=ax, centre_x=eye_x, centre_y=eye_y, radius=radius, colour=colour)
# ... and the eyelids. Saving them in array for future use   
eyelids = []
eyelid_width = 12
for eye_x in [right_body, right_body+12]:
  for td in [-1, 1]:
    mid_y = eye_y + td * eyelid_width / 2
    eyelid = draw_a_double_smile(ax=ax, centre_x=eye_x, width=eyelid_width, corners_y=eye_y, mid1_y=mid_y, mid2_y=mid_y, colour='green')
    eyelids.append(eyelid)

# ... and the nostrils
nostril_y = top_head
for nostril_x in [right_head-r_nostrils, right_head-3*r_nostrils]:
  draw_a_circle(ax=ax, centre_x=nostril_x, centre_y=nostril_y, radius=r_nostrils, colour='lime')
  draw_a_circle(ax=ax, centre_x=nostril_x, centre_y=nostril_y, radius=1, colour='green')

# ... and the teeth and the lip
# teeth
draw_a_polygon(ax=ax, contour=upper_teeth, colour='white')
# upper lip
lipline_top = build_an_arc(centre_x=right_body-lip_r, centre_y=lip_y+lip_r, radius_x=lip_r, radius_y=lip_r, angle_start=6, angle_end=9)
lipline_top = link_contours([[right_head, lip_y]], lipline_top)
draw_a_broken_line(ax=ax, points=lipline_top, colour='green', linewidth=2)

# now for the animation!
scenarios = {}

eyelid_outlines_all_scenarios = []
for eyelid_shape_nb in range(blink_frames):
  eyelid_outlines = []
  for eye_x in [right_body, right_body+12]:
    for td in [-1, 1]:
      eyelid_outline = build_a_double_smile(centre_x=eye_x, width=eyelid_width, corners_y=eye_y, 
      mid1_y=eye_y + td * eyelid_width / 2, 
      mid2_y=eye_y + td * eyelid_width / 2 * eyelid_shape_nb / (blink_frames-1))
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
      set_xy(something=eyelid_shape, 
             xy=eyelid_outlines_this_scenario[eyelid_nb])
  # lift legs
  shift_layer(layer_nb=0, shift=[0, scenarios['leg_lift'][i]])
  # lift body, head & upper jaw
  shift_layer(layer_nb=1, shift=[0, scenarios['body_lift'][i]])
  shift_layer(layer_nb=2, shift=[0, scenarios['body_lift'][i]])
  # upper jaw
  rotate_layer(layer_nb=2, turn=scenarios['jaw_turn'][i], diamond=[right_body-lip_r, lip_y+lip_r])
  # return the list of the shapes that are moved by animation
  return get_all_shapes_in_layers(0, 1, 2)

show_drawing_and_save_if_needed(filename="croc" 
  , animation_func = animate,  animation_init = init, nb_of_frames = total_nb_of_frames
  )