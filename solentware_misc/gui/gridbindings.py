# gridbindings.py
# Copyright 2009 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""This module provides classes which define event bindings common to
many grids in applications available on www.solentware.co.uk which have
a class from solentware_grid.datagrid as a superclass.

It is assumed solentware_grid.datagrid.DataGrid will be a superclass whenever
the classes in this module are a superclass, but behaviour when this is
not so is undefined.

"""

import tkinter

from .exceptionhandler import ExceptionHandler


class GridBindings(ExceptionHandler):

    """This class applies some standard bindings to data grids.

    """
    
    def __init__(self, receivefocuskey=None, appsyspanel=None, **kwargs):
        """Extend and bind grid row selection commands to popup menus.

        receivefocuskey -
        appsyspanel -
        **kwargs - ignored

        """
        super(GridBindings, self).__init__()
        self.receivefocuskey = receivefocuskey
        self.appsyspanel = appsyspanel
        self.make_focus_to_grid()
        for label, function, accelerator in (
            ('Select', self.select_from_popup, 'Left/Right Arrow'),
            ('Cancel Select',
             self.cancel_select_from_popup,
             'Control + Delete'),
            ('Select Visible',
             self.move_selection_to_popup_selection,
             'Control + L/R Arrow'),
            ('Bookmark', self.bookmark_from_popup, 'Alt + Ins'),
            ('Cancel Bookmark',
             self.cancel_bookmark_from_popup,
             'Alt + Delete'),
            ):
            self.menupopup.add_command(
                label=label,
                command=self.try_command(function, self.menupopup),
                accelerator=accelerator)

    def bindings(self):
        """Apply DataGrid's bindings to it's frame and scrollbar widgets."""
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
        """Give grid the focus."""
        if self.appsyspanel is not None:
            self.appsyspanel.give_focus(self.get_frame())
        self.focus_set_frame()
        
    def grid_bindings(self, siblings, *a, **ka):
        """Bind grid switching methods to all exposed widgets taking focus.

        siblings - iterable of widgets which can give focus to self
        *a - ignored
        **ka - ignored

        """
        widgets = (
            self.get_frame(),
            self.get_horizontal_scrollbar(),
            self.get_vertical_scrollbar())
        self.receive_focus(widgets[1:])
        for s in siblings:
            s.receive_focus(widgets)

    def make_focus_to_grid(self):
        """Create method to give focus to self and bind to self.focus_to_grid.

        Replaces any existing definition of self.focus_to_grid method.

        """
        def focus(event):
            self.give_and_set_focus()
        self.focus_to_grid = focus

    def receive_focus(self, widgets):
        """Bind take focus method to all exposed widgets taking focus.

        widgets - iterable of widgets which can be given focus from self

        """
        for w in widgets:
            w.bind(self.receivefocuskey, self.try_event(self.focus_to_grid))

    def select_from_popup(self):
        """Select row under pointer unless current selection not visible."""
        if len(self.selection):
            if self.selection[0] not in self.objects:
                return
        self.move_selection_to_popup_selection()

    def cancel_select_from_popup(self):
        """Cancel selection if selected row is under pointer."""
        if self.pointer_popup_selection in self.selection:
            self.cancel_visible_selection(self.pointer_popup_selection)

    def bookmark_from_popup(self):
        """Bookmark row under pointer."""
        self.add_bookmark(self.pointer_popup_selection)

    def cancel_bookmark_from_popup(self):
        """Cancel bookmark for row under pointer."""
        if self.pointer_popup_selection in self.bookmarks:
            self.cancel_bookmark(self.pointer_popup_selection)


class SelectorGridBindings(GridBindings):

    """Standard bindings for data grids with item selection.

    """
    """This class applies some standard bindings to data grids with data
    entry widgets for typing search text.

    """
    
    def __init__(
        self,
        selecthintlabel=None,
        setbinding=None,
        focus_selector=None,
        keypress_grid_to_select=True,
        **kwargs):
        """Extend and bind grid navigation within page commands to events.

        selecthintlabel
        setbinding
        focus_selector
        keypress_grid_to_select

        """
        super(SelectorGridBindings, self).__init__(**kwargs)
        if setbinding is None:
            self.position_grid_at_record = self.navigate_grid_by_key
        else:
            self.position_grid_at_record = setbinding
        self.selecthintlabel = selecthintlabel
        self.make_focus_to_grid()
        self.make_grid_bindings(
            setfocuskey=focus_selector,
            keypress_grid_to_select=keypress_grid_to_select)

    def bind_return(self,
                    setbinding=None,
                    clearbinding=None,
                    siblingargs=(),
                    slavegrids=()):
        """Set bindings for <Return> in selector Entry widgets.

        setbinding must be an iterable of Datagrids or None
        clearbinding must be a selector Entry widget or None or True
        siblingargs
        slavegrids - keystroke sequence to give focus to grid from selector
        
        """
        if self.appsyspanel is None:
            return
        gs = self.appsyspanel.gridselector
        if not setbinding:
            if setbinding is None:
                if clearbinding is True:
                    for w in gs.values():
                        w.bind(sequence='<KeyPress-Return>')
                        w.bind(sequence='<Control-KeyPress-Return>')
                else:
                    w = gs.get(clearbinding)
                    if w is not None:
                        w.bind(sequence='<KeyPress-Return>')
                        w.bind(sequence='<Control-KeyPress-Return>')
            return
        if setbinding is True:
            setbinding = (self,)
        w = gs.get(self)
        if w is not None:
            w.bind(
                sequence='<KeyPress-Return>',
                func=self.try_event(self.position_grid_at_record))
            slaved = {self}
            for s, sa in zip(setbinding, siblingargs):
                for sg in slavegrids:
                    if sg == sa['gridfocuskey']:
                        slaved.add(s)

            def position_grids(event=None):
                if not isinstance(event.widget, tkinter.Entry):
                    return False
                for g in slaved:
                    g.move_to_row_in_grid(event.widget.get())
                return True
            
            for s, sa in zip(setbinding, siblingargs):
                for sg in slavegrids:
                    if sg == sa['gridfocuskey']:
                        w.bind(
                            sequence='<Control-KeyPress-Return>',
                            func=self.try_event(position_grids))

    def bindings(self, function=None):
        """Extend to handle FocusIn event for superclass' frame.

        function - the function to bind to event

        """
        super(SelectorGridBindings, self).bindings()
        self.get_frame().bind(
            sequence='<FocusIn>', func=self.try_event(function))

    def focus_selector(self, event):
        """Give focus to the Entry for record selection."""
        if self.appsyspanel is None:
            return
        if self.appsyspanel.get_grid_selector(self) is not None:
            self.appsyspanel.give_focus(
                self.appsyspanel.get_grid_selector(self))
            self.appsyspanel.get_grid_selector(self).focus_set()
        return

    def keypress_selector(self, event):
        """Give focus to the Entry for record selection and set text."""
        if event.char.isalnum():
            if self.appsyspanel is None:
                return
            self.focus_selector(event)
            self.appsyspanel.get_grid_selector(self).delete(0, tkinter.END)
            self.appsyspanel.get_grid_selector(self).insert(
                tkinter.END, event.char)
        
    def make_focus_to_grid(self):
        """Create method to give focus to self and bind to self.focus_to_grid.

        Replaces any existing definition of self.focus_to_grid method.

        """
        def focus(event):
            self.set_select_hint_label()
            self.give_and_set_focus()
        self.focus_to_grid = focus

    def make_grid_bindings(self,
                           setfocuskey=None,
                           keypress_grid_to_select=True):
        """Create method to set event bindings and bind to self.grid_bindings.

        setfocuskey -
        The keypress_grid_to_select argument should be a boolean value.

        Replaces any existing definition of self.grid_bindings method.

        """
        if self.appsyspanel is None:
            return
        
        def bindings(siblings, siblingargs, slavegrids=(), **ka):
            widgets = (
                self.get_frame(),
                self.get_horizontal_scrollbar(),
                self.get_vertical_scrollbar(),
                self.appsyspanel.get_grid_selector(self))
            rfk = self.receivefocuskey[1:-1].split('-')
            rfk.insert(0, 'Control')
            defaultsetfocuskey = '-'.join(rfk).join(('<', '>'))
            self.receive_focus(widgets[1:])
            for s in siblings:
                s.receive_focus(widgets)
            if widgets[-1] is not None:
                for s in siblings:
                    ss = self.appsyspanel.get_grid_selector(s)
                    if widgets[-1] is not ss:
                        for w in (
                            ss,
                            s.get_frame(),
                            s.get_horizontal_scrollbar(),
                            s.get_vertical_scrollbar(),
                            ):
                            w.bind(
                                defaultsetfocuskey,
                                self.try_event(self.focus_selector))
                            if setfocuskey is not None:
                                w.bind(
                                    setfocuskey,
                                    self.try_event(self.focus_selector))
                for w in widgets[:-1]:
                    w.bind(
                        defaultsetfocuskey, self.try_event(self.focus_selector))
                    if setfocuskey is not None:
                        w.bind(setfocuskey, self.try_event(self.focus_selector))
                    if keypress_grid_to_select is True:
                        w.bind(
                            '<KeyPress>',
                            self.try_event(self.keypress_selector))
                # for shared selector __init__() targets last grid created
                self.bind_return(
                    setbinding=siblings,
                    siblingargs=siblingargs,
                    slavegrids=slavegrids)

        self.grid_bindings = bindings

    def on_focus_in(self, event=None):
        """Clear the record selector Entry."""
        if self.appsyspanel is None:
            return
        self.appsyspanel.get_active_grid_hint(self).configure(
            text=self.selecthintlabel)

    def set_select_hint_label(self):
        """Set the selection widget hint (to indicate selection target)."""
        if self.appsyspanel is None:
            return
        try:
            self.appsyspanel.get_active_grid_hint(self).configure(
                text=self.selecthintlabel)
        except tkinter._tkinter.TclError as error:
            #application destroyed while confirm dialogue exists
            if str(error) != ''.join((
                'invalid command name "',
                str(self.appsyspanel.get_active_grid_hint(self)),
                '"')):
                raise
        
