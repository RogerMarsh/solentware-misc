# test_null.py
# Copyright 2012 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""null tests"""

import unittest

from .. import null


class Null(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_001_null_001(self):
        nil = null.Null()
        self.assertIs(nil(), nil)
        self.assertEqual(repr(nil), "Null()")
        self.assertEqual(bool(nil), False)
        self.assertEqual(nil.__getattr__("x"), nil)
        self.assertEqual(nil.__setattr__("x", 1), nil)
        self.assertEqual(nil.__delattr__("x"), nil)


if __name__ == "__main__":
    runner = unittest.TextTestRunner
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    runner().run(loader(Null))
