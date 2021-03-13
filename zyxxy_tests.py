
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
    if f.startswith("draw"):
      print(f, datetime.datetime.now())
      loader = importlib.machinery.SourceFileLoader(f[:-3], f)
      mod = types.ModuleType(loader.name)
      loader.exec_module(mod)
  print(datetime.datetime.now())