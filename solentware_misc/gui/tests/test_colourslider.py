# test_colourslider.py
# Copyright 2021 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""colourslider tests"""

import unittest
import tkinter
import base64

from .. import colourslider


class _Slider(unittest.TestCase):
    def setUp(self):
        self.parent = tkinter.Tk()
        self.slider = colourslider._Slider(master=self.parent)

    def tearDown(self):
        self.parent = tkinter.Tk()

    def test_001___init___001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"__init__\(\) takes from 1 to 5 positional arguments ",
                    "but 6 were given",
                )
            ),
            colourslider._Slider,
            *(
                None,
                None,
                None,
                None,
                None,
            ),
        )

    def test_001___init___002(self):
        self.assertRaisesRegex(
            TypeError,
            r"__init__\(\) got an unexpected keyword argument 'badkey'",
            colourslider._Slider,
            **dict(
                master=None, column=None, row=None, resolution=2, badkey=None
            ),
        )

    def test_002_on_enter_001(self):
        self.assertRaisesRegex(
            TypeError,
            r"on_enter\(\) got an unexpected keyword argument 'badkey'",
            self.slider.on_enter,
            **dict(event=None, badkey=None),
        )

    def test_002_on_enter_002(self):
        self.assertEqual(self.slider.on_enter(), None)

    def test_003_on_leave_001(self):
        self.assertRaisesRegex(
            TypeError,
            r"on_leave\(\) got an unexpected keyword argument 'badkey'",
            self.slider.on_leave,
            **dict(event=None, badkey=None),
        )

    def test_003_on_leave_002(self):
        self.assertEqual(self.slider.on_leave(), None)

    def test_004_move_slider_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"move_slider\(\) missing 1 required positional ",
                    "argument: 'colour'",
                )
            ),
            self.slider.move_slider,
        )

    def test_004_move_slider_002(self):
        self.assertEqual(self.slider.move_slider(50), None)

    def test_005_fill_scale_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"fill_scale\(\) missing 4 required positional ",
                    "arguments: ",
                    "'newcolour', 'redhex', 'greenhex', and 'bluehex'",
                )
            ),
            self.slider.fill_scale,
        )

    def test_005_fill_scale_004(self):
        self.assertEqual(self.slider.fill_scale(50, True, True, True), None)

    def test_005_fill_scale_005(self):
        self.assertEqual(
            self.slider.fill_scale(
                50,
                None,
                base64.b16encode(bytes((20,))).lower(),
                base64.b16encode(bytes((30,))).lower(),
            ),
            None,
        )

    def test_005_fill_scale_006(self):
        self.assertEqual(
            self.slider.fill_scale(
                50,
                base64.b16encode(bytes((10,))).lower(),
                None,
                base64.b16encode(bytes((30,))).lower(),
            ),
            None,
        )

    def test_005_fill_scale_007(self):
        self.assertEqual(
            self.slider.fill_scale(
                50,
                base64.b16encode(bytes((10,))).lower(),
                base64.b16encode(bytes((20,))).lower(),
                None,
            ),
            None,
        )


class RedSlider(unittest.TestCase):
    def setUp(self):
        self.parent = tkinter.Tk()

    def tearDown(self):
        self.parent = tkinter.Tk()

    def test_001___init___001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"__init__\(\) takes from 1 to 2 positional ",
                    "arguments but 3 were given",
                )
            ),
            colourslider.RedSlider,
            *(None, None),
        )

    def test_001___init___002(self):
        self.assertIsInstance(
            colourslider.RedSlider(
                colourslider.ColourSlider(master=self.parent)
            ),
            colourslider.RedSlider,
        )


class GreenSlider(unittest.TestCase):
    def setUp(self):
        self.parent = tkinter.Tk()

    def tearDown(self):
        self.parent = tkinter.Tk()

    def test_001___init___001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"__init__\(\) takes from 1 to 2 positional ",
                    "arguments but 3 were given",
                )
            ),
            colourslider.GreenSlider,
            *(None, None),
        )

    def test_001___init___002(self):
        self.assertIsInstance(
            colourslider.GreenSlider(
                colourslider.ColourSlider(master=self.parent)
            ),
            colourslider.GreenSlider,
        )


class BlueSlider(unittest.TestCase):
    def setUp(self):
        self.parent = tkinter.Tk()

    def tearDown(self):
        self.parent = tkinter.Tk()

    def test_001___init___001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"__init__\(\) takes from 1 to 2 positional ",
                    "arguments but 3 were given",
                )
            ),
            colourslider.BlueSlider,
            *(None, None),
        )

    def test_001___init___002(self):
        self.assertIsInstance(
            colourslider.BlueSlider(
                colourslider.ColourSlider(master=self.parent)
            ),
            colourslider.BlueSlider,
        )


