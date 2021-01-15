#####################################################
## don't change this file, please                  ##
#####################################################

from zyx_helpers import fill_in_outline, vertices_qty_in_circle
from zyx_settings import set_fill_in_outline_kwarg_defaults
from zyx_outlines import build_smile, build_star, build_polygon

# this function draws a rectangle
# diamond point is at the bottom left vertice
def draw_rectangle(ax, width, height, left_x=None, centre_x=None, right_x=None, bottom_y=None, centre_y=None, top_y=None, diamond=None, **kwargs):

  # checking that we the right number of inputs
  how_many_are_defined = {'x' : (left_x is not None) + (centre_x is not None) + (right_x is not None), 'y' :  (bottom_y is not None) + (centre_y is not None) + (top_y is not None)}
  errorMsg = '; '.join('One and only one ' + key + ' coordinate should be defined, but ' + str(value) + ' are defined' for key, value in how_many_are_defined.items() if value != 1)
  if errorMsg != '':
    raise Exception(errorMsg)

  diamond_best_guess = [None, None]
  # defining coordinates that are undefined - x
  if left_x is not None:
    centre_x = left_x + width / 2
    right_x = left_x + width
    diamond_best_guess[0] = left_x
  else:
    if centre_x is not None:
      left_x = centre_x - width / 2
      right_x = centre_x + width / 2
      diamond_best_guess[0] = centre_x
    elif right_x is not None:
      left_x = right_x - width
      centre_x = right_x - width / 2  
      diamond_best_guess[0] = right_x

  # defining coordinates that are undefined - y
  if bottom_y is not None:
    centre_y = bottom_y + height / 2
    top_y = bottom_y + height
    diamond_best_guess[1] = bottom_y
  else:
    if centre_y is not None:
      bottom_y = centre_y - height / 2
      top_y = centre_y + height / 2
      diamond_best_guess[1] = centre_y
    elif top_y is not None:
      bottom_y = top_y - height
      centre_y = top_y - height / 2 
      diamond_best_guess[1] = top_y

  # ... and the diamond          
  if diamond is None:
    diamond = diamond_best_guess
  kwargs['diamond'] = diamond

  all_x = [left_x, right_x, right_x, left_x]
  all_y = [bottom_y, bottom_y, top_y, top_y]  

  contour = fill_in_outline(ax=ax, all_x=all_x, all_y=all_y, **set_fill_in_outline_kwarg_defaults(kwargs))

  return contour

# draw a square, default side = 1, the simplest polygon!
def draw_square(ax, left_x, bottom_y, side=1, **kwargs):
  contour = draw_rectangle(ax=ax, left_x=left_x, bottom_y=bottom_y, height=side, width=side, **kwargs)

  return contour

# this function draws a symmetrical (isosceles) triangle
# diamond point is at the tip point
# if not rotated, the tip is pointing down
def draw_triangle(ax, tip_x, tip_y, height, width, **kwargs):
  all_x = [tip_x-width/2, tip_x, tip_x+width/2]
  all_y = [tip_y+height, tip_y, tip_y+height]
  contour = fill_in_outline(ax=ax, all_x=all_x, all_y=all_y, diamond=(tip_x, tip_y), **set_fill_in_outline_kwarg_defaults(kwargs))

  return contour

# this function that draws a star
# its diamond point is in the centre
def draw_star(ax, centre_x, centre_y, radius1, radius2, ends_qty, stretch_x=1.0, stretch_y=1.0, diamond=None, **kwargs): 

  contour_init = build_star(centre_x=centre_x, centre_y=centre_y, radius1=radius1, radius2=radius2, ends_qty=ends_qty, stretch_x=stretch_x, stretch_y=stretch_y)

  if diamond is None:
    diamond=(centre_x, centre_y)

  contour = fill_in_outline(ax=ax, all_x=[c[0] for c in contour_init], all_y=[c[1] for c in contour_init], diamond=diamond, **set_fill_in_outline_kwarg_defaults(kwargs))

  return contour

# a polygon is a special case of a star (when radiuses are equal), so we will reuse that function
# its diamond point is in the centre (same as the star)
def draw_polygon(ax, centre_x, centre_y, radius, 
vertices_qty, stretch_x=1.0, stretch_y=1.0, diamond=None, **kwargs):
  contour_init = build_polygon(centre_x=centre_x, centre_y=centre_y, radius=radius, vertices_qty=vertices_qty, stretch_x=stretch_x, stretch_y=stretch_y) 

  if diamond is None:
    diamond=(centre_x, centre_y)

  contour = fill_in_outline(ax=ax, all_x=[c[0] for c in contour_init], all_y=[c[1] for c in contour_init], diamond=diamond, **set_fill_in_outline_kwarg_defaults(kwargs))

  return contour

# a polygon with 60 vertices looks very similar to a circle
# possible to increase the number of vertices if needed
# its diamond point is in the centre (same as the star)
def draw_ellipse(ax, centre_x, centre_y, radius, stretch_x=1.0, stretch_y=1.0, diamond=None, **kwargs):
  contour = draw_polygon(ax=ax, centre_x=centre_x, centre_y=centre_y, radius=radius, vertices_qty=vertices_qty_in_circle(), stretch_x=stretch_x, stretch_y=stretch_y, diamond=diamond, **kwargs)

  return contour

# a circle is a special case of an ellipse
def draw_circle(ax, centre_x, centre_y, radius, diamond=None, **kwargs):
  contour = draw_ellipse(ax=ax, centre_x=centre_x, centre_y=centre_y, radius=radius, stretch_x=1.0, stretch_y=1.0, diamond=diamond, **kwargs)

  return contour 

# this function that draws a star
# its diamond point is in the centre
def draw_double_smile(ax, centre_x, width, corners_y, mid1_y, mid2_y, **kwargs): 
  smile1 = build_smile(centre_x=centre_x, bottom_y=mid1_y, top_y=corners_y, width=width)
  smile2 = build_smile(centre_x=centre_x, bottom_y=mid2_y, top_y=corners_y, width=width)
  contour_init = smile1[:-1] + smile2[::-1]

  contour = fill_in_outline(ax=ax, all_x=[c[0] for c in contour_init], all_y=[c[1] for c in contour_init], diamond=(centre_x, corners_y), **set_fill_in_outline_kwarg_defaults(kwargs))

  return contour

def draw_rhombus(ax, centre_x, centre_y, width, height, diamond=None, **kwargs):
  contour = draw_star(ax=ax, centre_x=centre_x, centre_y=centre_y, radius1=height/2, radius2=width/2, ends_qty=2, stretch_x=1.0, stretch_y=1.0, diamond=diamond, **kwargs)

  return contour