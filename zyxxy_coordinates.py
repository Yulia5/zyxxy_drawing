########################################################################
## Draw With Zixxy (or Zixxy Drawings, or Drawing With Zyxxy)
## (C) 2021 by Yulia Voevodskaya (draw.with.zyxxy@outlook.com)
## 
##  This program is free software: you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation, either version 3 of the License, or
##  (at your option) any later version.
##  See <https://www.gnu.org/licenses/> for the specifics.
##  
##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License for more details.
########################################################################

import numpy as np
from zyxxy_utils import sin_hours, cos_hours, asin_hours

#####################################################
## contours manipulation                           ##
#####################################################
tolerance = 0.0001

def is_the_same_point(p1, p2):
  sqr_dist = ((p1[0] - p2[0]) ** 2) + ((p1[1] - p2[1]) ** 2) 
  return (sqr_dist < tolerance)

def link_contours(*arg):
  result = []
  for a in arg:
    if (len(a) == 0):
      continue
    if (len(result) == 0):
      result = a
      continue
    if is_the_same_point(p1=result[-1], p2=a[0]):
      result = np.vstack((result[:-1, :], a))
    else:
      result = np.vstack((result, a))
  return result

def add_a_mirror(contour, mirror_x=0):
  reverse_contour = np.copy(contour[::-1, :])
  reverse_contour[:, 0] = 2 * mirror_x - reverse_contour[:, 0]
  result = link_contours(reverse_contour, contour)
  return result

#####################################################
def vertices_qty_in_circle():
  return 60

def build_an_arc(centre_x, centre_y, radius_x, radius_y, angle_start, angle_end):
  _angle_start = angle_start % 12
  _angle_end = angle_end %12
  if _angle_start > _angle_end:
    _angle_end += 12
    
  number_points = int(vertices_qty_in_circle()/12 * (_angle_end - _angle_start) + 1)
  angle_step = (_angle_end - _angle_start) / number_points
  angles = [n * angle_step + _angle_start for n in range(number_points+1)]
  angles[-1] = _angle_end

  contour = np.array([[centre_x + radius_x * sin_hours(a),
              centre_y + radius_y * cos_hours(a)] for a in angles])

  return contour

def build_a_smile(centre_x, bottom_y, top_y, width):
  if abs((top_y-bottom_y)/width) < 0.001: # assume it's a straight line
    result = np.array([[], []])
  else:
    # reusing build_arc
    radius = 0.5 * (width**2 / 4 + (top_y - bottom_y)**2) / (top_y - bottom_y)
    angle = - asin_hours(sin_value = width / (2 * radius))
    result = build_an_arc(centre_x=centre_x, centre_y=bottom_y+radius, radius_x=radius, radius_y=radius, angle_start=6-angle, angle_end=6+angle)
  # adjusting start and end points to make sure they match the inputs exactly
  result[0] = [centre_x - width/2, top_y]
  result[-1] = [centre_x + width/2, top_y]
  # all done!
  return result

def build_a_double_smile(centre_x, width, corners_y, mid1_y, mid2_y): 
  smile1 = build_a_smile(centre_x=centre_x, bottom_y=mid1_y, top_y=corners_y, width=width)
  smile2 = build_a_smile(centre_x=centre_x, bottom_y=mid2_y, top_y=corners_y, width=width)
  result = link_contours(smile1, smile2[::-1])
  return result

def build_a_half_ellipse(centre_x, bottom_y, top_y, width):
  # reusing build_arc
  result = build_an_arc(centre_x=centre_x, centre_y=top_y, radius_x=width/2, radius_y=top_y-bottom_y, angle_start=3, angle_end=9)
  # adjusting start and end points to make sure they match the inputs exactly
  result[0] = [centre_x - width/2, top_y]
  result[-1] = [centre_x + width/2, top_y]
  # all done!
  return result

def build_an_ellipse_with_different_speeds(centre_x, centre_y, radius_x, radius_y, angle_start, angle_end, speed_x=1.0, speed_y=1.0):
  step = 1. / (max(abs(speed_x), abs(speed_y)) * vertices_qty_in_circle())
  angles = np.arange(angle_start, angle_end, step)

  contour = np.array([[centre_x + radius_x * sin_hours(a * speed_x), centre_y + radius_y * cos_hours(a * speed_y)] for a in angles])

  return contour

def build_a_regular_polygon(centre_x, centre_y, vertices_qty, radius):
  angles_indices = range(vertices_qty)
  
  contour = np.array([[centre_x + radius * sin_hours(i * 12 / vertices_qty), centre_y + radius * cos_hours(i * 12 / vertices_qty)] for i in angles_indices])

  return contour

def build_a_star(centre_x, centre_y, radius1, radius2, ends_qty):
  angles_indices = range(2*ends_qty)
  
  contour = np.array([[centre_x + (radius1 * (i%2 == 0) + radius2  * (i%2 == 1)) * sin_hours(i * 12/(2*ends_qty)), centre_y + (radius1 * (i%2 == 0) + radius2  * (i%2 == 1))* cos_hours(i * 12/(2*ends_qty))] for i in angles_indices])

  return contour
