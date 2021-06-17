# texttab.py
# Copyright 2009 Roger Marsh
# Licence: See LICENCE (BSD licence)

######
#
# Hacked <Escape><Tab> as I do not see how to make Alt-Shift-Tab work
#
######
"""Subclass of Text widget with Alt-Shift-Tab replacing Tab.

The intention is to avoid accidents where a Text widget is in the tab order
cycle along with Buttons and other widgets where the significance of Tab
changes with the widget having focus.


List of classes:

TextTab - subclass of Text with methods to set and unset tab bindings.

List of functions:

make_text_tab - make a Text widget that uses Alt-Shift-Tab instead of Tab.
set_tab_bindings - function to set tab bindings on (text) widget.
unset_tab_bindings - function to unset tab bindings on (text) widget.

"""

import Tkinter


class TextTab(Tkinter.Text):
    
    """Subclass of Text widget with Alt-Shift-Tab replacing Tab.

    Methods added:

    set_tab_bindings
    unset_tab_bindings

    Methods overridden:

    None

    Methods extended:

    None
    
    """

    def set_tab_bindings(self):
        """Set bindings replacing Tab with Alt-Shift-Tab on this instance."""
        set_tab_bindings(self)

    def unset_tab_bindings(self):
        """Unset bindings replacing Tab with Alt-Shift-Tab on this instance."""
        unset_tab_bindings(self)


def make_text_tab(master=None, cnf={}, **kargs):
    """Return Text widget with Alt-Shift-Tab binding replacing Tab binding."""
    t = Tkinter.Text(master=master, cnf=cnf, **kargs)
    set_tab_bindings(t)
    return t


def set_tab_bindings(tw):
    """Set bindings to replace Tab with Alt-Shift-Tab on Text widget.

    Derived by looking at /usr/local/lib/tk8.5/text.tcl.

    """

    def InsertTab(event=None):
        # Hacked to use <Escape><Tab> instead of <Alt-Shift-Tab>
        if event.keysym == 'Escape':
            tw.__time_escape = event.time
            return
        if event.time - tw.__time_escape > 500:
            del tw.__time_escape
            return 'break'
        # Let the Text (class) binding insert the Tab
        return 'continue'

    for b in _suppress_bindings:
        tw.bind(sequence=b, func=lambda event=None : 'break')
    for b in _use_class_bindings:
        tw.bind(sequence=b, func=lambda event=None : 'continue')
    for b in _tab_bindings:
        tw.bind(sequence=b, func=InsertTab)


def unset_tab_bindings(tw):
    """Unset bindings that replace Tab with Alt-Shift-Tab on Text widget.

    Derived by looking at /usr/local/lib/tk8.5/text.tcl.

    """
    for s in (_suppress_bindings, _use_class_bindings, _tab_bindings):
        for b in s:
            tw.bind(sequence=b)


# The text (class) bindings to be suppressed
_suppress_bindings = (
    '<Tab>',
    '<Shift-Tab>',
    )

# The text (class) bindings to be kept active
_use_class_bindings = (
    '<Control-Tab>',
    )

# The tab bindings specific to this widget
# Not seen how to make <Alt-Shift-Tab> work so hack <Escape><Tab>
_tab_bindings = (
    '<Escape>',
    '<Escape><Tab>',
    )

