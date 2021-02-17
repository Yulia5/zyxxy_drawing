#######################################################
## Importing functions that we will use below        ##
from zyxxy_canvas import create_canvas_and_axes, show_drawing_and_save_if_needed
import matplotlib.pyplot as plt


#########################################################
## CREATING THE DRAWING!                               ##
#######################################################
# Creating the canvas!                               ##
ax = create_canvas_and_axes(canvas_width = 12,
                            canvas_height = 10, 
                            title = "Hello, I am Zyxxy!")


plt.show()