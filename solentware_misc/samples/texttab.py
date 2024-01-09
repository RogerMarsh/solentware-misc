# texttab.py
# Copyright 2009 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Demonstrate subclass of Text widget with Alt-Shift-Tab replacing Tab."""


if __name__ == "__main__":
    import tkinter

    from solentware_misc.gui.texttab import TextTab, make_text_tab

    root = tkinter.Tk()
    doc = []
    for i in range(50):
        doc.append("a" * i)
        doc.append("\n")
    doc = "".join(doc)
    # Make one read only Text widget with the class
    ttab = TextTab(root)
    ttab.set_tab_bindings()
    ttab.pack(fill=tkinter.BOTH, expand=tkinter.TRUE)
    ttab.insert(tkinter.END, doc)
    # and one with the maker function
    ttab = make_text_tab(root)
    ttab.pack(fill=tkinter.BOTH, expand=tkinter.TRUE)
    ttab.insert(tkinter.END, doc)
    bt = ttab.bindtags()
    print(bt)
    for t in bt:
        print(ttab.bind_class(t))
    root.mainloop()
