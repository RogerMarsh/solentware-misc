# texttab.py
# Copyright 2009 Roger Marsh
# Licence: See LICENCE (BSD licence)

######
#
# Hacked <Escape><Tab> as I do not see how to make Alt-Shift-Tab work.
# (Later: what if monitor is on same PC that runs Python?)
#
######
"""This module provides a subclass of tkinter.Text with <Escape><Tab>
replacing Tab.

The intention is to avoid accidents where a Text widget is in the tab order
cycle along with Buttons and other widgets where the significance of Tab may
change from widget to widget.

I do not see how to make Alt-Shift-Tab work, which is why <Escape><Tab> got
the job.

"""

import tkinter


# Is ExceptionHandler appropriate to this class - Tkinter.Text not wrapped
class TextTab(tkinter.Text):
    
    """Subclass of tkinter.Text with methods to replace and restore Tab
    bindings.
    
    """

    def set_tab_bindings(self):
        """Set bindings replacing Tab with <Escape><Tab>."""
        set_tab_bindings(self)

    def unset_tab_bindings(self):
        """Unset bindings replacing Tab with <Escape><Tab>."""
        unset_tab_bindings(self)


def make_text_tab(master=None, cnf={}, **kargs):
    """Return Text widget with <Escape><Tab> binding replacing Tab binding."""
    t = tkinter.Text(master=master, cnf=cnf, **kargs)
    set_tab_bindings(t)
    return t


def set_tab_bindings(tw):
    """Set bindings to replace Tab with <Escape><Tab> on tw.

    tw - a tkinter.Text instance.

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
    """Unset bindings that replace Tab with <Escape><Tab> on tw.

    tw - a tkinter.Text instance.

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

