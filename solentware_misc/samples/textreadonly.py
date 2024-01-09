# textreadonly.py
# Copyright 2009 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Demonstrate subclass of Text widget with read only bindings."""


if __name__ == "__main__":
    import tkinter

    from solentware_misc.gui.textreadonly import (
        TextReadonly,
        make_text_readonly,
    )

    root = tkinter.Tk()
    doc = []
    for i in range(50):
        doc.append("a" * i)
        doc.append("\n")
    doc = "".join(doc)
    # Make one read only Text widget with the class
    tro = TextReadonly(root)
    tro.set_readonly_bindings()
    tro.pack(fill=tkinter.BOTH, expand=tkinter.TRUE)
    tro.insert(tkinter.END, doc)
    # and one with the maker function
    tro = make_text_readonly(root)
    tro.pack(fill=tkinter.BOTH, expand=tkinter.TRUE)
    tro.insert(tkinter.END, doc)
    root.mainloop()
