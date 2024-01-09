# colourslider.py
# Copyright 2009 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Demonstrate scale-like widgets for displaying colour choices."""


if __name__ == "__main__":
    import tkinter

    from solentware_misc.gui.colourslider import ColourSlider

    root = tkinter.Tk()
    root.grid_columnconfigure(0, weight=0)
    for c in range(1, 4):
        root.grid_columnconfigure(c, weight=1, uniform="csel")
    cs = ColourSlider(root, row=0, colour="cyan", label="Light squares")
    root.mainloop()
