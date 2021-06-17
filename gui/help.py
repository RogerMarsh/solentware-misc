# help.py
# Copyright 2012 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Functions to support creation of Help widgets.

List of functions:

help_widget (was _help in chesspad/gui/help.py)
help_text   (was _help_text in chesspad/gui/help.py)

"""

import Tkinter
from os.path import isfile, basename, splitext

import rmappsup.gui.textreadonly


def help_text(title, help_text_module, name):
    """Return text from the help text file for title."""

    for htf in help_text_module._textfile[title]:
        if name is not None:
            if name != splitext(basename(htf))[0]:
                continue
        if isfile(htf):
            try:
                f = open(htf)
                try:
                    t = f.read()
                except:
                    t = ' '.join(('Read help', str(title), 'failed'))
                f.close()
                return t
            except:
                break
    return ' '.join((str(title), 'help not found'))


def help_widget(master, title, help_text_module, hfname=None):
    """Build a Toplevel widget to display a help text document."""

    toplevel = Tkinter.Toplevel(master)
    toplevel.wm_title(title)
    help_ = rmappsup.gui.textreadonly.TextReadonly(
        toplevel, wrap='word', tabstyle='tabular')
    scrollbar = Tkinter.Scrollbar(
        toplevel, orient=Tkinter.VERTICAL, command=help_.yview)
    help_.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=Tkinter.RIGHT, fill=Tkinter.Y)
    help_.pack(
        side=Tkinter.LEFT, fill=Tkinter.BOTH, expand=Tkinter.TRUE)
    help_.set_readonly_bindings()
    help_.insert(Tkinter.END, help_text(title, help_text_module, hfname))
    help_.focus_set()
