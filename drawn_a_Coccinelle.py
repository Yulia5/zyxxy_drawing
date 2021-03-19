from zyxxy_canvas import create_canvas_and_axes, show_drawing_and_save_if_needed
from zyxxy_shape_functions import draw_a_sector, draw_a_circle, draw_an_arc
from zyxxy_utils import asin_hours

# based on https://www.pinterest.com/pin/701013498245673792/
# colours are identified using https://html-color-codes.info/colors-from-image/#
mustard = '#AD7D01'
beige = '#978E85'
brickred = '#830D05'
deepgreen = '#075337'
deepblue = '#134270'
bluegreen = '#002221'
bg_colour = 'oldlace'

#######################################################
# Creating the canvas!                               ##
axes = create_canvas_and_axes(canvas_width = 21,
                              canvas_height = 28,
                              #tick_step = 2,
                              make_symmetric = True,
                              title = "My Coccinelle",
                              model = 'https://assets.catawiki.nl/assets/2020/6/17/c/7/9/c79f120c-acb0-472e-8447-d334163ee436.jpg', 
                              background_colour=bg_colour)


draw_a_sector(ax=axes, centre_x=0, centre_y=0, radius=0, radius_2=3.5, angle_start=0, angle_end= 6, colour=beige)
draw_a_sector(ax=axes, centre_x=0, centre_y=0, radius=0, radius_2=3.5, angle_start=6, angle_end=12, colour=mustard)
draw_a_sector(ax=axes, centre_x=0, centre_y=0, radius=3.5, radius_2=4.5, angle_start=0, angle_end=6, colour=bluegreen)
draw_a_sector(ax=axes, centre_x=0, centre_y=0, radius=4.5, radius_2=6, angle_start=0, angle_end=6, colour=deepblue)

draw_a_sector(ax=axes, centre_x=-2, centre_y=8, radius=2.5, radius_2=4.5, angle_start=5, angle_end=12.5, colour=deepgreen)

draw_a_circle(ax=axes, centre_x=-2, centre_y=8, radius=1.85, colour=brickred)
draw_a_circle(ax=axes, centre_x=0, centre_y=4.5, radius=1.85, colour='black')

for radius in [1.5, 2.5, 3.5, 4.5]:
  angle_to_horizontal = asin_hours(1.25 / radius)
  draw_an_arc(ax=axes, centre_x=0, centre_y=-7.5, radius=radius, angle_start=3-angle_to_horizontal, angle_end=9+angle_to_horizontal, linewidth=9, colour='black', stretch_x=0.95)



#######################################################
# If you need to save it, and an argument filename="my_postcard", or whatever filename you like! ##
show_drawing_and_save_if_needed("MyCoccinelle")