# fontchooser.py
# Copyright 2009 Roger Marsh
# License: See LICENSE.TXT (BSD license)

"""Demonstrate font chooser dialogue."""


if __name__ == "__main__":

    import tkinter

    from solentware_misc.gui.fontchooser import AppSysFontChooser

    class mApp(object):
        """Define a simple font chooser application."""

        def __init__(self):
            """Define the font chooser widget."""
            self.root = tkinter.Tk()
            self.root.wm_title("Test Font Chooser")
            self.button = tkinter.Button(
                self.root, text="Select Font", command=self.Select
            )
            self.button.pack()

        def Select(self, event=None):
            """Display the font chooser widget."""
            AppSysFontChooser(self.root, "Select a font")

    app = mApp()
    app.root.mainloop()
