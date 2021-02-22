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

demo_screen_zoom = 1/2

figure_params = {'canvas_width' : 16, 
                 'canvas_height' : 10,
                 'figsize' : [10 / demo_screen_zoom, 7.5 / demo_screen_zoom],
                 'dpi' : 75,
                 'tick_step' : 1,
                 'font_size' : 10/demo_screen_zoom,
                 'widget_lefts' : {'left': 0.15, 'right' : 0.65},
                 'plot_gap' : 0.05,
                 'plot_bottom_gap' : 0.01}

widget_params = {'radio_width' : 0.2,
                 'radio_side_margin' : 0.025,
                 'radio_gap' : 0.2,
                 'height' : 0.0239,
                 'width' : 0.3,
                 'gap' : 0.01}

style_params = {"line" : {'colour' : 'black', 
                                    'linewidth' : 2, 'joinstyle' : 'miter', 'zorder' : 1,
                               "capstyle" : 'round'}, 
                          "patch" : {'alpha' : 0.5, 
                                     'zorder' : 1, 
                                     'colour' : 'none'},
                          "outline" : {'colour' : 'black', 
                                       'linewidth' : 2, 
                                       'joinstyle' : 'miter', 
                                       'zorder' : 1,
                                       "capstyle" : 'round'},
                          "diamond" : {
                                  'colour' : 'green', #  None #
                                  'alpha' : 1.0,
                                  'zorder' : 1000}}

my_default_demo_colours = {"left" : {"shape" : 'red', 'diamond' : 'red'},
                           "right" : {"shape" : 'blue', 'diamond' : 'blue'}}