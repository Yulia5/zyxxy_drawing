
import zyxxy_canvas
zyxxy_canvas.is_running_tests(True)
import datetime, pytest
import matplotlib.pyplot as plt
from zyxxy_shape_class import Shape

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

n=0
def check_rectangle():
  from zyxxy_shape_functions import draw_a_rectangle, clone_a_shape
  from zyxxy_canvas import create_canvas_and_axes
  from zyxxy_utils import is_the_same_contour #, is_the_same_point

  axes = create_canvas_and_axes(canvas_width = 18, canvas_height = 12)
  
  def compare_contours(s1, s2, **kwargs):
    global n
    p1 = s1.get_xy() if isinstance(s1, Shape) else s1
    p2 = s2.get_xy() if isinstance(s2, Shape) else s2

    assert is_the_same_contour(p1=p1, p2=p2, **kwargs), "failed test " + str(n)
    print("succeeded test " + str(n))
    n+=1

  # same rectangle, then with 0 turn, then stretched and turned, then with alternative diamonds
  r  = draw_a_rectangle(ax=axes, centre_x=5, centre_y=15, width=10, height=2)
  r0 = draw_a_rectangle(ax=axes, centre_x=5, centre_y=15, width=10, height=2, turn=0)
  r2 = clone_a_shape(r)
  r2.stretch(stretch_x=1/5, stretch_y=5)
  r2.rotate(turn=3)
  r3 = draw_a_rectangle(ax=axes, left=0, top=16, width=10, height=2)
  r4 = draw_a_rectangle(ax=axes, right=10, bottom=14, width=10, height=2)
  
  for other_r, kwargs in [[r0, {}], [r2, {'start_1':1}], [r3, {}], [r4, {}]]:
    compare_contours(s1=r, s2=other_r, **kwargs)

  # make sure shift works
  # print(r.get_xy());
  r_1 = clone_a_shape(r ); r_1.shift(shift=[1, 2]); # print(r.get_xy()); return; print(r_1.get_xy()); 
  r31 = clone_a_shape(r3); r31.shift(shift=[1, 2])
  r41 = clone_a_shape(r4); r41.shift(shift=[1, 2])

  for other_r in [r_1, r31, r41]:
    compare_contours(s1=r.get_xy() + [1, 2], s2=other_r)

  # make sure shift works
  

  #r_1.update_shape_parameters(centre_x)


  with pytest.raises(Exception):
    x = 1 / 0
