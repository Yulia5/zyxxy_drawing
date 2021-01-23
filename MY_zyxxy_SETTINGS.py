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

# There are 148 beautiful pre-defined colours!
# You can find them here:
# https://matplotlib.org/3.3.3/gallery/color/named_colors.html
#
# If this is not enough,
# you can save your favourite colours here!
# Try to give them names different from ...
# ... the names of standard colours
my_colour_palette = {'Bubble_blue'     : '#0099ff', 
                     'Light_pink'      : '#ff8888'}

# Colours, alphas and linewidths!
my_default_colour_etc_settings = {
                     "line" : {'colour' : 'black', 
                                    'linewidth' : 2, 'joinstyle' : 'miter', 'zorder' : 1}, 
                     "patch" : {'alpha' : 1.0, 
                                     'zorder' : 1, 
                                     'colour' : 'none'},
                     "patch_outline" : {'colour' : 'black', 
                                             'linewidth' : 0, 
                                             'joinstyle' : 'miter', 
                                             'zorder' : 1}}

# Diamond parameters!
# Diamonds don't move when you turn the shapes
my_default_diamond_size = 15
my_default_diamond_colour = 'green' #  None # 

# Font sizes and adjustment needed to fit them
my_default_title_font_size = 18
my_default_axes_label_font_size = 14
my_default_axes_tick_font_size = 10
my_default_margin_adjustments = {'top' : 0.85, 
                                 'bottom' : 0.20}

# Default format of image file 
my_default_image_format = "png"
# Figure sizes (in inches) and DPIs  
# Figure size in pixels is DPI * figure size in inches
my_default_figsize = [6, 4]
my_default_dpi = 75

my_default_image_file_figsize =  [3.6, 2.4]
my_default_image_file_dpi = 200

my_default_animation_file_figsize =  [3.6, 2.4]
my_default_animation_file_dpi = 200
my_default_animation_interval = 200
my_default_animation_blit = True
my_default_animation_repeat = False
my_default_animation_FPS = 5

my_default_demo_canvas_size = [16, 10]
my_default_demo_figsize = [6, 5]
my_default_demo_dpi = 75
my_default_demo_tick_step = 1

my_default_demo_params = {"line" : {'colour' : 'black', 
                                    'linewidth' : 2, 'joinstyle' : 'miter', 'zorder' : 1}, 
                          "patch" : {'alpha' : 0.5, 
                                     'zorder' : 1, 
                                     'colour' : 'red'},
                          "patch_outline" : {'colour' : 'black', 
                                             'linewidth' : 2, 
                                             'joinstyle' : 'miter', 
                                             'zorder' : 1}}