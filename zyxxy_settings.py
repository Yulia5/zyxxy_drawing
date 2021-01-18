#####################################################
## don't change this file, please                  ##
#####################################################
_default_arguments = {"line" : {}, 
                      "shape" : {'turn' : 0, 'alpha' : 1.0, 'stretch_x' : 1.0, 'stretch_y' : 1.0},
                      "shape_outline" : {}}

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
                     _default_arguments['shape']['zorder'],
                     _default_arguments['shape_outline']['zorder'])
  new_layer_nb = old_layer_nb + 1
  _default_arguments['line']['zorder'] = new_layer_nb
  _default_arguments['shape']['zorder'] = new_layer_nb
  _default_arguments['shape_outline']['zorder'] = new_layer_nb

def set_line_style(colour=None, linewidth=None, joinstyle=None, zorder=None):
  global _default_arguments
  _set_line_style(colour=colour, linewidth=linewidth, joinstyle=joinstyle, zorder=zorder, _target=_default_arguments['line'])

def get_shape_zorder():
  return _default_arguments['shape']['zorder']

def set_shape_style(outline_colour=None, outline_width=None, outline_joinstyle=None, outline_zorder=None, shape_colour=None, shape_stretch_x=None, shape_stretch_y=None, shape_turn=None, shape_zorder=None, shape_alpha=None):
  global _default_arguments
  if shape_alpha is not None:
    _default_arguments['shape']['alpha'] = shape_alpha
  if shape_zorder is not None:
    _default_arguments['shape']['zorder'] = shape_zorder
  if shape_turn is not None:
    _default_arguments['shape']['turn'] = shape_turn
  if shape_turn is not None:
    _default_arguments['shape']['stretch_x'] = shape_stretch_x
  if shape_turn is not None:
    _default_arguments['shape']['stretch_y'] = shape_stretch_y
  if shape_colour is not None:
    _default_arguments['shape']['colour'] = shape_colour

  if outline_zorder is None:
    outline_zorder = _default_arguments['shape']['zorder']

  _set_line_style(colour=outline_colour, linewidth=outline_width, joinstyle=outline_joinstyle, zorder=outline_zorder, 
  _target=_default_arguments['shape_outline'])


def _fill_in_missing_values(target, default_values, target_prefix=''):
  for key in default_values.keys():
    if (target_prefix + key) not in target:
      target[target_prefix + key] = default_values[key]

def set_fill_in_outline_kwarg_defaults(kwargs):
  _fill_in_missing_values(target=kwargs, 
                          default_values=_default_arguments['shape'])
  _fill_in_missing_values(target=kwargs, 
                          default_values=_default_arguments['shape_outline'], 
                          target_prefix='outline_') 
  return kwargs

def set_line_kwarg_default(kwargs):
  _fill_in_missing_values(target=kwargs, 
                          default_values=_default_arguments['line'])
  return kwargs

def set_outline_kwarg_default(kwargs):
  _fill_in_missing_values(target=kwargs, 
                          default_values=_default_arguments['shape_outline'])
  return kwargs
