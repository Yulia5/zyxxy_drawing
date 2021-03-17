
import zyxxy_canvas
zyxxy_canvas.is_running_tests(True)
import datetime

def run_all_examples():
  import inspect
  import zyxxy_all_EXAMPLES
  
  all_functions_list = inspect.getmembers(zyxxy_all_EXAMPLES, inspect.isfunction)
  all_functions_list.sort(key=lambda x: x[0], reverse=True)
  for key, value in all_functions_list:
    if key.startswith("example"):
      print(key, datetime.datetime.now())
      value()
  print(datetime.datetime.now())
  

def run_all_drawings():
  import os
  import types
  import importlib.machinery  

  files = [f for f in os.listdir('.') if os.path.isfile(f)]
  for f in files:
    if f.startswith("draw") or f.startswith("zyxxy_shape_demo"):
      print(f, datetime.datetime.now())
      loader = importlib.machinery.SourceFileLoader(f[:-3], f)
      mod = types.ModuleType(loader.name)
      loader.exec_module(mod)
  print(datetime.datetime.now())

def check_rectangle():
  from zyxxy_shape_functions import draw_a_rectangle
  from zyxxy_canvas import create_canvas_and_axes
  from zyxxy_utils import is_the_same_point

  axes = create_canvas_and_axes(canvas_width = 18,
                              canvas_height = 12)
  r  = draw_a_rectangle(ax=axes, centre_x=9, centre_y=2, width=22, height=1)
  r0 = draw_a_rectangle(ax=axes, centre_x=9, centre_y=2, width=22, height=1, turn=0)
  r1 = draw_a_rectangle(ax=axes, centre_x=9, centre_y=2, width=22, height=1, turn=6)
  print(r.get_xy())
  print(r.diamond_coords)
  print(r0.get_xy())
  #print(r0.get_xy() + r1.get_xy())
  print(is_the_same_point(p1=r.get_xy(), p2=r0.get_xy()))
  r0.rotate(turn=6)
  print(r0.get_xy())