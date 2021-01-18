#####################################################
## don't change this file, please                  ##
#####################################################

import math
import numpy as np
from zyxxy_helpers import sin_hours, cos_hours, vertices_qty_in_circle

def build_arc(centre_x, centre_y, radius_x, radius_y, angle_start, angle_end):
  number_points = int(vertices_qty_in_circle()/12 * (angle_end - angle_start) + 1)
  angle_step = (angle_end - angle_start) / number_points
  angles = [n * angle_step + angle_start for n in range(number_points+1)]
  contour = [[centre_x + radius_x * sin_hours(a),
              centre_y + radius_y * cos_hours(a)] for a in angles]
  return contour

def build_smile(centre_x, bottom_y, top_y, width):
  if abs((top_y-bottom_y)/width) < 0.001: # assume it's a straight line
    result = [[], []]
  else:
    # reusing build_arc
    radius = 0.5 * (width**2 / 4 + (top_y - bottom_y)**2) / (top_y - bottom_y)
    angle = math.degrees(math.asin(min(1.0, width / (2 * radius))))/30 
    result = build_arc(centre_x=centre_x, centre_y=bottom_y+radius, radius_x=radius, radius_y=radius, angle_start=6-angle, angle_end=6+angle)
  # adjusting start and end points to make sure they match the inputs exactly
  result[0] = [centre_x - width/2, top_y]
  result[-1] = [centre_x + width/2, top_y]
  # all done!
  return result

def build_half_ellipse(centre_x, bottom_y, top_y, width):
  # reusing build_arc
  result = build_arc(centre_x=centre_x, centre_y=top_y, radius_x=width/2, radius_y=top_y-bottom_y, angle_start=3, angle_end=9)
  # adjusting start and end points to make sure they match the inputs exactly
  result[0] = [centre_x - width/2, top_y]
  result[-1] = [centre_x + width/2, top_y]
  # all done!
  return result

def build_ellipse_different_speeds(centre_x, centre_y, radius_x, radius_y, start_hour, end_hour, speed_x=1.0, speed_y=1.0):
  step = 1. / (max(abs(speed_x), abs(speed_y)) * vertices_qty_in_circle())
  angles = np.arange(start_hour, end_hour, step)
  all_x = [centre_x + radius_x * sin_hours(a * speed_x) for a in angles]
  all_y = [centre_y + radius_y * cos_hours(a * speed_y) for a in angles]
  contour = zip(all_x, all_y)
  return contour

def build_polygon(centre_x, centre_y, vertices_qty, radius, stretch_x=1.0, stretch_y=1.0):
  angles_indices = range(vertices_qty)
  
  contour = [[centre_x + radius * sin_hours(i * 12 / vertices_qty) * stretch_x, centre_y + radius * cos_hours(i * 12 / vertices_qty) * stretch_y] for i in angles_indices]

  return contour

def build_star(centre_x, centre_y, radius1, radius2, ends_qty, stretch_x=1.0, stretch_y=1.0):
  angles_indices = range(2*ends_qty)
  
  contour = [[centre_x + (radius1 * (i%2 == 0) + radius2  * (i%2 == 1)) * sin_hours(i * 12/(2*ends_qty)) * stretch_x,centre_y + (radius1 * (i%2 == 0) + radius2  * (i%2 == 1))* cos_hours(i * 12/(2*ends_qty)) * stretch_y] for i in angles_indices]

  return contour
