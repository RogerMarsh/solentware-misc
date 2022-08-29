# indexmap_test.py
# Copyright 2012 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""indexmap tests"""

import unittest

from .. import indexmap


class Segment(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_001___init___001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"__init__\(\) missing 1 required positional argument: ",
                    "'segment'",
                )
            ),
            indexmap.Segment,
        )

    def test_001___init___002(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"__init__\(\) got an unexpected keyword argument ",
                    "'badkey'",
                )
            ),
            indexmap.Segment,
            *(None,),
            **dict(pickled=None, bitmap=False, values=None, badkey=None),
        )


if __name__ == "__main__":
    runner = unittest.TextTestRunner
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    runner().run(loader(Segment))
