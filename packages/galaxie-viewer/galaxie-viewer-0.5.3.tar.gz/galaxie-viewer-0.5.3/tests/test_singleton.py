#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Viewer Team, all rights reserved


import unittest
from glxviewer.viewer import Viewer


class TestSingleton(unittest.TestCase):
    # Test
    def test_singleton(self):
        viewer1 = Viewer()
        viewer2 = Viewer()

        self.assertEqual(viewer1, viewer2)


if __name__ == "__main__":
    unittest.main()
