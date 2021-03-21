import unittest
from main import *

import zyxxy_canvas
zyxxy_canvas.is_running_tests(True)
import datetime, pytest
import zyxxy_tests

class UnitTests(unittest.TestCase):

  def test_check_rectangle(self):
    zyxxy_tests.check_rectangle()

  def test_RunAllDrawings(self):
    zyxxy_tests.run_all_drawings()
    self.assertEquals(25, 25)

  def test_RunAllExamples(self):
    zyxxy_tests.run_all_examples()
    self.assertEquals(25, 25)

