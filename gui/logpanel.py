# logpanel.py
# Copyright 2013 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""This module contains classes which provide task log widgets for use in
the notebook style frame.AppSysFrame or a tkinter.Toplevel.

"""

import tkinter
import threading

from .textreadonly import make_scrolling_text_readonly
from . import (
    tasklog,
    panel,
    )


class TextAndLogPanel(panel.PlainPanel):
    
    """This class provides a task log widget for use in the notebook style
    frame.AppSysFrame.

    """

    def __init__(
        self,
        parent=None,
        taskheader=None,
        taskdata=None,
        taskbuttons=dict(),
        starttaskbuttons=(),
        runmethod=None,
        runmethodargs=dict(),
        cnf=dict(),
        **kargs):
        """Create the task log Text widget.

        parent - passed to superclass
        taskheader - optional text for the optional task header widget
        taskdata - optional intial text for the task log widget
        taskbuttons - button definitions for controlling the running task
        starttaskbuttons - button definitions for starting the task
        runmethod - method which does the task
        runmethodargs - arguments for the method which runs the task
        cnf - passed to superclass
        **kargs - passed to superclass

        """
        self.taskbuttons = taskbuttons
        
        super(TextAndLogPanel, self).__init__(
            parent=parent,
            cnf=cnf,
            **kargs)

        self.hide_panel_buttons()
        self.show_panel_buttons(starttaskbuttons)
        self.create_buttons()

        if taskheader is not None:
            self.headerwidget = tkinter.Label(
                master=self.get_widget(),
                text=taskheader)
            self.headerwidget.pack(side=tkinter.TOP, fill=tkinter.X)

        pw = tkinter.PanedWindow(
            self.get_widget(),
            opaqueresize=tkinter.FALSE,
            orient=tkinter.VERTICAL)
        pw.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=tkinter.TRUE)

        if taskdata is not None:
            ef, self.datawidget = make_scrolling_text_readonly(
                master=pw, wrap='word', undo=tkinter.FALSE)
            pw.add(ef)
            self.datawidget.insert(tkinter.END, taskdata)
        
        rf = tkinter.Frame(master=pw)
        self.tasklog = tasklog.TaskLog(
            get_app=self.get_appsys,
            logwidget=tasklog.LogText(
                master=rf,
                wrap='word',
                undo=tkinter.FALSE,
                get_app=self.get_appsys),
            )
        pw.add(rf)
        if runmethod is not False:
            self.tasklog.run_method(runmethod, kwargs=runmethodargs)

    def close(self):
        """Close resources prior to destroying this instance.

        Used, at least, as callback from AppSysFrame container
        """
        pass
            
    def describe_buttons(self):
        """Define all action buttons that may appear on Control page."""
        for tbi, tb in self.taskbuttons.items():
            if tb['command'] is False:
                tb['command'] = self.on_dismiss
            self.define_button(tbi, **tb)

    def on_dismiss(self, event=None):
        """Default do nothing 'dismiss' button for escape from task panel."""
        pass
    
    def create_buttons(self):
        """Create the action buttons in the main thread.

        This method is called in enough places to get it's own copy of the
        mechanism to ensure it is executed in the main thread.

        """
        if threading.current_thread().name == 'MainThread':
            super(TextAndLogPanel, self).create_buttons()
        else:
            self.get_appsys().do_ui_task(
                super(TextAndLogPanel, self).create_buttons)


class WidgetAndLogPanel(panel.PlainPanel):
    
    """This class provides a task log widget in a tkinter.Toplevel.

    """

    def __init__(
        self,
        parent=None,
        taskheader=None,
        maketaskwidget=None,
        taskbuttons=dict(),
        starttaskbuttons=(),
        runmethod=None,
        runmethodargs=dict(),
        cnf=dict(),
        **kargs):
        """Create the task log Toplevel widget.

        parent - passed to superclass
        taskheader - optional text for the optional task header widget
        maketaskwidget - method to create the task log widget
        taskbuttons - button definitions for controlling the running task
        starttaskbuttons - button definitions for starting the task
        runmethod - method which does the task
        runmethodargs - arguments for the method which runs the task
        cnf - passed to superclass
        **kargs - passed to superclass

        """
        self.taskbuttons = taskbuttons
        
        super(WidgetAndLogPanel, self).__init__(
            parent=parent,
            cnf=cnf,
            **kargs)

        self.hide_panel_buttons()
        self.show_panel_buttons(starttaskbuttons)
        self.create_buttons()

        if taskheader is not None:
            self.headerwidget = tkinter.Label(
                master=self.get_widget(),
                text=taskheader)
            self.headerwidget.pack(side=tkinter.TOP, fill=tkinter.X)

        pw = tkinter.PanedWindow(
            self.get_widget(),
            opaqueresize=tkinter.FALSE,
            orient=tkinter.VERTICAL)
        pw.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=tkinter.TRUE)

        if callable(maketaskwidget):
            pw.add(maketaskwidget(pw))
        
        rf = tkinter.Frame(master=pw)
        self.tasklog = tasklog.TaskLog(
            get_app=self.get_appsys,
            logwidget=tasklog.LogText(
                master=rf,
                wrap='word',
                undo=tkinter.FALSE,
                get_app=self.get_appsys),
            )
        pw.add(rf)
        if runmethod is not False:
            self.tasklog.run_method(runmethod, kwargs=runmethodargs)

    def close(self):
        """Do nothing.
        """
        pass
            
    def describe_buttons(self):
        """Define all action buttons that may appear on Control page."""
        for tbi, tb in self.taskbuttons.items():
            if tb['command'] is False:
                tb['command'] = self.on_dismiss
            self.define_button(tbi, **tb)

    def on_dismiss(self, event=None):
        """Default do nothing 'dismiss' button for escape from task panel."""
        pass
    
    def create_buttons(self):
        """Delegate to superclass create_buttons method if in main thread
        or queue the superclass method for execution in main thread.
        """
        if threading.current_thread().name == 'MainThread':
            super(WidgetAndLogPanel, self).create_buttons()
        else:
            self.get_appsys().do_ui_task(
                super(WidgetAndLogPanel, self).create_buttons)
