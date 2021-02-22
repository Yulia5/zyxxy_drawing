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

screen_zoom = 1/2

# There are 148 beautiful pre-defined colours!
# You can find them here:
# https://matplotlib.org/stable/gallery/color/named_colors.html
#
# If this is not enough,
# you can save your favourite colours here!
# Try to give them names different from ...
# ... the names of standard colours
my_colour_palette = {'DarkTeal'   : "#004949",
                     'SeaWave'    : "#009292",
                     'BubblePink' : "#ff6db6",
                     'LightPink'  : "#ffb6db",
                     'Purple'     : "#490092",
                     'RoyalBlue'  : "#006ddb",
                     'Hyacinth'   : "#b66dff",
                     'PastelBlue' : "#6db6ff",
                     'LightBlue'  : "#b6dbff",
                     'Burgundy'   : "#920000",
                     'MidBrown'   : "#924900",
                     'LightBrown' : "#db6d00",
                     'BrightGreen':"#24ff24",
                     'Yellow'     : "#ffff6d"}

# Colours, alphas and linewidths!
my_default_colour_etc_settings = {
                     "line" : {'colour' : 'black', 
                               'linewidth' : 2, 
                               'joinstyle' : 'miter', 
                               'zorder' : 1,
                               "capstyle" : 'round'}, 
                     "patch" : {'alpha' : 1.0, 
                                'zorder' : 1, 
                                'colour' : 'none'},
                     "outline" : {'colour' : 'black', 
                                             'linewidth' : 0, 
                                             'joinstyle' : 'miter', 
                                             'zorder' : 1,
                                 "capstyle" : 'round'},
                     "diamond" : {'colour' : 'blue', #  None #
                                  'alpha' : 1.0,
                                  'zorder' : 1000}} 

my_default_background_settings =  {'fc' : 'none', 
                                   'ec' : 'none',
                                   'zorder' : -1000,
                                   'alpha' : 1}   

my_default_diamond_size = 0.015         

# Font sizes and adjustment needed to fit them
my_default_font_sizes = {'title'      : 18/screen_zoom,
                         'axes_label' : 14/screen_zoom,
                         'tick'       :  8/screen_zoom}

# Figure sizes (in inches) and DPIs  
# Figure size in pixels is DPI * figure size in inches

my_default_display_params = {'figsize' : [6/screen_zoom, 4/screen_zoom],
                             'dpi' : 75,
                             'margin_adjustments' : {'top'    : 0.85, 
                                                     'bottom' : 0.20,
                                                     'hspace' : 0.3}}

my_default_image_params = {'figsize' : [3.6, 2.4], 
                           'dpi'     : 200,
                           'format'  : 'png'}

my_default_animation_params = {'figsize' : [3.6, 2.4],
                               'dpi'     : 200,
                               'interval': 200,
                               'blit'    : True,
                               'repeat'  : False,
                               'FPS'     : 5,
                               'writer'  : 'ffmpeg',
                               'format'  : 'mp4'}