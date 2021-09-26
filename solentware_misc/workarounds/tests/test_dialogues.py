# test_dialogues.py
# Copyright 2021 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""dialogues tests"""

import unittest
import tkinter.messagebox
import tkinter.filedialog

from .. import dialogues


class DialoguesModuleNames(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_001_module_names_001(self):
        self.assertEqual(
            [n for n in dir(dialogues) if not n.startswith("__")],
            sorted(
                [
                    "BAD_WINDOW",
                    "DESTROYED_ERROR",
                    "FOCUS_ERROR",
                    "GRAB_ERROR",
                    "showinfo",
                    "showwarning",
                    "showerror",
                    "askquestion",
                    "askokcancel",
                    "askyesno",
                    "askyesnocancel",
                    "askretrycancel",
                    "askopenfilename",
                    "asksaveasfilename",
                    "askopenfilenames",
                    "askopenfile",
                    "askopenfiles",
                    "asksaveasfile",
                    "askdirectory",
                ]
            ),
        )

    def test_001_module_name_bindings_001(self):
        self.assertEqual(dialogues.BAD_WINDOW, 'bad window path name ".!')
        self.assertEqual(
            dialogues.DESTROYED_ERROR,
            (
                "".join(("can't invoke ", '"')),
                '" command:  application has been destroyed',
            ),
        )
        self.assertEqual(
            dialogues.FOCUS_ERROR,
            "focus".join(
                (
                    "".join(("can't invoke ", '"')),
                    '" command:  application has been destroyed',
                )
            ),
        )
        self.assertEqual(
            dialogues.GRAB_ERROR,
            "grab".join(
                (
                    "".join(("can't invoke ", '"')),
                    '" command:  application has been destroyed',
                )
            ),
        )
        self.assertEqual(dialogues.showinfo, tkinter.messagebox.showinfo)
        self.assertIs(dialogues.showwarning, tkinter.messagebox.showwarning)
        self.assertIs(dialogues.showerror, tkinter.messagebox.showerror)
        self.assertIs(dialogues.askquestion, tkinter.messagebox.askquestion)
        self.assertIs(dialogues.askokcancel, tkinter.messagebox.askokcancel)
        self.assertIs(dialogues.askyesno, tkinter.messagebox.askyesno)
        self.assertIs(
            dialogues.askyesnocancel, tkinter.messagebox.askyesnocancel
        )
        self.assertIs(
            dialogues.askretrycancel, tkinter.messagebox.askretrycancel
        )
        self.assertIs(
            dialogues.askopenfilename, tkinter.filedialog.askopenfilename
        )
        self.assertIs(
            dialogues.asksaveasfilename, tkinter.filedialog.asksaveasfilename
        )
        self.assertIs(
            dialogues.askopenfilenames, tkinter.filedialog.askopenfilenames
        )
        self.assertIs(dialogues.askopenfile, tkinter.filedialog.askopenfile)
        self.assertIs(dialogues.askopenfiles, tkinter.filedialog.askopenfiles)
        self.assertIs(
            dialogues.asksaveasfile, tkinter.filedialog.asksaveasfile
        )
        self.assertIs(dialogues.askdirectory, tkinter.filedialog.askdirectory)


if __name__ == "__main__":
    runner = unittest.TextTestRunner
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    runner().run(loader(DialoguesModuleNames))
