# colourslider.py
# Copyright 2009 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""A collection of scale-like widgets for displaying colour choices.

List of classes:

_Slider
RedSlider
GreenSlider
BlueSlider
ColourSlider

"""

import Tkinter
import base64

from exceptionhandler import ExceptionHandler


class _Slider(ExceptionHandler):

    """A colour scale widget with a pointer and colour demonstration bar.

    Methods added:

    on_enter
    on_leave
    move_slider

    Methods overridden:

    __init__

    Methods extended:

    None
    
    """

    def __init__(
        self,
        master=None,
        column=None,
        row=None,
        resolution=2,
        colourslider=None):

        self.canvas = Tkinter.Canvas(master=master)
        self.canvas.grid_configure(column=column, row=row, sticky='nsew')

        self.lines = l = []
        self.slider = self.canvas.create_polygon(
            50, 22, 55, 32, 45, 32, fill='black')
        create_line = self.canvas.create_line
        for e, x in enumerate(range(0, 256, resolution)):
            l.append(create_line(e + 10, 0, e + 10, 20))
        left, top, right, bottom=self.canvas.bbox('all')
        self.canvas.configure(height=bottom, width=right + 10)

        self.fill_scale(colourslider=colourslider)

        self.canvas.bind('<Enter>', self.try_event(self.on_enter))
        self.canvas.bind('<Leave>', self.try_event(self.on_leave))

    def on_enter(self, event=None):
        self.canvas.itemconfigure(self.slider, fill='cyan')

    def on_leave(self, event=None):
        self.canvas.itemconfigure(self.slider, fill='black')

    def move_slider(self, slider, scalebase, colour):
        resolution = 256/len(self.lines)
        left, top, right, bottom = self.canvas.bbox(slider)
        position = (left + right)/2
        newposition = colour/resolution
        delta = scalebase + newposition - position
        self.canvas.move(slider, delta, 0)


class RedSlider(_Slider):

    """A red colour scale widget.

    Methods added:

    fill_scale

    Methods overridden:

    None

    Methods extended:

    __init__
    
    """

    def __init__(self, master=None, row=None, resolution=2, colourslider=None):
        super(RedSlider, self).__init__(
            master=master,
            column=1,
            row=row,
            resolution=resolution,
            colourslider=colourslider)

    def fill_scale(self, colourslider):
        encode = base64.b16encode
        redhex = colourslider.redhex
        greenhex = colourslider.greenhex
        bluehex = colourslider.bluehex
        itemconfigure = self.canvas.itemconfigure
        resolution = 256/len(self.lines)
        for e, line in enumerate(self.lines):
            itemconfigure(line, fill=''.join((
                '#', encode(chr(e * resolution)), greenhex, bluehex)))
        self.move_slider(self.slider, 10, colourslider.red)


class GreenSlider(_Slider):

    """A green colour scale widget.

    Methods added:

    fill_scale

    Methods overridden:

    None

    Methods extended:

    __init__
    
    """

    def __init__(self, master=None, row=None, resolution=2, colourslider=None):
        super(GreenSlider, self).__init__(
            master=master,
            column=2,
            row=row,
            resolution=resolution,
            colourslider=colourslider)

    def fill_scale(self, colourslider):
        encode = base64.b16encode
        redhex = colourslider.redhex
        greenhex = colourslider.greenhex
        bluehex = colourslider.bluehex
        itemconfigure = self.canvas.itemconfigure
        resolution = 256/len(self.lines)
        for e, line in enumerate(self.lines):
            itemconfigure(line, fill=''.join((
                '#', redhex, encode(chr(e * resolution)), bluehex)))
        self.move_slider(self.slider, 10, colourslider.green)


class BlueSlider(_Slider):

    """A blue colour scale widget.

    Methods added:

    fill_scale

    Methods overridden:

    None

    Methods extended:

    __init__
    
    """

    def __init__(self, master=None, row=None, resolution=2, colourslider=None):
        super(BlueSlider, self).__init__(
            master=master,
            column=3,
            row=row,
            resolution=resolution,
            colourslider=colourslider)

    def fill_scale(self, colourslider):
        encode = base64.b16encode
        redhex = colourslider.redhex
        greenhex = colourslider.greenhex
        bluehex = colourslider.bluehex
        itemconfigure = self.canvas.itemconfigure
        resolution = 256/len(self.lines)
        for e, line in enumerate(self.lines):
            itemconfigure(line, fill=''.join((
                '#', redhex, greenhex, encode(chr(e * resolution)))))
        self.move_slider(self.slider, 10, colourslider.blue)


class ColourSlider(ExceptionHandler):

    """A colour chooser widget consisting of a red green and blue colour scale

    Methods added:

    get_colour
    get_RGB
    delta_red_colour
    set_red_colour
    delta_green_colour
    set_green_colour
    delta_blue_colour
    set_blue_colour
    _encode
    _fill_scales
    _increment
    _set

    Methods overridden:

    __init__

    Methods extended:

    None
    
    """

    def __init__(
        self, master=None, row=None, label='', resolution=2, colour='grey'):

        self.resolution = resolution
        self.get_RGB(master.winfo_rgb(colour))

        canvas = Tkinter.Canvas(master=master, width=100, height=32)
        label = canvas.create_text(50, 16, text=label)
        canvas.grid_configure(column=0, row=row, sticky='nsew')
        self.redslider = RedSlider(
            master=master,
            row=row,
            resolution=resolution,
            colourslider=self)
        self.greenslider = GreenSlider(
            master=master,
            row=row,
            resolution=resolution,
            colourslider=self)
        self.blueslider = BlueSlider(
            master=master,
            row=row,
            resolution=resolution,
            colourslider=self)
        for widget, sequence, function in (
            (self.redslider, '<ButtonPress-1>', self.delta_red_colour),
            (self.redslider, '<ButtonPress-3>', self.set_red_colour),
            (self.greenslider, '<ButtonPress-1>', self.delta_green_colour),
            (self.greenslider, '<ButtonPress-3>', self.set_green_colour),
            (self.blueslider, '<ButtonPress-1>', self.delta_blue_colour),
            (self.blueslider, '<ButtonPress-3>', self.set_blue_colour),
            ):
            widget.canvas.bind(sequence, self.try_event(function))

    def get_colour(self):
        return ''.join(('#', self.redhex, self.greenhex, self.bluehex))

    def get_RGB(self, colour):
        r, g, b = colour
        self.red, self.green, self.blue = r/256, g/256, b/256
        self.redhex = self._encode(self.red)
        self.greenhex = self._encode(self.green)
        self.bluehex = self._encode(self.blue)

    def delta_red_colour(self, event=None):
        self.red += self._increment(event, self.red)
        self.redhex = self._encode(self.red)
        self._fill_scales()

    def set_red_colour(self, event=None):
        self.red = self._set(event)
        self.redhex = self._encode(self.red)
        self._fill_scales()

    def delta_green_colour(self, event=None):
        self.green += self._increment(event, self.green)
        self.greenhex = self._encode(self.green)
        self._fill_scales()

    def set_green_colour(self, event=None):
        self.green = self._set(event)
        self.greenhex = self._encode(self.green)
        self._fill_scales()

    def delta_blue_colour(self, event=None):
        self.blue += self._increment(event, self.blue)
        self.bluehex = self._encode(self.blue)
        self._fill_scales()

    def set_blue_colour(self, event=None):
        self.blue = self._set(event)
        self.bluehex = self._encode(self.blue)
        self._fill_scales()

    def _encode(self, colourcode):
        return base64.b16encode(chr(colourcode)).lower()

    def _fill_scales(self):
        self.redslider.fill_scale(self)
        self.greenslider.fill_scale(self)
        self.blueslider.fill_scale(self)

    def _increment(self, event, colour):
        x = (event.x - 10) * self.resolution
        if colour < x:
            if colour < 255:
                return 1
        if colour > x:
            if colour > 0:
                return -1
        return 0

    def _set(self, event):
        x = (event.x - 10) * self.resolution
        if x > 255:
            return 255
        if x < 0:
            return 0
        return x

