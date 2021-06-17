# textentry.py
# Copyright 2009 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""A text entry dialogue.

List of classes:

TextEntry - Text entry dialogue

List of functions:

get_text_modal - Get text from a TextEntry dialogue

"""

import Tkinter

_TITLE = 'title'
_TEXT = 'text'


class TextEntry(object):
    
    """Modal text entry dialogue widget.

    get_text() returns None unless Ok clicked. 
    
    Methods added:

    _cancel - Cancel dialogue.
    get_text - Return entered text if dialogue completed with Ok
    _ok - Complete dialogue.
    show_modal - Show dialogue
    __del__ - Destroy dialogue

    Methods overridden:

    __init__

    Methods extended:

    None
    
    """

    def __init__(self, master=None, **options):
        """Initialise dialogue"""
        self.entered_text = None
        self.master = master
        self.options = options
        self.toplevel = None
        self.entry = None

    def _cancel(self):
        """Cancel dialogue"""
        self.toplevel.destroy()
        self.toplevel = None
        self.entry = None

    def get_text(self):
        """Return entered text if Ok clicked otherwise None"""
        return self.entered_text

    def _ok(self):
        """Complete dialogue.  Entered text is returned by get_text()"""
        self.entered_text = self.entry.get()
        self.toplevel.destroy()
        self.toplevel = None
        self.entry = None

    def show_modal(self):
        """Create and show the modal text entry dialogue.

        Remove text and title from options before passing rest to Entry.
        Title is passed to Toplevel.
        Text is passed to Label.

        """
        options = self.options

        if _TITLE in options:
            title = options[_TITLE]
            del options[_TITLE]
        else:
            title = 'Text Entry'
        if _TEXT in options:
            text = options[_TEXT]
            del options[_TEXT]
        else:
            text = 'Enter text'

        self.toplevel = toplevel = Tkinter.Toplevel(master=self.master)
        toplevel.wm_title(title)
        label = Tkinter.Label(master=toplevel, text=text)
        label.pack()
        self.entry = entry = Tkinter.Entry(master=toplevel, **options)
        entry.pack(fill=Tkinter.X, expand=Tkinter.TRUE)
        buttonbar = Tkinter.Frame(master=toplevel)
        buttonbar.pack(fill=Tkinter.X, expand=Tkinter.TRUE)
        cancel = Tkinter.Button(
            master=buttonbar,
            text='Cancel',
            underline=0,
            command=self._cancel)
        cancel.pack(expand=Tkinter.TRUE, side=Tkinter.LEFT)
        ok = Tkinter.Button(
            master=buttonbar,
            text='Ok',
            underline=0,
            command=self._ok)
        ok.pack(expand=Tkinter.TRUE, side=Tkinter.LEFT)
        entry.focus()
        toplevel.grab_set()
        toplevel.wait_window()

        return self.entered_text

    def __del__(self):

        if self.toplevel:
            self.toplevel.destroy()


def get_text_modal(master=None, **options):
    """Return text from TextEntry dialog

    The get_text_modal convenience function is provided to return the entered
    text and destroy the dialogue.
    Otherwise use get_text method of TextEntry instance to retrieve text.
    
    """
    te = TextEntry(master=master, **options)
    return te.show_modal()

