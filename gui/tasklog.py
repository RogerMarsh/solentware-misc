# tasklog.py
# Copyright 2013 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""This module provides classes which run tasks one at a time in a background
thread and log reported progress to a visible transaction log.

"""

import datetime
import tkinter
import tkinter.font
import queue
import threading

from .exceptionhandler import ExceptionHandler
from .textreadonly import TextReadonly


class TaskLog(ExceptionHandler):
    """Run a function in a separate thread and provide a progress report log.
    
    """

    def __init__(
        self,
        title='Action Log',
        get_app=None,
        cancelmethod=None,
        logwidget=None,
        ):
        """Configure class instance for it's environment.

        title - tasklog title text.
        get_app - method which returns the application instance.
        cancelmethod - method called when Cancel button clicked.
        logwidget - tasklog Toplevel widget.
        """
        super(TaskLog, self).__init__()
        self._title = title
        self.get_app = get_app
        if callable(get_app):
            self._threadqueue = get_app().get_thread_queue()
        else:
            self._threadqueue = None
        self._cancelmethod = cancelmethod
        self.logwidget = logwidget
        self.report = logwidget

    def _create_log_widget(self):
        """Create the log widget, usually after scheduling the task."""
        if self.logwidget is not None:
            # Assume the log widget has been created already.
            return
        self.logwidget = tkinter.Toplevel()
        self.logwidget.wm_title(self._title)
        frame = tkinter.Frame(master=self.logwidget)
        frame.pack(side=tkinter.BOTTOM)
        self.buttonframe = tkinter.Frame(master=frame)
        self.buttonframe.pack(side=tkinter.BOTTOM)
        self.message = tkinter.Label(master=frame, wraplength=500)
        self.message.pack(side=tkinter.BOTTOM)
        self.cancel = tkinter.Button(
            master=self.buttonframe,
            text='Cancel',
            command=self.try_command(
                self.do_cancel, self.buttonframe))
        self.cancel.pack(side=tkinter.RIGHT, padx=12)
        self.report = LogText(
            master=self.logwidget,
            wrap='word',
            undo=tkinter.FALSE,
            get_app=self.get_app,
            )
        self.report.pack(
            side=tkinter.LEFT, fill=tkinter.BOTH, expand=tkinter.TRUE)
        self.logwidget.iconify()
        self.logwidget.update()
        self.logwidget.deiconify()

    def add_button(self, text, command=None):
        """Add a button to the right of the current buttons.

        text - button label text
        command - method invoked when button clicked.
        """
        button = tkinter.Button(
            master=self.buttonframe,
            text=text,
            command=self.try_command(command, self.buttonframe))
        button.pack(side=tkinter.RIGHT, padx=12)
        return button

    def append_text(self, text, timestamp=True):
        """Append an item to the log widget with timestamp by default.

        text - text to be appended to log.
        timestamp - if True timestamp the entry.
        """
        self.report.append_text(text, timestamp=timestamp)

    def append_text_only(self, text):
        """Append an item to the log widget without timestamp.

        text - text to be appended to log.
        """
        self.report.append_text(text, timestamp=False)
            
    def do_cancel(self):
        """Cancel button action."""
        if self._threadqueue.queue.unfinished_tasks == 0:
            if callable(self._cancelmethod):
                self._cancelmethod()
            self.logwidget.destroy()
            
    def run_method(self, method, message=None, args=(), kwargs={}):
        """Add the task method to queue for processing in separate thread.

        method - method to be run in separate thread.
        message - log entry if method is placed on queue for running.
        args - positional arguments for method.
        kwargs - keyword arguments for method.
        """
        self._create_log_widget()
        if not callable(method):
            self.report.append_text(''.join(
                ('No action.  Must be either an error in Application or a ',
                 'feature that has not been implemented.',
                 )))
        elif self._threadqueue:
            kwargs['logwidget'] = self.report
            try:
                self._threadqueue.put_method(
                    self.try_command(method, self.logwidget),
                    args,
                    kwargs)
                if isinstance(message, str):
                    self.report.append_text(message)
            except queue.Full:
                self.report.append_text(
                    'Application busy.  Please try again shortly.')
        else:
            self.report.append_text(''.join(
                ('Action in progress but application will be unresponsive ',
                 'until it is finished',
                 )))
            self.try_command(method, self.logwidget)(*args, **kwargs)


class _LogText(TextReadonly):
    """A progress report log.
    
    """

    def __init__(self, get_app=None, master=None, cnf={}, **kargs):
        """Add a vertical scrollbar to a read-only tkinter.Text widget.

        get_app - method which returns the application instance.
        master - parent widget for log widget.
        cnf - ignored
        **kargs - passed to superclass as **kargs argument.
        """
        super(_LogText, self).__init__(master=master, cnf={}, **kargs)
        self.get_app = get_app
        self.set_readonly_bindings()
        scrollbar = tkinter.Scrollbar(
            master,
            orient=tkinter.VERTICAL,
            command=self.yview)
        self.configure(yscrollcommand=scrollbar.set)
        self.tag_configure(
            'margin',
            lmargin2=tkinter.font.nametofont(
                self.cget('font')).measure('2010-05-23 10:20:57  '))
        scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=tkinter.TRUE)
        self.tagstart = '1.0'

    def append_bytestring(self, text, timestamp=True):
        """Append text to the log widget with timestamp by default.

        text - a bytestring.
        timestamp - if True the entry is timestamped.
        """
        if timestamp:
            day, time = datetime.datetime.isoformat(
                datetime.datetime.today()).encode('utf8').split(b'T')
            time = time.split(b'.')[0]
            self.insert(
                tkinter.END,
                b''.join((day, b' ', time, b'  ', text, b'\n')))
        else:
            self.insert(
                tkinter.END,
                b''.join((b'                     ', text, b'\n')))
        try:
            self.tag_add('margin', self.tagstart, tkinter.END)
        except:
            self.tag_add('margin', '1.0', tkinter.END)
        self.tagstart = self.index(tkinter.END)
        self.see(tkinter.END)

    def append_text(self, text, timestamp=True):
        """Append text to the log widget with timestamp by default.

        text - a str.
        timestamp - if True the entry is timestamped.
        """
        if timestamp:
            day, time = datetime.datetime.isoformat(
                datetime.datetime.today()).split('T')
            time = time.split('.')[0]
            self.insert(
                tkinter.END,
                ''.join((day, ' ', time, '  ', text, '\n')))
        else:
            self.insert(
                tkinter.END,
                ''.join(('                     ', text, '\n')))
        try:
            self.tag_add('margin', self.tagstart, tkinter.END)
        except:
            self.tag_add('margin', '1.0', tkinter.END)
        self.tagstart = self.index(tkinter.END)
        self.see(tkinter.END)

    def append_bytestring_only(self, text):
        """Append text to the log widget without timestamp.

        text - a bytestring.
        """
        self.append_bytestring(text, timestamp=False)

    def append_text_only(self, text):
        """Append text to the log widget without timestamp.

        text - a str.
        """
        self.append_text(text, timestamp=False)


class LogText(_LogText):
    """Arrange for items to be added to log in the main thread of application.

    This is required on Microsoft Windows, and it is simplest to do so always.

    If in main thread just append the text to the widget, otherwise put an
    entry on the queue read periodically in main thread to get these requests
    and process them.

    It is assumed that caller of LogText(...) arranges for call to be made in
    the main thread.
    
    """

    def append_bytestring(self, text, timestamp=True):
        """Delegate to superclass in main thread otherwise add entry to queue
        for running in main thread.

        The queue entry is a tuple:
        (super().append_bytestring, (text,), dict(timestamp=timestamp)).
        """
        if threading.current_thread().name == 'MainThread':
            super(LogText, self).append_bytestring(
                text, timestamp=timestamp)
        else:
            self.get_app().get_reportqueue().put(
                (super(LogText, self).append_bytestring,
                 (text,),
                 dict(timestamp=timestamp)))

    def append_text(self, text, timestamp=True):
        """Delegate to superclass in main thread otherwise add entry to queue
        for running in main thread.

        The queue entry is a tuple:
        (super().append_text, (text,), dict(timestamp=timestamp)).
        """
        if threading.current_thread().name == 'MainThread':
            super(LogText, self).append_text(text, timestamp=timestamp)
        else:
            self.get_app().get_reportqueue().put(
                (super(LogText, self).append_text,
                 (text,),
                 dict(timestamp=timestamp)))
