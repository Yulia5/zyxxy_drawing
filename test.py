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

import matplotlib.pyplot as plt
from zyxxy_widgets import get_axes_for_widget
from matplotlib.widgets import Slider

ax = plt.axes([0.2, 0.2, 1 - 0.3, 1 - 0.3])

def change_angle(angle):
  print(angle)


##########################################################################################
def add_a_slider(w_left, w_bottom, w_caption, s_vals, on_click_or_change=None):
  _, sax = get_axes_for_widget(w_left=w_left, 
                               w_bottom=w_bottom)
  result = Slider(ax=sax, label=w_caption, valmin=s_vals[0], valmax=s_vals[1], valinit=s_vals[2], valstep=s_vals[3], color='black')

  if on_click_or_change is not None:
    result.on_changed(on_click_or_change)


init_angle = 7

w_left=.2
w_bottom=0.1
w_caption='angle' 
s_vals=[0, 36, init_angle, 1] 
on_click_or_change=change_angle

def as2(w_left, w_bottom, w_caption, s_vals, on_click_or_change):

  sax = plt.axes([0.02, 0.5, 0.3,  0.1])
  result = Slider(ax=sax, label=w_caption, valmin=0, valmax=36, valinit=3, valstep=1, color='black')

  if on_click_or_change is not None:
    result.on_changed(on_click_or_change)

  return result

r = as2(w_left=w_left, w_bottom=w_left, w_caption=w_caption, s_vals=s_vals, on_click_or_change=on_click_or_change)


add_a_slider(w_left=.7, w_bottom=.1, w_caption='angle2', s_vals=[0, 36, init_angle, 1])#, on_click_or_change=change_angle)



plt.gcf().set_dpi(100) 
plt.gcf().set_size_inches([10, 8])
plt.show()