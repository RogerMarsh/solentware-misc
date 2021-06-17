# gridbindings.py
# Copyright 2009 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Database grid common event bindings and methods

List of classes

GridBindings - grid decorator bindings for scrollbars buttons and so on
SelectorGridBindings - extend GridBindings to record selector Entry widget

"""

import Tkinter


class GridBindings(object):

    """Standard bindings for data grids.

    Methods added:

    bindings
    give_and_set_focus
    grid_bindings
    make_focus_to_grid
    receive_focus
    
    Methods overridden:

    None
    
    Methods extended:

    __init__

    """
    
    def __init__(self, receivefocuskey=None, appsyspanel=None, **kwargs):
        """Extend and bind grid navigation within page commands to events"""
        super(GridBindings, self).__init__()
        self.receivefocuskey = receivefocuskey
        self.appsyspanel = appsyspanel
        self.make_focus_to_grid()

    def bindings(self):
        # Assume, for now, that appsyspanel frame instance bindtag is to
        # be inserted at front of grid instance bindtags
        if self.appsyspanel:
            for w in (
                self.get_horizontal_scrollbar(),
                self.get_vertical_scrollbar()):
                w.configure(highlightthickness=1)
                gridtags = list(w.bindtags())
                gridtags.insert(
                    0, self.appsyspanel.get_appsys().explicit_focus_tag)
                w.bindtags(tuple(gridtags))
            bindings = self.appsyspanel.get_widget().bindtags()[0]
            for w in (
                self.get_frame(),
                self.get_horizontal_scrollbar(),
                self.get_vertical_scrollbar()):
                gridtags = list(w.bindtags())
                gridtags.insert(0, bindings)
                w.bindtags(tuple(gridtags))

    def give_and_set_focus(self):
        if self.appsyspanel is not None:
            self.appsyspanel.give_focus(self.get_frame())
        self.focus_set_frame()
        
    def grid_bindings(self, siblings):
        """Bind grid switching methods to all exposed widgets taking focus"""
        widgets = (
            self.get_frame(),
            self.get_horizontal_scrollbar(),
            self.get_vertical_scrollbar())
        self.receive_focus(widgets[1:])
        for s in siblings:
            s.receive_focus(widgets)

    def make_focus_to_grid(self, setbinding=None):
        """Give focus to self"""
        def focus(event):
            self.give_and_set_focus()
        self.focus_to_grid = focus

    def receive_focus(self, widgets):
        """Bind take focus method to all exposed widgets taking focus"""
        for w in widgets:
            w.bind(self.receivefocuskey, self.focus_to_grid)


class SelectorGridBindings(GridBindings):

    """Standard bindings for data grids with item selection.

    Methods added:

    bind_return
    focus_selector
    on_focus_in
    keypress_selector
    make_grid_bindings
    set_select_hint_label
    
    
    Methods overridden:

    make_focus_to_grid
    
    Methods extended:

    bindings

    """
    
    def __init__(
        self,
        selecthintlabel=None,
        setbinding=None,
        focus_selector=None,
        **kwargs):
        """Extend and bind grid navigation within page commands to events"""
        super(SelectorGridBindings, self).__init__(**kwargs)
        if setbinding is None:
            self.position_grid_at_record = self.navigate_grid_by_key
        else:
            self.position_grid_at_record = setbinding
        self.selecthintlabel = selecthintlabel
        self.make_focus_to_grid(setbinding=self.position_grid_at_record)
        self.make_grid_bindings(setfocuskey=focus_selector)

    def bind_return(self, setbinding=None, clearbinding=None):
        """Set bindings for <Return> in selector Entry widgets.

        setbinding must be a bound method or None
        clearbinding must be a selector Entry widget or None or True
        
        """
        gs = self.appsyspanel.gridselector
        if setbinding is None:
            if clearbinding is True:
                for w in gs.itervalues():
                    w.bind(sequence='<KeyPress-Return>')
            else:
                w = gs.get(clearbinding)
                if w is not None:
                    w.bind(sequence='<KeyPress-Return>')
        else:
            w = gs.get(setbinding.__self__)
            if w is not None:
                w.bind(sequence='<KeyPress-Return>', func=setbinding)

    def bindings(self, function=None):
        """Extend to handle FocusIn event for superclass' frame"""
        super(SelectorGridBindings, self).bindings()
        self.get_frame().bind(sequence='<FocusIn>', func=function)

    def focus_selector(self, event):
        """Give focus to the Entry for record selection"""
        if self.appsyspanel.get_grid_selector(self) is not None:
            self.appsyspanel.give_focus(
                self.appsyspanel.get_grid_selector(self))
            self.appsyspanel.get_grid_selector(self).focus_set()
        return

    def keypress_selector(self, event):
        """Give focus to the Entry for record selection and set text"""
        if event.char.isalnum():
            self.focus_selector(event)
            self.appsyspanel.get_grid_selector(self).delete(0, Tkinter.END)
            self.appsyspanel.get_grid_selector(self).insert(
                Tkinter.END, event.char)
        
    def make_focus_to_grid(self, setbinding=None):
        """Give focus to self"""
        def focus(event):
            self.set_select_hint_label()
            self.bind_return(setbinding=self.position_grid_at_record)
            self.give_and_set_focus()
        self.focus_to_grid = focus

    def make_grid_bindings(self, setfocuskey=None):
        """Bind grid switching methods to all exposed widgets taking focus"""
        def bindings(siblings):
            widgets = (
                self.get_frame(),
                self.get_horizontal_scrollbar(),
                self.get_vertical_scrollbar(),
                self.appsyspanel.get_grid_selector(self))
            self.receive_focus(widgets[1:])
            for s in siblings:
                s.receive_focus(widgets)
            if widgets[-1] is not None:
                for w in widgets[:-1]:
                    w.bind(setfocuskey, self.focus_selector)
                    w.bind('<KeyRelease>', self.keypress_selector)
                # for shared selector __init__() targets last grid created
                self.bind_return(setbinding=self.position_grid_at_record)
        self.grid_bindings = bindings

    def on_focus_in(self, event=None):
        """Clear the record selector Entry."""
        self.appsyspanel.get_active_grid_hint(self).configure(
            text=self.selecthintlabel)

    def set_select_hint_label(self):
        try:
            self.appsyspanel.get_active_grid_hint(self).configure(
                text=self.selecthintlabel)
        except Tkinter._tkinter.TclError, error:
            #application destroyed while confirm dialogue exists
            if str(error) != ''.join((
                'invalid command name "',
                str(self.appsyspanel.get_active_grid_hint(self)),
                '"')):
                raise
        
