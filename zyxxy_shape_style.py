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
from matplotlib.colors import is_color_like
from MY_zyxxy_SETTINGS import my_colour_palette, my_default_colour_etc_settings, my_default_diamond_size, default_outlines_width, default_outlines_widthlayer_nb
from zyxxy_utils import raise_Exception_if_not_processed

########################################################################
# as defined by matplotlib
capstyle_types = ['butt', 'round', 'projecting']
joinstyle_types= ['round', 'miter', 'bevel']

########################################################################

line_arg_types = ["colour", "layer_nb", "linewidth", "joinstyle", "capstyle"]
patch_arg_types= ["colour", "layer_nb", "opacity"]

format_arg_dict = { "line"    : line_arg_types, 
                    "patch"   : patch_arg_types, 
                    "outline" : line_arg_types,
                    "diamond" : patch_arg_types }

_default_arguments = my_default_colour_etc_settings
__diamond_size_factor = 1.

##################################################################
## CANVAS HELPERS                                               ## 
##################################################################
def get_width(ax=None):
  if ax is None:
    ax = plt.gca()
  xlims = ax.set_xlim()
  return (xlims[1] - xlims[0])

def get_height(ax=None):
  if ax is None:
    ax = plt.gca()
  ylims = ax.set_ylim()
  return (ylims[1] - ylims[0])

##################################################################
## DIAMOND HELPERS                                              ## 
##################################################################

def set_diamond_size_factor(value=1.):
  global __diamond_size_factor
  __diamond_size_factor = float(value)

def get_diamond_size(ax):
  return get_width(ax=ax) * my_default_diamond_size * __diamond_size_factor

##################################################################
## COLOUR HELPERS                                               ## 
##################################################################

# Find colour that should be used. 
# Assume that it's a name of a standard colour.
# Attention, names are case-sensitive
def find_colour_code(colour_name):
  if colour_name is None:
    return 'none'
  if colour_name in my_colour_palette:
    return my_colour_palette[colour_name] 

  if not is_color_like(colour_name):
    raise Exception(colour_name, "is not a valid colour!")
  return colour_name

########################################################################

OUTLINES_COLOUR = None

def set_outlines_colour(val):
  global OUTLINES_COLOUR
  OUTLINES_COLOUR = val

########################################################################

def extract_colour_etc_kwargs(kwargs):
  possible_keys = line_arg_types + patch_arg_types + ["outline_" + a for a in line_arg_types] + ["diamond_" + a for a in patch_arg_types]
 
  result = {key : value for key, value in kwargs.items() if key in possible_keys}
  return result

def set_line_style(something, **kwargs):

    something.set_fc('none')
    if OUTLINES_COLOUR is not None:
      something.set_linestyle('--')
      something.set_ec(OUTLINES_COLOUR)
      something.set_lw(default_outlines_width)
      something.set_zorder(default_outlines_widthlayer_nb)
    else:
      something.set_linestyle('solid')
      if "colour" in kwargs:
        something.set_ec(find_colour_code( kwargs['colour'] ))
      if "linewidth" in kwargs:
        something.set_lw(kwargs['linewidth'])
      if "layer_nb" in kwargs:
        something.set_zorder(kwargs['layer_nb'])

    if "joinstyle" in kwargs:
      something.set_joinstyle(kwargs['joinstyle'])
    if 'capstyle' in kwargs:
      something.set_capstyle(kwargs['capstyle'])

def set_patch_style(something, **kwargs):

    if "colour" in kwargs:
      this_colour = find_colour_code( kwargs['colour'] )
      if OUTLINES_COLOUR is None:
        something.set_ec('none')
        something.set_fc(this_colour)
      else:
        something.set_fc('none')
        something.set_ec(OUTLINES_COLOUR)
        something.set_lw(default_outlines_width)
        something.set_linestyle('--')
        something.set_zorder(default_outlines_widthlayer_nb)
    
    something.set_lw(_default_arguments['line']['linewidth'])

    if "layer_nb" in kwargs:
      something.set_zorder(kwargs['layer_nb'])

    if OUTLINES_COLOUR is not None:
      if "opacity" in kwargs:
        something.set_alpha(kwargs['opacity'])


########################################################################

def new_layer():
  args_for_layer = ["line", "patch", "outline"]
  new_layer_nb = 1 + max([_default_arguments[fa]['layer_nb'] for fa in args_for_layer])
  for fa in args_for_layer: 
    _default_arguments[fa]['layer_nb'] = new_layer_nb
  return new_layer_nb

def set_default_line_style(**kwargs):
  _set_default_style(what='line', **kwargs)

def set_default_patch_style(**kwargs):
  _set_default_style(what='patch', **kwargs)
                
def set_default_outline_style(**kwargs):
  _set_default_style(what='outline', **kwargs)
 
def _set_default_style(what, **kwargs):
  global _default_arguments
  raise_Exception_if_not_processed(kwarg_keys=kwargs.keys(), 
                                   allowed_keys=_default_arguments[what].keys())
  for ua in kwargs.keys():
    _default_arguments[what][ua] = kwargs[ua]

