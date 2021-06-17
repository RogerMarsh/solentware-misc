# fontchooser.py
# Copyright 2009 Roger Marsh
# License: See LICENSE.TXT (BSD license)

"""A font chooser dialogue.

List of classes:

AppSysFontChooser

"""

import Tkinter
import tkFont

import basesup.tools.dialogues


class AppSysFontChooser(object):
    
    """Font chooser

    Methods added:

    get_chosen_font
    create_buttons
    on_cancel
    on_ok
    on_show_font
    __del__

    Methods overridden:

    __init__

    Methods extended:

    None
    
    """

    def __init__(self, master, title, cnf=dict(), **kargs):

        self.chosenfont = None

        self.confirm = Tkinter.Toplevel(master)
        self.confirm.wm_title(title)
        self.buttons_frame = Tkinter.Frame(master=self.confirm)
        self.buttons_frame.pack(side=Tkinter.BOTTOM, fill=Tkinter.X)
        self.create_buttons()

        self.fontpanel = framefonts = Tkinter.Frame(self.confirm)
        self.families = Tkinter.Listbox(framefonts)
        scrollfont = Tkinter.Scrollbar(framefonts)
        scrollfont.configure(command=self.families.yview)
        self.families.configure(yscrollcommand=scrollfont.set)
        for f in sorted(tkFont.families()):
            self.families.insert(Tkinter.END, f)
        self.families.pack(
            side = Tkinter.LEFT, expand=Tkinter.TRUE, fill=Tkinter.X)
        scrollfont.pack(side=Tkinter.LEFT, fill=Tkinter.Y)
        framefonts.pack(fill=Tkinter.X)

        wssf = Tkinter.Frame(master=self.confirm)
        self.weight = Tkinter.IntVar()
        self.slant = Tkinter.IntVar()
        self.normal = Tkinter.Radiobutton(
            master=wssf, text='Normal', variable=self.weight, value=1,
            command=self.on_show_font)
        self.bold = Tkinter.Radiobutton(
            master=wssf, text='Bold', variable=self.weight, value=2,
            command=self.on_show_font)
        self.roman = Tkinter.Radiobutton(
            master=wssf, text='Roman', variable=self.slant, value=1,
            command=self.on_show_font)
        self.italic = Tkinter.Radiobutton(
            master=wssf, text='Italic', variable=self.slant, value=2,
            command=self.on_show_font)
        Tkinter.Label(master=wssf, text='Size').grid_configure(
            column=1, row=3)
        self.normal.grid_configure(column=0, row=0)
        self.bold.grid_configure(column=0, row=1)
        self.roman.grid_configure(column=2, row=0)
        self.italic.grid_configure(column=2, row=1)
        wssf.grid_columnconfigure(0, weight=1)
        wssf.grid_columnconfigure(1, weight=1)
        wssf.grid_columnconfigure(2, weight=1)
        wssf.grid_columnconfigure(3, weight=1)
        wssf.pack(fill=Tkinter.X)

        sf = Tkinter.Frame(master=self.confirm)
        self.size = Tkinter.IntVar()
        for i, s in enumerate((7, 8, 9, 10, 11, 12, 13, 14, 16, 18, 20)):
            sb = Tkinter.Radiobutton(
                master=sf, text=str(s), variable=self.size, value=s,
                indicatoron=0, command=self.on_show_font)
            sb.grid_configure(column=i, row=0, sticky='ew')
            sf.grid_columnconfigure(i, weight=1, uniform='fsb')
        sf.pack(fill=Tkinter.X)

        self.families.bind('<<ListboxSelect>>', self.on_show_font)

        self.sample = Tkinter.Label(self.confirm)
        self.sample.pack(fill=Tkinter.BOTH, expand=Tkinter.TRUE)

        self.restore_focus = self.confirm.focus_get()
        self.confirm.wait_visibility()
        self.confirm.grab_set()
        self.confirm.wait_window()

    def get_chosen_font(self):
        return self.chosenfont

    def create_buttons(self):

        buttons = (
            ('OK',
             'OK button Tooltip.',
             True,
             -1,
             self.on_ok),
            ('Cancel',
             'OK button Tooltip.',
             True,
             -1,
             self.on_cancel),
            )

        buttonrow = self.buttons_frame.pack_info()['side'] in ('top', 'bottom')

        for i, b in enumerate(buttons):
            button = Tkinter.Button(
                master=self.buttons_frame,
                text=buttons[i][0],
                underline=buttons[i][3],
                command=buttons[i][4])
            if buttonrow:
                self.buttons_frame.grid_columnconfigure(i*2, weight=1)
                button.grid_configure(column=i*2 + 1, row=0)
            else:
                self.buttons_frame.grid_rowconfigure(i*2, weight=1)
                button.grid_configure(row=i*2 + 1, column=0)
        if buttonrow:
            self.buttons_frame.grid_columnconfigure(
                len(buttons*2), weight=1)
        else:
            self.buttons_frame.grid_rowconfigure(
                len(buttons*2), weight=1)

    def on_cancel(self, event=None):
        self.confirm.destroy()

    def on_ok(self, event=None):
        if self.chosenfont:
            self.confirm.destroy()
        else:
            basesup.tools.dialogues.showerror(
                title='Font Chooser',
                message='No font chosen')

    def on_show_font(self, event=None):

        selection = self.families.curselection()
        if not selection:
            basesup.tools.dialogues.showerror(
                title='Font Chooser',
                message='No font chosen')
            return

        if self.weight.get() == 2:
            weight = tkFont.BOLD
        else:
            weight = tkFont.NORMAL
        if self.slant.get() == 2:
            slant = tkFont.ITALIC
        else:
            slant = tkFont.ROMAN
        size = self.size.get()
        if not size:
            size = 12
        self.chosenfont = tkFont.Font(
            family=self.families.get(selection[0]),
            weight=weight,
            slant=slant,
            size=size)
        self.sample.configure(
            font=self.chosenfont,
            text='\n'.join((
                'ABCDEFGHIJKLMNOPQRSTWXYZ',
                'abcdefghijklmnopqrstuvwxyz',
                '0123456789',
                '!@#$%^&*()-_=+[{]};:"\|,<.>/?`~',
                )))

    def __del__(self):
        self.chosenfont = None
        try:
            #restore focus on dismissing dialogue
            self.restore_focus.focus_set()
        except Tkinter._tkinter.TclError, error:
            #application destroyed while confirm dialogue exists
            if str(error) != basesup.tools.dialogues.FOCUS_ERROR:
                raise

