"""no pyQt5/pySide2 or vtk"""
from pyNastran.gui.test.test_utils import *
from pyNastran.gui.test.test_parsing import *
from pyNastran.gui.gui_objects.test.test_settings import *
from pyNastran.gui.menus.test.test_groups_modify import *

if __name__ == "__main__":  # pragma: no cover
    import unittest
    unittest.main()
