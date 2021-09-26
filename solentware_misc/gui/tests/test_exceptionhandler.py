# test_exceptionhandler.py
# Copyright 2021 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""exceptionhandler tests."""

import unittest
import tkinter

from .. import exceptionhandler


class ExceptionHandler(unittest.TestCase):
    def setUp(self):
        self.exceptionhandler = exceptionhandler.ExceptionHandler()

    def tearDown(self):
        pass

    def test_001_module_constants_001(self):
        self.assertEqual(
            exceptionhandler.BAD_WINDOW, 'bad window path name ".!'
        )
        self.assertEqual(
            exceptionhandler.DESTROYED_ERROR,
            (
                "".join(("can't invoke ", '"')),
                '" command:  application has been destroyed',
            ),
        )
        self.assertEqual(
            exceptionhandler.GRAB_ERROR,
            "grab".join(
                (
                    "".join(("can't invoke ", '"')),
                    '" command:  application has been destroyed',
                )
            ),
        )
        self.assertEqual(
            exceptionhandler.FOCUS_ERROR,
            "focus".join(
                (
                    "".join(("can't invoke ", '"')),
                    '" command:  application has been destroyed',
                )
            ),
        )
        self.assertEqual(
            exceptionhandler.DESTROY_ERROR,
            "destroy".join(
                (
                    "".join(("can't invoke ", '"')),
                    '" command:  application has been destroyed',
                )
            ),
        )

    def test_002_class_attributes_001(self):
        self.assertEqual(
            sorted(
                n
                for n in dir(exceptionhandler.ExceptionHandler)
                if not n.startswith("__") and not n.endswith("__")
            ),
            [
                "_application_name",
                "_error_file_name",
                "get_application_name",
                "get_error_file_name",
                "report_exception",
                "set_application_name",
                "set_error_file_name",
                "try_command",
                "try_event",
                "try_thread",
            ],
        )

    def test_002_class_attributes_002(self):
        self.assertEqual(
            exceptionhandler.ExceptionHandler._application_name, None
        )
        self.assertEqual(
            exceptionhandler.ExceptionHandler._error_file_name, None
        )

    def test_003_get_application_name_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "get_application_name\(\) takes 0 positional arguments ",
                    "but 1 was given",
                )
            ),
            self.exceptionhandler.get_application_name,
            *(None,),
        )

    def test_003_get_application_name_002(self):
        self.assertEqual(self.exceptionhandler.get_application_name(), "None")

    def test_004_get_error_file_name_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "get_error_file_name\(\) takes 0 positional arguments ",
                    "but 1 was given",
                )
            ),
            self.exceptionhandler.get_error_file_name,
            *(None,),
        )

    def test_004_get_error_file_name_002(self):
        self.assertEqual(self.exceptionhandler.get_error_file_name(), None)

    def test_005_report_exception_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "report_exception\(\) takes from 1 to 4 positional ",
                    "arguments but 5 were given",
                )
            ),
            self.exceptionhandler.report_exception,
            *(None, None, None, None),
        )

    def test_005_report_exception_002(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "report_exception\(\) got an unexpected keyword ",
                    "argument 'badkey'",
                )
            ),
            self.exceptionhandler.report_exception,
            **dict(root=None, title=None, message=None, badkey=None),
        )

    def test_006_set_application_name_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "set_application_name\(\) missing 1 required positional ",
                    "argument: 'application_name'",
                )
            ),
            self.exceptionhandler.set_application_name,
        )

    def test_006_set_application_name_002(self):
        self.assertEqual(
            self.exceptionhandler.set_application_name("App"), None
        )
        self.assertEqual(
            exceptionhandler.ExceptionHandler._application_name, "App"
        )
        self.assertEqual(
            self.exceptionhandler.set_application_name("NewApp"), None
        )
        self.assertEqual(
            exceptionhandler.ExceptionHandler._application_name, "App"
        )

    def test_007_set_error_file_name_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "set_error_file_name\(\) missing 1 required positional ",
                    "argument: 'error_file_name'",
                )
            ),
            self.exceptionhandler.set_error_file_name,
        )

    def test_007_set_error_file_name_002(self):
        self.assertEqual(
            self.exceptionhandler.set_error_file_name("file"), None
        )
        self.assertEqual(
            exceptionhandler.ExceptionHandler._error_file_name, "file"
        )
        self.assertEqual(
            self.exceptionhandler.set_error_file_name("newfile"), None
        )
        self.assertEqual(
            exceptionhandler.ExceptionHandler._error_file_name, "newfile"
        )

    def test_008_try_command_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "try_command\(\) missing 2 required positional ",
                    "arguments: 'method' and 'widget'",
                )
            ),
            self.exceptionhandler.try_command,
        )

    def test_008_try_command_002(self):
        def m():
            pass

        f = self.exceptionhandler.try_command(m, tkinter.Label)
        self.assertEqual(type(f), type(m))

    def test_009_try_event_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "try_event\(\) missing 1 required positional ",
                    "argument: 'method'",
                )
            ),
            self.exceptionhandler.try_event,
        )

    def test_009_try_event_002(self):
        def m():
            pass

        f = self.exceptionhandler.try_event(m)
        self.assertEqual(type(f), type(m))

    def test_010_try_thread_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "try_thread\(\) missing 2 required positional ",
                    "arguments: 'method' and 'widget'",
                )
            ),
            self.exceptionhandler.try_thread,
        )

    def test_010_try_thread_002(self):
        def m():
            pass

        f = self.exceptionhandler.try_thread(m, tkinter.Label)
        self.assertEqual(type(f), type(m))


if __name__ == "__main__":
    runner = unittest.TextTestRunner
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    runner().run(loader(ExceptionHandler))
