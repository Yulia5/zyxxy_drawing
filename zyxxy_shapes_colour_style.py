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

from MY_zyxxy_SETTINGS import my_default_demo_params, my_default_colour_etc_settings
from matplotlib.colors import is_color_like
from MY_zyxxy_SETTINGS import my_colour_palette

########################################################################

line_arg_types = ["colour", "width", "joinstyle", "zorder"]
patch_arg_types = ["colour", "alpha", "zorder"]
diamond_arg_types = ["colour", "size", "zorder", "show", 'alpha']
background_arg_types = ['colour', 'zorder']

format_arg_dict = { "line"    : line_arg_types, 
                    "patch"   : patch_arg_types, 
                    "outline" : line_arg_types,
                    "diamond" : diamond_arg_types}

_default_arguments = my_default_colour_etc_settings

##################################################################
## DIAMOND HELPERS                                              ## 
##################################################################

def set_diamond_style(show=None):
  if show is not None:
    _default_arguments['diamond']['show'] = show

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

def get_patch_style(patch_name, kwargs=None):
  if kwargs is None:
    kwargs = _default_arguments
  patch_dict = {key[len(patch_name)+1:] : value for key, value in kwargs.items()
                                              if key.startswith(patch_name + "_")}

  colour_to_use = find_colour_code( patch_dict['colour'])
  if 'show' in patch_dict and not patch_dict['show']:
    colour_to_use = 'none'
  result = {'fc' : colour_to_use, 
            'ec' : 'none',
            'zorder' : patch_dict['zorder'],
            'alpha' : patch_dict['alpha']}
  return result

def get_line_style(line_name, kwargs=None):
  if kwargs is None:
    kwargs = _default_arguments
  line_dict = {key[len(line_name)+1:] : value for key, value in kwargs.items()
                                            if key.startswith(line_name + "_")}
  try:
    result = {'color' : find_colour_code( line_dict['colour'] ), 
            'lw' : line_dict['width'],
            'zorder' : line_dict['zorder'],
            'solid_joinstyle' : line_dict['joinstyle']}
  except:
    raise Exception(line_dict)
  return result

########################################################################

def new_layer():
  args_for_layer = ["line", "patch", "outline"]
  new_layer_nb = 1 + max([_default_arguments[fa]['zorder'] for fa in args_for_layer])
  for fa in args_for_layer: 
    _default_arguments[fa]['zorder'] = new_layer_nb

def set_line_style(kwargs):
  global _default_arguments
  _set_dictionary_from_kwargs(target_dict=_default_arguments['line'], 
                              kwargs=kwargs, 
                              dict_keys=line_arg_types)
  raise_Exception_if_not_processed(kwarg_keys=kwargs.keys(), 
                                    processed_keys=line_arg_types)

def set_patch_style(kwargs):
  global _default_arguments

  used_for_patch = _set_dictionary_from_kwargs(target_dict=_default_arguments['patch'], 
                                               kwargs=kwargs, 
                                               dict_keys=patch_arg_types, 
                                               kwargs_prefix="patch_")

  if 'outline_zorder' not in kwargs:
    kwargs['outline_zorder'] = _default_arguments['patch']['zorder']

  used_for_outline = _set_dictionary_from_kwargs(target_dict=_default_arguments['outline'], 
                                                 wargs=kwargs, 
                                                 dict_keys=line_arg_types, 
                                                 kwargs_prefix="outline_")

  raise_Exception_if_not_processed(kwarg_keys=kwargs.keys(), 
                                    processed_keys=used_for_outline+used_for_patch)

########################################################################

def set_fill_in_outline_kwarg_defaults(kwargs, defaults_for_demo=False):
  if defaults_for_demo:
    defaults_to_use = my_default_demo_params
  else:
    defaults_to_use = _default_arguments

  result = {}
  param_names_used = []
  for fa in format_arg_dict.keys(): 
    for _arg in format_arg_dict[fa]:
      param_name = fa + '_' + _arg
      if param_name in kwargs:
        result[param_name] = kwargs[param_name]
        param_names_used.append(param_name)
      else:
        result[param_name] = defaults_to_use[fa][_arg]
  return param_names_used, result

########################################################################

def _set_dictionary_from_kwargs(target_dict, kwargs, dict_keys, kwargs_prefix=""):
  processed_arguments = []
  for dk in dict_keys:
    if dk in kwargs:
      target_dict[dk] = kwargs[kwargs_prefix + dk]
      processed_arguments.append(kwargs_prefix + dk)
  return processed_arguments

def raise_Exception_if_not_processed(kwarg_keys, processed_keys):
  not_processed = [arg_name for arg_name in kwarg_keys if arg_name not in processed_keys]
  if len(not_processed) > 0:
    raise Exception("Arguments", ', '.join(not_processed), " are not recognised")