class ColourSlider(unittest.TestCase):
    def setUp(self):
        class Event:
            x = 20

        self.Event = Event
        self.parent = tkinter.Tk()
        self.colourslider = colourslider.ColourSlider(
            master=self.parent, row=1
        )

    def tearDown(self):
        self.parent = tkinter.Tk()

    def test_001___init___001(self):
        self.assertRaisesRegex(
            TypeError,
            r"__init__\(\) got an unexpected keyword argument 'badkey'",
            colourslider.ColourSlider,
            **dict(
                master=None,
                row=None,
                label="",
                resolution=2,
                colour="grey",
                badkey=None,
            ),
        )

    def test_002_get_colour_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"get_colour\(\) takes 1 positional argument ",
                    "but 2 were given",
                )
            ),
            self.colourslider.get_colour,
            (None,),
        )

    def test_002_get_colour_002(self):
        self.assertEqual(self.colourslider.get_colour(), b"#808080")

    def test_003_convert_RGB_colour_to_hex_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"convert_RGB_colour_to_hex\(\) missing 1 required ",
                    "positional argument: 'colour'",
                )
            ),
            self.colourslider.convert_RGB_colour_to_hex,
        )

    def test_003_convert_RGB_colour_to_hex_002(self):
        self.assertEqual(
            self.colourslider.convert_RGB_colour_to_hex((10, 20, 30)), None
        )

    def test_004_delta_red_colour_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"delta_red_colour\(\) got an unexpected keyword ",
                    "argument 'badkey'",
                )
            ),
            self.colourslider.delta_red_colour,
            **dict(event=None, badkey=None),
        )

    def test_004_delta_red_colour_002(self):
        self.assertEqual(
            self.colourslider.delta_red_colour(self.Event()), None
        )

    def test_005_delta_green_colour_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"delta_green_colour\(\) got an unexpected ",
                    "keyword argument 'badkey'",
                )
            ),
            self.colourslider.delta_green_colour,
            **dict(event=None, badkey=None),
        )

    def test_005_delta_green_colour_002(self):
        self.assertEqual(
            self.colourslider.delta_green_colour(self.Event()), None
        )

    def test_006_delta_blue_colour_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"delta_blue_colour\(\) got an unexpected ",
                    "keyword argument 'badkey'",
                )
            ),
            self.colourslider.delta_blue_colour,
            **dict(event=None, badkey=None),
        )

    def test_006_delta_blue_colour_002(self):
        self.assertEqual(
            self.colourslider.delta_blue_colour(self.Event()), None
        )

    def test_007__encode_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"_encode\(\) missing 1 required ",
                    "positional argument: 'colourcode'",
                )
            ),
            self.colourslider._encode,
        )

    def test_007__encode_002(self):
        self.assertEqual(self.colourslider._encode(10), b"0a")

    def test_008__fill_scales_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"_fill_scales\(\) takes 1 positional argument ",
                    "but 2 were given",
                )
            ),
            self.colourslider._fill_scales,
            (None,),
        )

    def test_008__fill_scales_002(self):
        self.assertEqual(self.colourslider._fill_scales(), None)

    def test_009__increment_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"_increment\(\) missing 2 required ",
                    "positional arguments: 'event' and 'colour'",
                )
            ),
            self.colourslider._increment,
        )

    def test_009__increment_002(self):
        self.assertEqual(self.colourslider._increment(self.Event(), 10), 1)

    def test_009__increment_003(self):
        self.assertEqual(self.colourslider._increment(self.Event(), 30), -1)

    def test_009__increment_004(self):
        self.assertEqual(self.colourslider._increment(self.Event(), 20), 0)

    def test_010__set_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"_set\(\) missing 1 required ",
                    "positional argument: 'event'",
                )
            ),
            self.colourslider._set,
        )

    def test_010__set_002(self):
        self.assertEqual(self.colourslider._set(self.Event()), 20)

    def test_010__set_003(self):
        self.colourslider.resolution = 30
        self.assertEqual(self.colourslider._set(self.Event()), 255)

    def test_010__set_004(self):
        self.colourslider.resolution = -10
        self.assertEqual(self.colourslider._set(self.Event()), 0)


if __name__ == "__main__":
    runner = unittest.TextTestRunner
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    runner().run(loader(_Slider))
    runner().run(loader(RedSlider))
    runner().run(loader(GreenSlider))
    runner().run(loader(BlueSlider))
    runner().run(loader(ColourSlider))
