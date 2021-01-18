#####################################################
## don't change this file, please                  ##
#####################################################

from zyxxy_utils import cos_hours, sin_hours
import numpy as np 
import matplotlib.lines

def rotate_point(point, diamond, turn):
  if diamond is None:
    return point
  return [diamond[0] + (point[0] - diamond[0]) * cos_hours(turn) + (point[1] - diamond[1]) * sin_hours(turn),
          diamond[1] - (point[0] - diamond[0]) * sin_hours(turn) + (point[1] - diamond[1]) * cos_hours(turn)] 

def get_xy(something):
  if isinstance(something, np.ndarray):
    return something
  elif isinstance(something, matplotlib.lines.Line2D):
    return something.get_xydata()
  else:
    return something.get_xy()

def set_xy(something, xy):
  if isinstance(something, np.ndarray):
    something = xy
  elif isinstance(something, matplotlib.lines.Line2D):
    something.set_xdata(xy[:, 0])
    something.set_ydata(xy[:, 1])
  else:
    something.set_xy(xy)
  return something

def shift_something(something, shift):
  xy = get_xy(something=something)
  xy += shift
  set_xy(something=something, xy=xy)
  return xy

def rotate_something(something, turn, diamond):
  xy = get_xy(something=something)

  if (diamond is not None) and (turn is not None) and (turn != 0):      xy = np.array([rotate_point(point=point, diamond=diamond,turn=turn) for point in xy])

  set_xy(something=something, xy=xy)
  return xy

def stretch_something(something, diamond, stretch_x, stretch_y):
  xy = get_xy(something=something)

  if diamond is not None:
    if stretch_x is not None and (stretch_x != 1.):
      xy[:, 0] = diamond[0] + (xy[:, 0] - diamond[0]) * stretch_x 
    if stretch_y is not None and (stretch_y != 1.):
      xy[:, 1] = diamond[1] + (xy[:, 1] - diamond[1]) * stretch_y

  set_xy(something=something, xy=xy)
  return xy