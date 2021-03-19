
from zyxxy_canvas import create_canvas_and_axes, show_drawing_and_save_if_needed
from zyxxy_all_EXAMPLES import example_us_flag
from zyxxy_shape_functions import draw_a_star, draw_a_rectangle
from zyxxy_shape_style import set_diamond_size_factor

#######################################################
# Creating the canvas!                               ##
ax = create_canvas_and_axes(  canvas_width = 19*13*2,
                              canvas_height = 10*13*2,
                              tick_step = 50,
                              title = "Flag Of The U.S.A.",
                              model = example_us_flag,
                              outlines_colour = "cyan")

set_diamond_size_factor(0.75)

#######################################################
# Now let's draw the shapes!                         ##
for stripe_nb in range(3):
  draw_a_rectangle(ax=ax, left=0, centre_y=15+30*stripe_nb, width=19*13*2, height=15, colour='red')
    
draw_a_rectangle(ax=ax, left=0, centre_y=190, width=90, height=80, colour='navy')   

for row in range(7): # there are 9 rows of stars
  # let's define how many stars are in this row
  # and where is the centre_x of the first star    
  if row%2==0: # if row number is even
    stars_qty=9
    first_star_centre_x = 15 
  else:        # if row number is odd
    stars_qty=8
    first_star_centre_x = 33 
  # centre_y=260-(row+1)*14 because we are counting star rows from the top
  for column in range(stars_qty):
    draw_a_star(ax=ax, centre_x=first_star_centre_x+column*40, centre_y=260-(row+1)*20, radius_1=18, radius_2=6, ends_qty=5, colour='skyblue')               

show_drawing_and_save_if_needed()