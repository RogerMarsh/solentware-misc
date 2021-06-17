# dialogues.py
# Copyright 2009 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""This module wraps tkinter.messagebox and tkinter.filedialog functions to
catch tkinter.TclError exceptions raised for grab errors occurring after
the application has been destroyed.

The wrappers for the tkinter.messagebox functions call the _show method,
bypassing the wrapped function, to avoid a problem seen on Python2.6 where
the wrapped function returns a booleanString causing comparison with
tkinter.YES, a str, to be False in all circumstances.
"""

# At 2009-08-01 calling tkMessageBox.askyesno and so on does not work
# on Python2.6: s == YES compares booleanString with str
# but calling _show works (as it does in tkMessageBox.py test stuff)
# tkFileDialog functions seem ok

import tkinter, tkinter.messagebox, tkinter.filedialog
import re

GRAB_ERROR = ''.join((
    'can',
    "'",
    't invoke "grab" command:  application has been destroyed'))
FOCUS_ERROR = ''.join((
    'can',
    "'",
    't invoke "focus" command:  application has been destroyed'))


def showinfo(title=None, message=None, **options):
    """Return tkinter.messagebox.showinfo(...), catching grab errors
    after application has been destroyed.
    """
    try:
        return str(tkinter.messagebox._show(
            title, message, tkinter.messagebox.INFO, tkinter.messagebox.OK,
            **options))
    except tkinter.TclError as error:
        if str(error) != GRAB_ERROR:
            raise


def showwarning(title=None, message=None, **options):
    """Return tkinter.messagebox.showwarning(...), catching grab errors
    after application has been destroyed.
    """
    try:
        return str(tkinter.messagebox._show(
            title, message, tkinter.messagebox.WARNING, tkinter.messagebox.OK,
            **options))
    except tkinter.TclError as error:
        if str(error) != GRAB_ERROR:
            raise


def showerror(title=None, message=None, **options):
    """Return tkinter.messagebox.showerror(...), catching grab errors
    after application has been destroyed.
    """
    try:
        return str(tkinter.messagebox._show(
            title, message, tkinter.messagebox.ERROR, tkinter.messagebox.OK,
            **options))
    except tkinter.TclError as error:
        if str(error) != GRAB_ERROR:
            raise


def askquestion(title=None, message=None, **options):
    """Return tkinter.messagebox.askquestion(...), catching grab errors
    after application has been destroyed.
    """
    try:
        return str(tkinter.messagebox._show(
            title, message, tkinter.messagebox.QUESTION,
            tkinter.messagebox.YESNO,
            **options))
    except tkinter.TclError as error:
        if str(error) != GRAB_ERROR:
            raise


def askokcancel(title=None, message=None, **options):
    """Return tkinter.messagebox.askokcancel(...), catching grab errors
    after application has been destroyed.
    """
    try:
        s = tkinter.messagebox._show(
            title, message, tkinter.messagebox.QUESTION,
            tkinter.messagebox.OKCANCEL,
            **options)
        return str(s) == tkinter.messagebox.OK
    except tkinter.TclError as error:
        if str(error) != GRAB_ERROR:
            raise


def askyesno(title=None, message=None, **options):
    """Return tkinter.messagebox.askyesno(...), catching grab errors
    after application has been destroyed.
    """
    try:
        s = tkinter.messagebox._show(
            title, message, tkinter.messagebox.QUESTION,
            tkinter.messagebox.YESNO,
            **options)
        return str(s) == tkinter.messagebox.YES
    except tkinter.TclError as error:
        if str(error) != GRAB_ERROR:
            raise


def askyesnocancel(title=None, message=None, **options):
    """Return tkinter.messagebox.askyesnocancel(...), catching grab errors
    after application has been destroyed.
    """
    try:
        s = tkinter.messagebox._show(
            title, message, tkinter.messagebox.QUESTION,
            tkinter.messagebox.YESNOCANCEL,
            **options)
        s = str(s)
        if s == tkinter.messagebox.CANCEL:
            return None
        return s == tkinter.messagebox.YES
    except tkinter.TclError as error:
        if str(error) != GRAB_ERROR:
            raise


def askretrycancel(title=None, message=None, **options):
    """Return tkinter.messagebox.askretrycancel(...), catching grab errors
    after application has been destroyed.
    """
    try:
        s = tkinter.messagebox._show(
            title, message, tkinter.messagebox.WARNING,
            tkinter.messagebox.RETRYCANCEL,
            **options)
        return str(s) == tkinter.messagebox.RETRY
    except tkinter.TclError as error:
        if str(error) != GRAB_ERROR:
            raise


def askopenfilename(**options):
    """Return tkinter.filedialog.askopenfilename(...), catching grab errors
    after application has been destroyed.
    """
    try:
        return tkinter.filedialog.askopenfilename(**options)
    except tkinter.TclError as error:
        if str(error) != GRAB_ERROR:
            raise


def asksaveasfilename(**options):
    """Return tkinter.filedialog.asksaveasfilename(...), catching grab errors
    after application has been destroyed.
    """
    try:
        return tkinter.filedialog.asksaveasfilename(**options)
    except tkinter.TclError as error:
        if str(error) != GRAB_ERROR:
            raise


def askopenfilenames(**options):
    """Return tkinter.filedialog.askopenfilenames(...), catching grab errors
    after application has been destroyed.

    tkinter.filedialog.askopenfilenames(...) returns a string with path
    names separated by spaces in some versions of Microsoft Windows, but
    returns a tuple of filenames otherwise.  Attempt to cope here.
    
    Under Wine multiple=Tkinter.TRUE has no effect at Python 2.6.2 so the
    dialogue supports selection of a single file only.  Nothing can be done
    about this here.  If it works in other versions: excellent.
    """
    # tkFileDialog.askopenfilenames always returns a tuple in the FreeBSD
    # port but always returns a string with path names separated by spaces
    # in some versions of the Microsoft Windows port.  Path names containing
    # spaces are surrounded by curly brackets (a TCL list).
    #
    # Under Wine multiple=Tkinter.TRUE has no effect at Python 2.6.2 so the
    # dialogue supports selection of a single file only.  Nothing can be done
    # about this here.  If it works in other versions - excellent.
    try:
        fn = tkinter.filedialog.askopenfilenames(**options)
        if not isinstance(fn, str):
            return fn
        if not fn:
            return fn
        fnl = [s[1:-1] for s in re.findall('{.*}', fn)]
        fnl.extend(re.sub('{.*}', '', fn).split())
        fnl.sort()
        return tuple(fnl)
    except tkinter.TclError as error:
        if str(error) != GRAB_ERROR:
            raise


def askopenfile(mode = "r", **options):
    """Return tkinter.filedialog.askopenfile(...), catching grab errors
    after application has been destroyed.
    """
    try:
        return tkinter.filedialog.askopenfile(mode = mode, **options)
    except tkinter.TclError as error:
        if str(error) != GRAB_ERROR:
            raise


def askopenfiles(mode = "r", **options):
    """Return tkinter.filedialog.askopenfiles(...), catching grab errors
    after application has been destroyed.
    """
    try:
        return tkinter.filedialog.askopenfiles(mode = mode, **options)
    except tkinter.TclError as error:
        if str(error) != GRAB_ERROR:
            raise


def asksaveasfile(mode = "w", **options):
    """Return tkinter.filedialog.asksaveasfile(...), catching grab errors
    after application has been destroyed.
    """
    try:
        return tkinter.filedialog.asksaveasfile(mode = mode, **options)
    except tkinter.TclError as error:
        if str(error) != GRAB_ERROR:
            raise


def askdirectory(**options):
    """Return tkinter.filedialog.askdirectory(...), catching grab errors
    after application has been destroyed.
    """
    try:
        return tkinter.filedialog.askdirectory (**options)
    except tkinter.TclError as error:
        if str(error) != GRAB_ERROR:
            raise
