
import zyxxy_canvas
zyxxy_canvas.is_running_tests(True)
import datetime, pytest
import matplotlib.pyplot as plt

def run_all_examples():
  import inspect
  import zyxxy_all_EXAMPLES
  
  all_functions_list = inspect.getmembers(zyxxy_all_EXAMPLES, inspect.isfunction)
  all_functions_list.sort(key=lambda x: x[0], reverse=True)
  for key, value in all_functions_list:
    if key.startswith("example"):
      print(key, datetime.datetime.now())
      value()
      plt.close('all')
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
      plt.close('all')
  print(datetime.datetime.now())

def check_rectangle():
  from zyxxy_shape_functions import draw_a_rectangle, clone_a_shape
  from zyxxy_canvas import create_canvas_and_axes
  from zyxxy_utils import is_the_same_contour #, is_the_same_point

  axes = create_canvas_and_axes(canvas_width = 18, canvas_height = 12)
  r  = draw_a_rectangle(ax=axes, centre_x=5, centre_y=15, width=10, height=2)
  r0 = draw_a_rectangle(ax=axes, centre_x=5, centre_y=15, width=10, height=2, turn=0)
  r2 = clone_a_shape(r)
  r2.stretch(stretch_x=1/5, stretch_y=5)
  r2.rotate(turn=3)
  r3 = draw_a_rectangle(ax=axes, left=0, top=16, width=10, height=2)
  r4 = draw_a_rectangle(ax=axes, right=10, bottom=14, width=10, height=2)
  r31 = clone_a_shape(r3)
  r41 = clone_a_shape(r4)

  n=0
  for other_r, kwargs in [[r0, {}], [r2, {'start_1':1}], [r3, {}], [r4, {}]]:
    assert is_the_same_contour(p1=r.get_xy(), p2=other_r.get_xy(), **kwargs), "failed test " + str(n)
    print("succeeded test " + str(n))
    n+=1

  with pytest.raises(Exception):
    x = 1 / 0
