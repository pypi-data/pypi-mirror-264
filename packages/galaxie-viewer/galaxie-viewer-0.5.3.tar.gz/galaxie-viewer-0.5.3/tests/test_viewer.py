#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Viewer Team, all rights reserved

import sys
import unittest
from io import StringIO
from unittest.mock import patch

from glxviewer import viewer


class TestView(unittest.TestCase):
    # Test

    def test_Viewer_property_with_date(self):
        # viewer = Viewer()
        self.assertTrue(viewer.with_date)

        viewer.with_date = False
        self.assertFalse(viewer.with_date)

        self.assertRaises(TypeError, setattr, viewer, 'with_date', "Hello42")

    def test_Viewer_property_status_text(self):
        # viewer = Viewer()
        self.assertEqual(viewer.status_text, "DEBUG")

        viewer.status_text = "42"
        self.assertEqual(viewer.status_text, "42")

        self.assertRaises(TypeError, setattr, viewer, 'status_text', 42)

    def test_Viewer_property_status_text_color(self):
        # viewer = Viewer()
        self.assertEqual(viewer.status_text_color, "WHITE")

        viewer.status_text_color = "CYAN"
        self.assertEqual(viewer.status_text_color, "CYAN")

        viewer.status_text_color = None
        self.assertEqual(viewer.status_text_color, "WHITE")

        self.assertRaises(TypeError, setattr, viewer, 'status_text_color', 42)
        self.assertRaises(ValueError, setattr, viewer, 'status_text_color', "42")

    def test_Viewer_property_status_symbol(self):
        # viewer = Viewer()
        self.assertEqual(viewer.status_symbol, " ")

        viewer.status_symbol = "<"
        self.assertEqual(viewer.status_symbol, "<")

        self.assertRaises(TypeError, setattr, viewer, 'status_symbol', 42)

    def test_Viewer_property_text_column_1(self):
        # viewer = Viewer()
        self.assertEqual(viewer.text_column_1, "")

        viewer.text_column_1 = "42"
        self.assertEqual(viewer.text_column_1, "42")

        self.assertRaises(TypeError, setattr, viewer, 'text_column_1', 42)

    def test_Viewer_property_text_column_2(self):
        # viewer = Viewer()
        self.assertEqual(viewer.text_column_2, "")

        viewer.text_column_2 = "42"
        self.assertEqual(viewer.text_column_2, "42")

        self.assertRaises(TypeError, setattr, viewer, 'text_column_2', 42)

    def test_Viewer_property_text_column_3(self):
        # viewer = Viewer()
        self.assertEqual(viewer.text_column_3, "")

        viewer.text_column_3 = "42"
        self.assertEqual(viewer.text_column_3, "42")

        self.assertRaises(TypeError, setattr, viewer, 'text_column_3', 42)

    def test_flush_infos(self):
        self.assertRaises(
            ValueError,
            viewer.write,
            with_date=True,
            status_text="DEBUG",
            status_text_color="42",
            status_symbol=None,
            column_1=None,
            column_2=None,
            column_3=None,
            prompt=None
        )
        color_list = ["BLACK", "RED", "GREEN", "YELLOW", "BLUE", "MAGENTA", "CYAN", "WHITE", None]
        for color in color_list:
            viewer.write(
                with_date=True,
                status_text="TEST",
                status_text_color=color,
                column_1="test with:",
                column_2="> {0} color".format(color),
            )

        for color in color_list:
            viewer.write(
                with_date=False,
                status_text="TEST",
                status_text_color=color,
                column_1="test with {0} color".format(color),
            )

        for color in color_list:
            viewer.write(
                with_date=True,
                status_text="TEST",
                status_text_color=color,
                column_1="test with {0} color".format(color),
                prompt=-1,
                status_symbol='<'
            )
            viewer.write(
                with_date=False,
                status_text="TEST",
                status_text_color=color,
                column_1="test with {0} color".format(color),
                prompt=-1,
                status_symbol='<'
            )

        for color in color_list:
            viewer.write(
                with_date=True,
                status_text="TEST",
                status_text_color=color,
                column_1="test with {0} color".format(color),
                prompt=None,
                status_symbol='>'
            )

        for color in color_list:
            viewer.write(
                with_date=True,
                status_text="TEST",
                status_text_color=color,
                column_1="test with {0} color".format(color),
                prompt=1
            )
        sys.stdout.write("\n")
        sys.stdout.flush()

    def test_flush_new_line(self):
        # viewer = Viewer()
        with patch("sys.stdout", new=StringIO()) as fake_out:
            viewer.flush_a_new_line()
            self.assertEqual(fake_out.getvalue(), "\n")


if __name__ == "__main__":
    unittest.main()
