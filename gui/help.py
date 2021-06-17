# help.py
# Copyright 2012 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""This module provides functions to create widgets which display help
text files.

"""

import tkinter
from os.path import isfile, basename, splitext

from . import textreadonly


def help_text(title, help_text_module, name, encoding='utf-8'):
    """Return text from the help text file for title."""

    for htf in help_text_module._textfile[title]:
        if name is not None:
            if name != splitext(basename(htf))[0]:
                continue
        if isfile(htf):
            try:
                f = open(htf, encoding=encoding)
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

    toplevel = tkinter.Toplevel(master)
    toplevel.wm_title(title)
    help_ = textreadonly.TextReadonly(
        toplevel, wrap='word', tabstyle='tabular')
    scrollbar = tkinter.Scrollbar(
        toplevel, orient=tkinter.VERTICAL, command=help_.yview)
    help_.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    help_.pack(
        side=tkinter.LEFT, fill=tkinter.BOTH, expand=tkinter.TRUE)
    help_.set_readonly_bindings()
    help_.insert(tkinter.END, help_text(title, help_text_module, hfname))
    help_.focus_set()
