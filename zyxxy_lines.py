#####################################################
## don't change this file, please                  ##
#####################################################

from zyxxy_helpers import _draw_broken_line, rotate_point
from zyxxy_settings import set_line_kwarg_default
from zyxxy_outlines import build_arc, build_smile, build_half_ellipse, build_ellipse_different_speeds

def draw_broken_line(ax, points, diamond=None, turn=0, **kwargs):
  _draw_broken_line(ax=ax, contour=points, turn=turn, diamond=diamond, **set_line_kwarg_default(kwargs))

# this function draws a line of a given length in a given turn
# of a given width starting from the diamond point
def draw_line_between_two_points(ax, point_1_x, point_1_y, point_2_x, point_2_y, **kwargs):
  _draw_broken_line(ax=ax, contour=[[point_1_x, point_1_y], 
                                   [point_2_x, point_2_y]],
                   **set_line_kwarg_default(kwargs))

def draw_line(ax, start_x, start_y, length, turn, **kwargs):
  rotated_centre = rotate_point(point=(start_x, start_y+length),
                                diamond=(start_x, start_y), 
                                turn = turn)
  _draw_broken_line(ax=ax, 
                   contour=[[start_x, start_y], 
                            [rotated_centre[0], rotated_centre[1]]],
                   **set_line_kwarg_default(kwargs))

def draw_arc(ax, centre_x, centre_y, radius_x, radius_y, angle_start, angle_end, **kwargs):
  contour = build_arc(centre_x=centre_x, centre_y=centre_y, radius_x=radius_x, radius_y=radius_y, angle_start=angle_start, angle_end=angle_end)
  _draw_broken_line(ax=ax, contour=contour, **set_line_kwarg_default(kwargs))

def draw_smile(ax, centre_x, bottom_y, top_y, width, **kwargs):
  contour = build_smile(centre_x=centre_x, bottom_y=bottom_y, top_y=top_y, width=width)
  _draw_broken_line(ax=ax, contour=contour, diamond=[centre_x, top_y], **set_line_kwarg_default(kwargs))

def draw_half_ellipse_line(ax, centre_x, bottom_y, top_y, width, **kwargs):
  contour = build_half_ellipse(centre_x=centre_x, bottom_y=bottom_y, top_y=top_y, width=width)
  _draw_broken_line(ax=ax, contour=contour, diamond=[centre_x, top_y], **set_line_kwarg_default(kwargs))

def draw_ellipse_line_different_speeds(ax, centre_x, centre_y, radius_x, radius_y, start_hour, end_hour, speed_x=1.0, speed_y=1.0, **kwargs):
  contour = build_ellipse_different_speeds(centre_x=centre_x, centre_y=centre_y, radius_x=radius_x, radius_y=radius_y, start_hour=start_hour, end_hour=end_hour, speed_x=speed_x, speed_y=speed_x)
  _draw_broken_line(ax=ax, contour=contour, diamond=[centre_x, centre_y], **set_line_kwarg_default(kwargs))