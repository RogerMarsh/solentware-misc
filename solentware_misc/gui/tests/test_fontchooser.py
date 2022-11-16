# test_fontchooser.py
# Copyright 2021 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""exceptionhandler tests."""

import unittest

from .. import fontchooser


class AppSysFontChooser(unittest.TestCase):
    def test_001___init___001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"__init__\(\) takes from 1 to 4 positional ",
                    "arguments but 5 were given",
                )
            ),
            fontchooser.AppSysFontChooser,
            *(None, None, None, None),
        )


if __name__ == "__main__":
    runner = unittest.TextTestRunner
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    runner().run(loader(AppSysFontChooser))
