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
import matplotlib.lines, matplotlib.patches
import matplotlib.pyplot as plt
from matplotlib.colors import is_color_like
from MY_zyxxy_SETTINGS import my_colour_palette, my_default_demo_params, my_default_colour_etc_settings, my_default_diamond_size

########################################################################

line_arg_types = ["colour", "linewidth", "joinstyle", "zorder"]
patch_arg_types = ["colour", "alpha", "zorder"]

format_arg_dict = { "line"    : line_arg_types, 
                    "patch"   : patch_arg_types, 
                    "outline" : line_arg_types,
                    "diamond" : patch_arg_types}

_default_arguments = my_default_colour_etc_settings
_show_diamond = True

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
## MOVEMENT HELPERS                                             ## 
##################################################################
def _get_xy(something):
  if isinstance(something, np.ndarray):
    return something
  elif isinstance(something, matplotlib.lines.Line2D):
    return something.get_xydata()
  elif isinstance(something, matplotlib.patches.Polygon):
    return something.get_xy()
  raise Exception("Data type ", type(something), " is not handled")

def _set_xy(something, xy):
  if isinstance(something, np.ndarray):
    something = xy
  elif isinstance(something, matplotlib.lines.Line2D):
    something.set_xdata(xy[:, 0])
    something.set_ydata(xy[:, 1])
  elif isinstance(something, matplotlib.patches.Polygon):
    something.set_xy(xy)
  else:
    raise Exception("Data type ", type(something), " is not handled")
  return something

##################################################################
## DIAMOND HELPERS                                              ## 
##################################################################

def set_diamond_style(show):
  global _show_diamond
  _show_diamond = show

def get_diamond_size(ax):
  return get_width(ax=ax) * my_default_diamond_size * int(_show_diamond)

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

def get_default_arguments(defaults_for_demo):
  if defaults_for_demo:
    defaults_to_use = my_default_demo_params
  else:
    defaults_to_use = _default_arguments
  return defaults_to_use

def extract_colour_etc_kwargs(kwargs):
  possible_keys = line_arg_types + patch_arg_types + ["outline_" + a for a in line_arg_types] + ["diamond_" + a for a in patch_arg_types]
 
  result = {key : value for key, value in kwargs.items() if key in possible_keys}
  return result

def _set_line_style(something, **kwargs):

    something.set_fc('none')
    something.set_linestyle('solid') # 'dotted'
    if "colour" in kwargs:
      something.set_ec(find_colour_code( kwargs['colour'] ))
    if "zorder" in kwargs:
      something.set_zorder(kwargs['zorder'])

    if "linewidth" in kwargs:
      something.set_lw(kwargs['linewidth'])
    if "joinstyle" in kwargs:
      something.set_joinstyle(kwargs['joinstyle'])

def _set_patch_style(something, **kwargs):

    something.set_ec('none')
    if "colour" in kwargs:
      something.set_fc(find_colour_code( kwargs['colour'] ))
    if "zorder" in kwargs:
      something.set_zorder(kwargs['zorder'])
    if "alpha" in kwargs:
      something.set_alpha(kwargs['alpha'])


########################################################################

def new_layer():
  args_for_layer = ["line", "patch", "outline"]
  new_layer_nb = 1 + max([_default_arguments[fa]['zorder'] for fa in args_for_layer])
  for fa in args_for_layer: 
    _default_arguments[fa]['zorder'] = new_layer_nb

def set_line_style(**kwargs):
  _set_default_style(what='line', **kwargs)

def set_patch_style(**kwargs):
  _set_default_style(what='patch', **kwargs)
                
def set_outline_style(**kwargs):
  _set_default_style(what='outline', **kwargs)
 
def _set_default_style(what, **kwargs):
  global _default_arguments
  for ua in kwargs.keys():
    _default_arguments[what][ua] = kwargs[ua]

########################################################################

def raise_Exception_if_not_processed(kwarg_keys, processed_keys):
  not_processed = [arg_name for arg_name in kwarg_keys if arg_name not in processed_keys]
  if len(not_processed) > 0:
    raise Exception("Arguments", ', '.join(not_processed), " are not recognised")
