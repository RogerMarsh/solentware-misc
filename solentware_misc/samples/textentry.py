# textentry.py
# Copyright 2009 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Demonstrate text entry dialogue."""


if __name__ == "__main__":

    import tkinter

    from solentware_misc.gui.textentry import get_text_modal

    def enter():
        """Show the text entry dialogue."""
        get_text_modal(root)

    def quit_():
        """Quit application."""
        root.destroy()

    root = tkinter.Tk()
    root.wm_title("Text Entry dialogue")
    button = tkinter.Button(
        root, text="Enter Text", underline=0, command=enter
    )
    button.pack(side=tkinter.LEFT)
    button = tkinter.Button(root, text="Quit", underline=0, command=quit_)
    button.pack(side=tkinter.LEFT)
    root.mainloop()
