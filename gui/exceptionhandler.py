# exceptionhandler.py
# Copyright 2011 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Intercept exceptions in methods called from Tkinter or threading

List of classes:

ExceptionHandler

List of functions:

None

"""

from basesup.tools.callbackexception import CallbackException


class ExceptionHandler(CallbackException):
    """Tkinter callback and threaded activity exception handler wrappers.

    Override methods provided by CallbackException class.

    Methods added:

    get_application_name
    get_error_file_name
    set_application_name
    set_error_file_name
    
    Methods overridden:

    try_command
    try_event
    try_thread

    Methods extended:

    report_exception
    
    """
    _application_name = None
    _error_file_name = None

    # Move to CallbackException eventually
    @staticmethod
    def get_application_name():
        """Return the application name."""
        return str(ExceptionHandler._application_name)

    # Move to CallbackException eventually
    @staticmethod
    def get_error_file_name():
        """Return the exception report file name."""
        # Assumes set_error_file_name has been called
        return ExceptionHandler._error_file_name

    def report_exception(self, root=None, title=None, message=None):
        """Extend to write exception to errorlog if available.

        root - usually the application toplevel widget
        title - usually the application name
        message - custom errorlog dialogue message if errorlog not available

        """
        import traceback
        import datetime

        if self.get_error_file_name() is not None:
            try:
                f = open(self.get_error_file_name(), 'ab')
                try:
                    f.write(
                        ''.join(
                            ('\n\n\n',
                             ' '.join(
                                 (self.get_application_name(),
                                  'exception report at',
                                  datetime.datetime.isoformat(
                                      datetime.datetime.today())
                                  )),
                             '\n\n',
                             traceback.format_exc(),
                             '\n\n',
                             ))
                        )
                finally:
                    f.close()
                    message = ''.join(
                    ('An exception has occured.\n\nThe exception report ',
                     'has been appended to the error file.\n\nClick "Yes" ',
                     'to see the detail\nor "No" to quit the application.',
                     ))
            except:
                message = ''.join(
                    ('An exception has occured.\n\nThe attempt to append ',
                     'the exception report to the error file was not ',
                     'completed.\n\nClick "Yes" to see the detail\nor ',
                     '"No" to quit the application.',
                 ))
        super(ExceptionHandler, self).report_exception(
            root=root, title=title, message=message)

    # Move to CallbackException eventually
    @staticmethod
    def set_application_name(application_name):
        """Set the exception report application name.

        The class attribute is set once per run.

        """
        if ExceptionHandler._application_name is None:
            ExceptionHandler._application_name = application_name

    # Move to CallbackException eventually
    @staticmethod
    def set_error_file_name(error_file_name):
        """Set the exception report file name."""
        ExceptionHandler._error_file_name = error_file_name

    def try_command(self, method, widget):
        """Return the method wrapped to write exception trace to error log.

        method - the command callback to be wrapped
        root - usually the application toplevel widget

        Copied and adapted from Tkinter.

        """
        def wrapped_command_method(*a, **k):
            try:
                return method(*a, **k)
            except SystemExit, message:
                raise SystemExit, message
            except:
                # If an unexpected exception occurs in report_exception let
                # Tkinter deal with it (better than just killing application
                # when Microsoft Windows User Access Control gets involved in
                # py2exe generated executables).
                self.report_exception(
                    root=widget.winfo_toplevel(),
                    title=self.get_application_name())
        return wrapped_command_method

    def try_event(self, method):
        """Return the method wrapped to write exception trace to error log.

        method - the event callback to be wrapped

        Copied and adapted from Tkinter.

        """
        def wrapped_event_method(e):
            try:
                return method(e)
            except SystemExit, message:
                raise SystemExit, message
            except:
                # If an unexpected exception occurs in report_exception let
                # Tkinter deal with it (better than just killing application
                # when Microsoft Windows User Access Control gets involved in
                # py2exe generated executables).
                self.report_exception(
                    root=e.widget.winfo_toplevel(),
                    title=self.get_application_name())
        return wrapped_event_method

    def try_thread(self, method, widget):
        """Return the method wrapped to write exception trace to error log.

        method - the threaded activity to be wrapped
        root - usually the application toplevel widget

        Copied and adapted from Tkinter.

        """
        def wrapped_thread_method(*a, **k):
            try:
                return method(*a, **k)
            except SystemExit, message:
                raise SystemExit, message
            except:
                # If an unexpected exception occurs in report_exception let
                # Tkinter deal with it (better than just killing application
                # when Microsoft Windows User Access Control gets involved in
                # py2exe generated executables).
                self.report_exception(
                    root=widget.winfo_toplevel(),
                    title=self.get_application_name())
        return wrapped_thread_method
