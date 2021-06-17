# textreadonly.py
# Copyright 2009 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Subclass of, and maker function for, Text widget with read only bindings.

List of classes:

TextReadonly - Text subclass with edit bindings that can be set and unset.

List of functions:

make_text_readonly - function to make a Text widget initialized read only.
set_readonly_bindings - function to set read only bindings on (text) widget.
unset_readonly_bindings - function to unset read only bindings on (text) widget.

"""

import Tkinter


# Is ExceptionHandler appropriate to this class - Tkinter.Text not wrapped
class TextReadonly(Tkinter.Text):
    
    """Read-only subclass of Text widget with full navigation.

    Methods added:

    set_readonly_bindings
    unset_readonly_bindings

    Methods overridden:

    None

    Methods extended:

    None
    
    """

    def set_readonly_bindings(self):
        """Set bindings to suppress editing actions on this Text widget."""
        set_readonly_bindings(self)

    def unset_readonly_bindings(self):
        """Unset bindings that suppress editing actions on this Text widget."""
        unset_readonly_bindings(self)


def make_text_readonly(master=None, cnf={}, **kargs):
    """Return Text widget with read only bindings"""
    t = Tkinter.Text(master=master, cnf=cnf, **kargs)
    set_readonly_bindings(t)
    return t


def set_readonly_bindings(tw):
    """Set bindings to suppress editing actions on Text widget.

    Derived by looking at /usr/local/lib/tk8.5/text.tcl.

    """
    # Never insert character in tw Text widget
    # Suppress editing events
    for b in _suppress_bindings:
        tw.bind(sequence=b, func=lambda event=None : 'break')

    # All navigation sequences are handled by class bindings
    # No need to ignore Escape and KP_Enter here becuase KeyPress
    # never gets to class bindings
    for b in _use_class_bindings:
        tw.bind(sequence=b, func=lambda event=None : 'continue')


def unset_readonly_bindings(tw):
    """Unset bindings that suppress editing actions on Text widget.

    Derived by looking at /usr/local/lib/tk8.5/text.tcl.

    """
    for s in (_suppress_bindings, _use_class_bindings):
        for b in s:
            tw.bind(sequence=b)


# The text bindings to be suppressed
_suppress_bindings = (
    '<KeyPress>',
    '<B1-Motion>',
    '<Double-1>',
    '<Triple-1>',
    '<Shift-1>',
    '<Double-Shift-1>',
    '<Triple-Shift-1>',
    '<B1-Leave>',
    '<B1-Enter>',
    '<ButtonRelease-1>',
    '<Control-1>',
    '<Shift-Left>',
    '<Shift-Right>',
    '<Shift-Up>',
    '<Shift-Down>',
    '<Shift-Home>',
    '<Shift-End>',
    '<Shift-Prior>',
    '<Shift-Next>',
    '<Shift-Control-Left>',
    '<Shift-Control-Right>',
    '<Shift-Control-Up>',
    '<Shift-Control-Down>',
    '<Control-Shift-Home>',
    '<Control-Shift-End>',
    '<Control-i>',
    '<Control-space>',
    '<Control-Shift-space>',
    '<Shift-Select>',
    '<Control-slash>',
    '<Control-backslash>',
    '<Control-d>',
    '<Control-k>',
    '<Control-o>',
    '<Control-t>',
    '<<Cut>>',
    '<<Copy>>',
    '<<Paste>>',
    '<<Clear>>',
    '<<PasteSelection>>',
    '<<Undo>>',
    '<<Redo>>',
    '<Meta-d>',
    '<Meta-BackSpace>',
    '<Meta-Delete>',
    '<Shift-Option-Left>',
    '<Shift-Option-Right>',
    '<Shift-Option-Up>',
    '<Shift-Option-Down>',
    '<Button-2>',
    '<B2-Motion>',
    )

# The text bindings to be kept active
_use_class_bindings = (
    '<Control-KeyPress>',
    '<Shift-KeyPress>',
    '<Alt-KeyPress>',
    '<Meta-KeyPress>',
    '<Left>',
    '<Right>',
    '<Up>',
    '<Down>',
    '<Home>',
    '<End>',
    '<Prior>',
    '<Next>',
    '<Control-Left>',
    '<Control-Right>',
    '<Control-Up>',
    '<Control-Down>',
    '<Control-Home>',
    '<Control-End>',
    '<Control-Prior>',
    '<Control-Next>',
    '<Control-a>',
    '<Control-b>',
    '<Control-e>',
    '<Control-f>',
    '<Control-n>',
    '<Control-p>',
    '<Meta-b>',
    '<Meta-f>',
    '<Meta-less>',
    '<Meta-greater>',
    )

