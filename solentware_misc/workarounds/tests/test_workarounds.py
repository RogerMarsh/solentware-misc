# test_workarounds.py
# Copyright 2021 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""workarounds tests"""

import unittest
import tkinter

from .. import workarounds


class Workarounds(unittest.TestCase):
    def setUp(self):
        self.parent = tkinter.Tk()

    def tearDown(self):
        self.parent.destroy()

    def test_grid_configure_query_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"grid_configure_query\(\) missing 3 required positional ",
                    "arguments: 'widget', 'command', and 'index'",
                )
            ),
            workarounds.grid_configure_query,
        )

    def test_grid_configure_query_002(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"grid_configure_query\(\) got an unexpected keyword ",
                    "argument 'badkey'",
                )
            ),
            workarounds.grid_configure_query,
            *(
                None,
                None,
                None,
            ),
            **dict(option=None, badkey=None),
        )

    def test_grid_configure_query_003(self):
        frame = tkinter.Frame(master=self.parent)
        self.assertEqual(
            workarounds.grid_configure_query(frame, "rowconfigure", 0),
            {"minsize": 0, "pad": 0, "uniform": None, "weight": 0},
        )

    def test_grid_configure_query_004(self):
        frame = tkinter.Frame(master=self.parent)
        self.assertEqual(
            workarounds.grid_configure_query(
                frame, "rowconfigure", 0, option="-pad"
            ),
            0,
        )

    def test_grid_configure_query_005(self):
        frame = tkinter.Frame(master=self.parent)
        self.assertEqual(
            workarounds.grid_configure_query(
                frame, "rowconfigure", 0, option="-uniform"
            ),
            None,
        )

    def test_grid_configure_query_006(self):
        frame = tkinter.Frame(master=self.parent)
        frame.grid_rowconfigure(0, uniform="fixed")
        self.assertEqual(
            workarounds.grid_configure_query(
                frame, "rowconfigure", 0, option="uniform"
            ),
            "fixed",
        )

    def test_grid_configure_query_007(self):
        frame = tkinter.Frame(master=self.parent)
        self.assertEqual(
            workarounds.grid_configure_query(
                frame, "rowconfigure", 0, option="pad"
            ),
            0,
        )

    def test_grid_configure_query_008(self):
        frame = tkinter.Frame(master=self.parent)
        frame.grid_rowconfigure(0, uniform="fixed")
        self.assertEqual(
            workarounds.grid_configure_query(
                frame, "rowconfigure", 0, option="-uniform"
            ),
            "fixed",
        )

    def test_text_count_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"text_count\(\) missing 3 required positional ",
                    "arguments: 'widget', 'index1', and 'index2'",
                )
            ),
            workarounds.text_count,
        )

    def test_text_count_002(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"text_count\(\) got an unexpected keyword ",
                    "argument 'badkey'",
                )
            ),
            workarounds.text_count,
            *(
                None,
                None,
                None,
            ),
            **dict(badkey=None),
        )

    def test_text_count_003(self):
        text = tkinter.Text(master=self.parent)
        self.assertEqual(workarounds.text_count(text, "1.0", tkinter.END), 1)

    def test_text_count_004(self):
        text = tkinter.Text(master=self.parent)
        text.insert(tkinter.END, "five")
        self.assertEqual(
            workarounds.text_count(
                text, "1.0", tkinter.END, "-chars", "-lines"
            ),
            (5, 1),
        )


class WorkaroundsRedundant(unittest.TestCase):
    def setUp(self):
        self.parent = tkinter.Tk()

    def tearDown(self):
        self.parent.destroy()

    def test_grid_configure_query_007(self):
        frame = tkinter.Frame(master=self.parent)
        self.assertEqual(frame.grid_rowconfigure(0, "pad"), 0)

    def test_grid_configure_query_008(self):
        frame = tkinter.Frame(master=self.parent)
        frame.grid_rowconfigure(0, uniform="fixed")
        self.assertEqual(frame.grid_rowconfigure(0, "uniform"), "fixed")

    def test_count_001(self):
        text = tkinter.Text(master=self.parent)
        text.insert(tkinter.END, "five")
        self.assertEqual(
            text.count("1.0", tkinter.END, "chars", "lines"), (5, 1)
        )


if __name__ == "__main__":
    runner = unittest.TextTestRunner
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    runner().run(loader(Workarounds))
    runner().run(loader(WorkaroundsRedundant))
