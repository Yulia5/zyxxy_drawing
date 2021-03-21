from zyxxy_canvas import create_canvas_and_axes, show_drawing_and_save_if_needed
from zyxxy_shape_functions import *
from zyxxy_shape_style import set_default_patch_style, set_default_outline_style, set_default_line_style, new_layer

width = 48
height= 27
height_ground = 5
height_grass = 12
aquarium_side = 15
fish_body_length = 8
stripe_radius = 10
stalk_depth = 1
stalk_width = 5 
leaf_width = 3

#######################################################
# Creating the canvas!                               ##
axes = create_canvas_and_axes(canvas_width = width,
                              canvas_height = height,
                              # tick_step = 2,
                              title = "Happy Nowruz 1400!")

#######################################################
# Now let's draw the shapes!                         ##
# grass
for i in range(25):
  draw_a_triangle(ax=axes, tip_x=aquarium_side+2+i/3, tip_y=height_ground+height_grass, width=0.5, height=height_grass, colour='springgreen', turn=6, opacity=0.7)

set_default_outline_style(linewidth=2)

# a table
draw_a_rectangle(ax=axes, left=0, bottom=0, width=width, height=height_ground, colour='MidBrown') 

# an aquarium
draw_a_square(ax=axes, left=0, bottom=height_ground, side=aquarium_side, colour='PastelBlue')

# fish
draw_a_crescent(ax=axes, centre_x=10, centre_y=13, width=8, depth_1=1, depth_2=-1, colour='orange')
draw_a_triangle(ax=axes, tip_x=6, tip_y=13, width=1, height=2, turn=9, colour='orange')
draw_a_circle(ax=axes, centre_x=12, centre_y=13, radius=.3, colour='black', outline_linewidth=0)

# an egg
an_egg = draw_an_egg(ax=axes, power=3, height_widest_point=3, width=4, height=5, tip_x=30, tip_y = height_ground, colour='crimson')
draw_a_sector(ax=axes, centre_x=30, centre_y=stripe_radius+(3+height_ground), angle_start=3, angle_end=9, radius=stripe_radius, radius_2=stripe_radius+1, colour='Yellow', clip_outline=an_egg)


# an apple = two eggs, a smile and an eye
for x in [40-0.75, 40+0.75]:
  draw_an_egg(ax=axes, power=3, height_widest_point=3, width=4, height=5, tip_x=x, tip_y=height_ground, colour='greenyellow', outline_linewidth=4, layer_nb=2)
draw_a_smile(ax=axes, centre_x=40+stalk_depth, centre_y=5+height_ground, width=stalk_width, depth=stalk_depth, turn=3, colour='black', linewidth=5)
draw_a_crescent(ax=axes, centre_x=40+stalk_depth+leaf_width/2, centre_y=5+height_ground+stalk_width/2, width=leaf_width, depth_1=1, depth_2=-1, colour='green', opacity=0.7)

#######################################################
# If you need to save it, and an argument filename="my_postcard", or whatever filename you like! ##
show_drawing_and_save_if_needed()