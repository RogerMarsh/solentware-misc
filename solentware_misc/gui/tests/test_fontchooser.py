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
                    "__init__\(\) missing 2 required positional ",
                    "arguments: 'master' and 'title'",
                )
            ),
            fontchooser.AppSysFontChooser,
        )


if __name__ == "__main__":
    runner = unittest.TextTestRunner
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    runner().run(loader(AppSysFontChooser))
