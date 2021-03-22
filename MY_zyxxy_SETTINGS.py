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
                     'BrightGreen': "#24ff24",
                     'Yellow'     : "#ffff6d"}

# Colours, alphas and linewidths!
my_default_colour_etc_settings = {
                     "line" : {'colour' : 'black', 
                               'linewidth' : 2, 
                               'joinstyle' : 'miter', 
                               'layer_nb' : 1,
                               "capstyle" : 'round'}, 
                     "patch" : {'opacity' : 1.0, 
                                'layer_nb' : 1, 
                                'colour' : 'none'},
                     "outline" : {'colour' : 'black', 
                                  'linewidth' : 0, 
                                  'joinstyle' : 'miter', 
                                  'layer_nb' : 1},
                     "diamond" : {'colour' : 'cyan', #  None #
                                  'opacity' : 1.0,
                                  'layer_nb' : 1000}}

my_default_diamond_size = 0.015 
default_outlines_width = 10 
default_outlines_layer_nb = 501       

# Font sizes and adjustment needed to fit them
my_default_font_sizes = {'title'      : 18/screen_zoom,
                         'axes_label' : 14/screen_zoom,
                         'tick'       :  8/screen_zoom}

# Figure sizes (in inches) and DPIs  
# Figure size in pixels is DPI * figure size in inches

my_default_display_params = {'max_figsize' : [5/screen_zoom, 5.5/screen_zoom],
                             'dpi' : 100,
                             'margin_side' : 0.5 }
my_default_image_params = {'dpi'     : 50,
                           'format'  : 'png'}

my_default_animation_params = {'dpi'     : 70,
                               'interval': 200,
                               'blit'    : True,
                               'repeat'  : False,
                               'FPS'     : 5,
                               'writer'  : 'ffmpeg',
                               'format'  : 'mp4'}