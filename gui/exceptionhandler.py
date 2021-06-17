# exceptionhandler.py
# Copyright 2011 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""The ExceptionHandler class provides methods to intercept exceptions in
methods called from tkinter or threading and write the exception details to
the errorlog file before offering the option to display the exception
details.

The module expects the solentware_grid package, a sibling of solentware_misc,
to be installed but provides a minimal alternative if it is not installed.
"""

try:
    from solentware_grid.gui.callbackexception import CallbackException
except ModuleNotFoundError:


    class CallbackException(object):
        """Provide a minimal emulation of solentware_grid's CallbackException
        class which is used if import solentware_grid.gui.callbackexception
        raises ModuleNotFoundError.
        """

        def report_exception(self, **k):
            """Do nothing."""

        def try_command(self, method, widget):
            """Return the method.  Subclasses of solentware_grid's
            CallbackException class are expected, but not obliged, to override
            the method.
            """
            return method

        def try_event(self, method):
            """Return the method.  Subclasses of solentware_grid's
            CallbackException class are expected, but not obliged, to override
            the method.
            """
            return method

        def try_thread(self, method, widget):
            """Return the method.  Subclasses of solentware_grid's
            CallbackException class are expected, but not obliged, to override
            the method.
            """
            return method


class ExceptionHandler(CallbackException):
    """Adapt methods in superclass to provide behaviour needed by
    applications on www.solentware.co.uk.

    Exception details are written to the application's error log before
    offering the option to display the exception details in a dialogue.
    
    """
    _application_name = None
    _error_file_name = None

    @staticmethod
    def get_application_name():
        """Return the application name."""
        return str(ExceptionHandler._application_name)

    @staticmethod
    def get_error_file_name():
        """Return the exception report file name."""
        # Assumes set_error_file_name has been called
        return ExceptionHandler._error_file_name

    def report_exception(self, root=None, title=None, message=None):
        """Extend to write exception to errorlog if available.

        root - usually the application toplevel widget
        title - usually the application name
        message - usually the dialogue message if errorlog not available

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
                             )).encode('iso-8859-1')
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

    @staticmethod
    def set_application_name(application_name):
        """Set the exception report application name.

        The class attribute is set once per run.

        """
        if ExceptionHandler._application_name is None:
            ExceptionHandler._application_name = application_name

    @staticmethod
    def set_error_file_name(error_file_name):
        """Set the exception report file name."""
        ExceptionHandler._error_file_name = error_file_name

    def try_command(self, method, widget):
        """Return the method wrapped to call report_exception if an
        exception occurs.

        method - the command callback to be wrapped
        widget - usually the application toplevel widget

        Copied and adapted from Tkinter.

        """
        def wrapped_command_method(*a, **k):
            try:
                return method(*a, **k)
            except SystemExit as message:
                raise SystemExit(message)
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
        """Return the method wrapped to call report_exception if an
        exception occurs.

        method - the event callback to be wrapped

        Copied and adapted from Tkinter.

        """
        def wrapped_event_method(e):
            try:
                return method(e)
            except SystemExit as message:
                raise SystemExit(message)
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
        """Return the method wrapped to call report_exception if an
        exception occurs.

        method - the threaded activity to be wrapped
        widget - usually the application toplevel widget

        Copied and adapted from Tkinter.

        """
        def wrapped_thread_method(*a, **k):
            try:
                return method(*a, **k)
            except SystemExit as message:
                raise SystemExit(message)
            except:
                # If an unexpected exception occurs in report_exception let
                # Tkinter deal with it (better than just killing application
                # when Microsoft Windows User Access Control gets involved in
                # py2exe generated executables).
                self.report_exception(
                    root=widget.winfo_toplevel(),
                    title=self.get_application_name())
        return wrapped_thread_method
