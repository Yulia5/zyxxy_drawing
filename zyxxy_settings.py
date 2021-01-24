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

from MY_zyxxy_SETTINGS import my_default_colour_etc_settings

_default_arguments = {"line" : {}, 
                      "patch" : {},
                      "patch_outline" : {}}

def set_all_colour_etc_settings(colour_etc_settings):
  global _default_arguments
  _default_arguments = colour_etc_settings

def _set_line_style(colour, linewidth, joinstyle, zorder, _target):
  global _count
  if colour is not None:
    _target['colour'] = colour
  if linewidth is not None:
    _target['linewidth'] = linewidth
  if joinstyle is not None:
    _target['joinstyle'] = joinstyle
  if zorder is not None:
    _target['zorder'] = zorder
  return _target

def new_layer():
  old_layer_nb = max(_default_arguments['line']['zorder'],
                     _default_arguments['patch']['zorder'],
                     _default_arguments['patch_outline']['zorder'])
  new_layer_nb = old_layer_nb + 1
  _default_arguments['line']['zorder'] = new_layer_nb
  _default_arguments['patch']['zorder'] = new_layer_nb
  _default_arguments['patch_outline']['zorder'] = new_layer_nb

def set_line_style(colour=None, linewidth=None, joinstyle=None, zorder=None):
  global _default_arguments
  _set_line_style(colour=colour, linewidth=linewidth, joinstyle=joinstyle, zorder=zorder, _target=_default_arguments['line'])

def get_shape_zorder():
  return _default_arguments['patch']['zorder']

def set_shape_style(outline_colour=None, outline_width=None, outline_joinstyle=None, outline_zorder=None, shape_colour=None, shape_zorder=None, shape_alpha=None):
  global _default_arguments
  if shape_alpha is not None:
    _default_arguments['patch']['alpha'] = shape_alpha
  if shape_zorder is not None:
    _default_arguments['patch']['zorder'] = shape_zorder
  if shape_colour is not None:
    _default_arguments['patch']['colour'] = shape_colour

  if outline_zorder is None:
    outline_zorder = _default_arguments['patch']['zorder']

  _set_line_style(colour=outline_colour, linewidth=outline_width, joinstyle=outline_joinstyle, zorder=outline_zorder, 
  _target=_default_arguments['patch_outline'])

def _fill_in_missing_values(target, default_values, target_prefix=''):
  for key in default_values.keys():
    if (target_prefix + key) not in target:
      target[target_prefix + key] = default_values[key]

def set_fill_in_outline_kwarg_defaults(kwargs, defaults_for_demo=False):
  if defaults_for_demo:
    defaults_to_use = my_default_colour_etc_settings
  else:
    defaults_to_use = _default_arguments
  _fill_in_missing_values(target=kwargs, 
                          default_values=defaults_to_use['patch'], 
                          target_prefix='patch_')
  _fill_in_missing_values(target=kwargs, 
                          default_values=defaults_to_use['patch_outline'], 
                          target_prefix='line_') 
  _fill_in_missing_values(target=kwargs, 
                          default_values=defaults_to_use['line'], 
                          target_prefix='line_')
  return kwargs
