# reports.py
# Copyright 2007 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Base classes for application dialogues and reports.

These classes allow application defined widgets to be used in dialogues and
reports as an alternative to the Label widget used in Tkinter equivalents.

List of classes:

AppSysReportBase
AppSysDialogueBase
AppSysReport
AppSysConfirm
AppSysInformation

List of functions:

show_report
show_confirm
show_information

"""

import Tkinter

import basesup.tools.dialogues

import textreadonly


class AppSysReportBase(object):

    """Base class for reports and dialogues.
    
    Methods added:

    get_button_definitions
    create_buttons
    
    Methods overridden:

    __init__

    Methods extended:

    None
    
    """

    def __init__(
        self, parent, title, caption, header, report, cnf=dict(), **kargs):
        """Define framework for application reports and dialogues.

        Subclasses provide header and report widgets which are placed in
        PanedWindow widgets.

        The cnf and **kargs arguments are ignored at present.

        """
        self.confirm = Tkinter.Toplevel()
        self.confirm.wm_title(title)
        self.caption = textreadonly.make_text_readonly(
            master=self.confirm, height=3) #temp height
        self.caption.insert(Tkinter.END, caption)
        self.buttons_frame = Tkinter.Frame(master=self.confirm)
        self.buttons_frame.pack(side=Tkinter.BOTTOM, fill=Tkinter.X)
        self.create_buttons(self.get_button_definitions())
        self.caption.pack(side=Tkinter.BOTTOM)
        self.reports = Tkinter.PanedWindow(
            master=self.confirm,
            opaqueresize=Tkinter.FALSE,
            orient=Tkinter.HORIZONTAL)
        for h, r in zip(header, report):
            p = Tkinter.PanedWindow(
                master=self.reports,
                opaqueresize=Tkinter.FALSE,
                orient=Tkinter.VERTICAL)
            th = textreadonly.make_text_readonly(
                master=p, height=6) #temp height
            th.insert(Tkinter.END, h)
            p.add(th)
            tr = textreadonly.make_text_readonly(master=p)
            tr.insert(Tkinter.END, r)
            p.add(tr)
            self.reports.add(p)
        self.reports.pack(side=Tkinter.BOTTOM, fill=Tkinter.X)

    def get_button_definitions(self):
        """Return an empty set of button definitions.

        Subclasses should override this method.

        """
        return ()

    def create_buttons(self, buttons):
        """Create the buttons in the button definition."""
        buttonrow = self.buttons_frame.pack_info()['side'] in ('top', 'bottom')
        for i, b in enumerate(buttons):
            button = Tkinter.Button(
                master=self.buttons_frame,
                text=buttons[i][0],
                underline=buttons[i][3],
                command=buttons[i][4])
            if buttonrow:
                self.buttons_frame.grid_columnconfigure(i*2, weight=1)
                button.grid_configure(column=i*2 + 1, row=0)
            else:
                self.buttons_frame.grid_rowconfigure(i*2, weight=1)
                button.grid_configure(row=i*2 + 1, column=0)
        if buttonrow:
            self.buttons_frame.grid_columnconfigure(
                len(buttons*2), weight=1)
        else:
            self.buttons_frame.grid_rowconfigure(
                len(buttons*2), weight=1)


class AppSysDialogueBase(AppSysReportBase):

    """Base class for modal reports and dialogues.
    
    Methods added:

    __del__
    
    Methods overridden:

    None

    Methods extended:

    __init__
    
    """

    def __init__(
        self, parent, title, caption, header, report, cnf=dict(), **kargs):
        """Extend superclass to be modal report or dialogue."""
        super(AppSysDialogueBase, self).__init__(
            parent=parent,
            title=title,
            caption=caption,
            header=header,
            report=report,
            cnf=cnf,
            **kargs)
        self.restore_focus = self.confirm.focus_get()
        self.confirm.wait_visibility()
        self.confirm.grab_set()
        self.confirm.wait_window()

    def __del__(self):
        """Restore focus to widget with focus before modal interaction."""
        try:
            #restore focus on dismissing dialogue
            self.restore_focus.focus_set()
        except Tkinter._tkinter.TclError, error:
            #application destroyed while confirm dialogue exists
            if str(error) != dialogues.FOCUS_ERROR:
                raise


class AppSysReport(AppSysReportBase):

    """Base class for non-modal reports.
    
    Methods added:

    on_ok
    
    Methods overridden:

    get_button_definitions

    Methods extended:

    None
    
    """

    def get_button_definitions(self):
        """Return non-modal report button definitions"""
        return (
            ('OK',
             'OK button Tooltip.',
             True,
             -1,
             self.on_ok),
            )

    def on_ok(self, event=None):
        """Destroy report widget"""
        self.confirm.destroy()


def show_report(parent, title, caption, header, report, cnf=dict(), **kargs):
    """Return AppSysReport instance."""
    return AppSysReport(
        parent=parent,
        title=title,
        caption=caption,
        header=header,
        report=report,
        cnf=cnf,
        **kargs)


class AppSysConfirm(AppSysDialogueBase):

    """A modal confirmation dialogue with Text widgets for action details.
    
    Methods added:

    is_ok
    on_cancel
    on_ok
    
    Methods overridden:

    get_button_definitions

    Methods extended:

    __init__
    __del__
    
    """

    def __init__(
        self, parent, title, caption, header, report, cnf=dict(), **kargs):
        """Extend superclass to be modal confirmation dialogue."""
        self.ok = False
        super(AppSysConfirm, self).__init__(
            parent=parent,
            title=title,
            caption=caption,
            header=header,
            report=report,
            cnf=cnf,
            **kargs)
        
    def get_button_definitions(self):
        """Return modal confirmation dialogue button definitions"""
        return (
            ('OK',
             'OK button Tooltip.',
             True,
             -1,
             self.on_ok),
            ('Cancel',
             'Cancel button Tooltip.',
             True,
             2,
             self.on_cancel),
            )

    def is_ok(self):
        """Return True if dialogue dismissed with OK button"""
        return self.ok

    def on_cancel(self, event=None):
        """Dismiss dialogue and indicate OK button not used."""
        self.ok = False
        self.confirm.destroy()

    def on_ok(self, event=None):
        """Dismiss dialogue and indicate OK button used."""
        self.ok = True
        self.confirm.destroy()

    def __del__(self):
        """Extend to indicate dialogue not dismissed with OK button."""
        self.ok = False
        super(AppSysConfirm, self).__del__()


def show_confirm(parent, title, caption, header, report, cnf=dict(), **kargs):
    """Return AppSysConfirm instance."""
    return AppSysConfirm(
        parent=parent,
        title=title,
        caption=caption,
        header=header,
        report=report,
        cnf=cnf,
        **kargs)


class AppSysInformation(AppSysDialogueBase):

    """A modal information dialogue with Text widgets for action details.
    
    Methods added:

    on_ok
    
    Methods overridden:

    get_button_definitions

    Methods extended:

    None
    
    """

    def get_button_definitions(self):
        """Return modal information dialogue button definitions"""
        return (
            ('OK',
             'OK button Tooltip.',
             True,
             -1,
             self.on_ok),
            )

    def on_ok(self, event=None):
        """Dismiss dialogue and restore focus to widget that lost focus."""
        self.confirm.destroy()


def show_information(
    parent, title, caption, header, report, cnf=dict(), **kargs):
    """Return AppSysInformation instance."""
    return AppSysInformation(
        parent=parent,
        title=title,
        caption=caption,
        header=header,
        report=report,
        cnf=cnf,
        **kargs)

