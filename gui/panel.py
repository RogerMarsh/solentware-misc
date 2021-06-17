# panel.py
# Copyright 2007 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""This module provides base classes for pages in notebook style user
interfaces.

The classes are written to work with the classes provided in the frame
module.

The *Grid* classes assume the solentware_grid.datagrid classes are available,
and behaviour is undefined if the solentware_grid package is not available.

"""

import tkinter

from .exceptionhandler import ExceptionHandler


class AppSysPanelError(Exception):
    pass


class AppSysPanelButton(ExceptionHandler):
    """This class creates a tkinter.Button and places it on the parent's
    frame reserved for buttons.
    
    """
    
    def __init__(self, parent, identity, switchpanel, cnf=dict(), **kargs):
        """Create page action button.

        parent - parent AppSysPanel.
        identity - arbitrary identity number for button.
        switchpanel - if True button is allowed to change page in notebook.
        cnf - passed to tkinter.Button() as cnf argument.
        **kargs - passed to tkinter.Button() as **kargs.

        The identity must be unique within the application for buttons.  It
        is used to keep track of context while navigating tabs.

        """
        self.parent = parent
        self.switchpanel = switchpanel
        self.identity = identity
        self.command = kargs.get('command')
        try:
            del kargs['command']
        except:
            pass

        self.button = tkinter.Button(
            master=parent.get_buttons_frame(),
            cnf=cnf,
            **kargs)
        
        self.obeycontextswitch = True

        tags = list(self.button.bindtags())
        tags.insert(0, parent.get_appsys().explicit_focus_tag)
        self.button.bindtags(tuple(tags))

    def bind_panel_button(self):
        """Bind key and button events to button actions."""
        if self.switchpanel:

            def switch_context(event):
                # invoke the AppSysPanel or the AppSysFrame (via appsys
                # attribute of AppSysPanel) switch_context method
                self.parent.switch_context(button=self.identity)
        
        self.button.bind(
            sequence=''.join((
                '<ButtonPress-1>')),
            func=self.try_event(self.command))
        self.button.bind(
            sequence='<KeyPress-Return>',
            func=self.try_event(self.command))
        if self.switchpanel:
            for f in (self.switch_context_check, switch_context):
                self.button.bind(
                    sequence=''.join((
                        '<ButtonPress-1>')),
                    func=self.try_event(f),
                    add=True)
                self.button.bind(
                    sequence='<KeyPress-Return>',
                    func=self.try_event(f),
                    add=True)

        conf = self.button.configure()
        underline = conf['underline'][-1]
        text = conf['text'][-1]
        if isinstance(text, tuple):
            text = ' '.join(text)
        try:
            if not underline < 0:
                self.parent.get_widget().bind(
                    sequence=''.join((
                        '<Alt-KeyPress-',
                        text[underline].lower(),
                        '>')),
                    func=self.try_event(self.command))
                if self.switchpanel:
                    for f in (self.switch_context_check, switch_context):
                        self.parent.get_widget().bind(
                            sequence=''.join((
                                '<Alt-KeyPress-',
                                text[underline].lower(),
                                '>')),
                            func=self.try_event(f),
                            add=True)
        except:
            print('AppSysPanelButton bind exception', self.identity)
            pass

    def inhibit_context_switch(self):
        """Inhibit change of panel displayed.

        Usually called when validation before an action proceeds has not
        been passed.

        """
        self.obeycontextswitch = False

    def obey_context_switch(self):
        """Return self.obeycontextswitch value prior to setting it True.

        Validation may occur prior to performing an action.  obeycontextswitch
        should be True when an action is invoked and set False during
        validation if needed.  This method is used to check if navigation
        may proceed at end of validation and set obeycontextswitch True for
        the next action invoked.

        """
        v, self.obeycontextswitch = self.obeycontextswitch, True
        return v

    def raise_action_button(self):
        """Raise button in stacking order.

        When called for buttons in the order they appear on the panel gives
        a sensible tab order provided buttons are in a dedicated frame.

        """
        self.button.tkraise()

    def switch_context_check(self, event=None):
        """Return 'break' to tk interpreter if obey_context_switch()==False.

        In other words abandon processing the event.

        """
        if not self.obey_context_switch():
            return 'break'

    def unbind_panel_button(self):
        """Unbind key and button events from button actions."""
        self.button.bind(
            sequence=''.join((
                '<ButtonPress-1>')),
            func='')
        self.button.bind(
            sequence='<KeyPress-Return>',
            func='')

        conf = self.button.configure()
        underline = conf['underline'][-1]
        text = conf['text'][-1]
        if isinstance(text, tuple):
            text = ' '.join(text)
        
        try:
            if not underline < 0:
                self.parent.get_widget().bind(
                    sequence=''.join((
                        '<Alt-KeyPress-',
                        text[underline].lower(),
                        '>')),
                    func='')
        except:
            print('AppSysPanelButton unbind exception')
            pass


class AppSysPanel(ExceptionHandler):
    
    """This is the base class for pages in a notebook style user interface.

    It provides the main frame of a page.  A frame for buttons that invoke
    actions is packed at bottom of page.  The rest of the page is filled by
    widgets providing application features.
    
    """

    def __init__(self, parent, cnf=dict(), **kargs):
        """Define basic structure of a page of a notebook style application.

        parent - AppSysFrame instance that owns this AppSysPanel instance
        cnf - passed to main tkinter.Frame() call as cnf argument
        **kargs - passed to main tkinter.Frame() call as **kargs argument

        Subclasses define the content of the page and the action buttons.

        """
        self.panel = tkinter.Frame(
            master=parent.get_widget(), cnf=cnf, **kargs)
        self.buttons_frame = tkinter.Frame(master=self.panel)
        self._give_focus_widget = None
        self.buttons_frame.pack(side=tkinter.BOTTOM, fill=tkinter.X)

        self.appsys = parent

        self.button_definitions = {}
        self.button_order = []
        self.buttons = {}
        self.describe_buttons()
        super(AppSysPanel, self).__init__()

    def close(self):
        """Raise AppSysPanelError('close not implemented') error.

        Subclasses must override this method.

        """
        raise AppSysPanelError('close not implemented')

    def create_buttons(self):
        """Create the action buttons defined for the page."""
        buttonrow = self.buttons_frame.pack_info()['side'] in ('top', 'bottom')
        definitions = self.button_definitions
        for w in self.buttons_frame.grid_slaves():
            w.grid_forget()
        for i, b in enumerate(self.button_order):
            if b not in self.buttons:
                self.buttons[b] = AppSysPanelButton(
                    self,
                    b,
                    definitions[b][2],
                    text=definitions[b][0],
                    underline=definitions[b][3],
                    command=self.try_command(
                        definitions[b][4], self.buttons_frame))
            self.buttons[b].raise_action_button()
            self.buttons[b].bind_panel_button()
            if buttonrow:
                self.buttons_frame.grid_columnconfigure(i*2, weight=1)
                self.buttons[b].button.grid_configure(column=i*2 + 1, row=0)
            else:
                self.buttons_frame.grid_rowconfigure(i*2, weight=1)
                self.buttons[b].button.grid_configure(row=i*2 + 1, column=0)
        if buttonrow:
            self.buttons_frame.grid_columnconfigure(
                len(self.button_order*2), weight=1)
        else:
            self.buttons_frame.grid_rowconfigure(
                len(self.button_order*2), weight=1)

    def define_button(
        self,
        identity,
        text='',
        tooltip='',
        switchpanel=False,
        underline=-1,
        command=None,
        position=-1):
        """Define an action button for the page.

        identity - unique identification number for button
        text - text displayed on button
        tooltip - tooltip text for button (not used at present)
        switchpanel - if True button is allowed to change page in notebook
        underline - position in text for use in Alt-<character> invokation
                    <0 means no Alt binding
        command - function implementing button action.
        position - button position in tab order relative to other buttons
                    <0 means add at end of list

        """
        self.button_definitions[identity] = (
            text, tooltip, switchpanel, underline, command)
        if identity in self.button_order:
            del self.button_order[self.button_order.index(identity)]
        if position < 0:
            self.button_order.append(identity)
        else:
            self.button_order.insert(position, identity)

    def describe_buttons(self):
        """Do nothing.  Subclasses should extend this method.

        Subclasses should extend this method to do a sequence of
        self.define_button(...) calls.
        AppSysPanel.__init__ calls self.describe_buttons()

        """

    def explicit_focus_bindings(self):
        """Do nothing.  Subclasses should extend this method.

        Subclasses should extend this method to set up event bindings for
        the page.
        AppSysPanel.show_panel calls self.explicit_focus_bindings()

        """

    def get_appsys(self):
        """Return application object."""
        return self.appsys

    def get_buttons_frame(self):
        """Return frame containing action buttons."""
        return self.buttons_frame

    def get_context(self):
        """Return None.  Context replaced by location in navigation map."""
        return

    def get_widget(self):
        """Return Tkinter.Frame containing all widgets for page."""
        return self.panel

    def give_focus(self, widget=None):
        """Set widget to be given focus when page is displayed."""
        self._give_focus_widget = widget

    def hide_panel(self):
        """Remove page from display."""
        self.panel.pack_forget()

    def hide_panel_buttons(self):
        """Remove event bindings for action buttons."""
        for b in self.buttons:
            self.buttons[b].unbind_panel_button()
        del self.button_order[:]

    def inhibit_context_switch(self, button):
        """Prevent next attempt to change context for button succeeding."""
        self.buttons[button].inhibit_context_switch()

    def make_explicit_focus_bindings(self, bindings):
        """Define bindings to change focus to grid from buttons."""

        def focus_bindings():
            for sequence, function in bindings.items():
                self.get_widget().bind_class(
                    self.get_appsys().explicit_focus_tag,
                    sequence=sequence,
                    func=function,
                    add=None)
                
        self.explicit_focus_bindings = focus_bindings

    def refresh_controls(self, widgets=None):
        """Notify all widgets registered for update notification.
        
        widgets = [DataClient instance | (db, file, index), ...]

        When widget is a DataClient the current DataSource is used if there
        is not an entry in DataRegister naming a callback.
        Naming the source by (db, file, index) causes refresh to happen
        only if the DataClient is registered.
        Calling DataSource.refresh_widgets refreshes all DataClients with
        that DataSource.

        DataClient, DataRegister, and DataSource, are classes defined in
        the solentware_grid package.

        """
        if widgets is None:
            return

        dr = self.get_appsys().get_data_register()
        ds = set()
        db = set()
        for w in widgets:
            if not isinstance(w, tuple):
                if not len(dr.datasources):
                    ds.add(w.datasource)
                else:
                    db.add((
                        w.datasource.dbhome,
                        w.datasource.dbset,
                        w.datasource.dbname))
            elif len(dr.datasources):
                db.add(w)
        for d in ds:
            d.refresh_widgets(None)
        for d in db:
            dr.refresh_after_update(d, None)

    def show_panel(self):
        """Pack page and button frames and define event bindings."""
        self.explicit_focus_bindings()
        self.panel.pack(fill=tkinter.BOTH, expand=True)
        if self._give_focus_widget is None:
            self.panel.focus_set()
        else:
            self._give_focus_widget.focus_set()

    def show_panel_buttons(self, buttons):
        """Ensure all action buttons for page are visible."""
        for b in buttons:
            if b in self.button_definitions:
                if b not in self.button_order:
                    self.button_order.append(b)

    def switch_context(self, button):
        """Call the application switch_context method."""
        # Could build this call directly into the switch_context function
        # built in AppSysButton. The parent argument to AppSysButton is
        # an AppSysPanel instance whose appsys attribute is the AppSysFrame
        # containing the context switch data structures.
        # But a hook at this point could be useful.
        self.appsys.switch_context(button)

    def __del__(self):
        """Call the close() method."""
        self.close()


class PlainPanel(AppSysPanel):
    
    """This is the base class for pages in a notebook style user interface
    which do not support *grid* classes in the solentware_grid package.
    
    """

    def make_grids(self, gridarguments):
        """Raise exception because solentware_grid *grid* classes are not
        supported.

        Subclasses can use classes from solentware_grid, but must be responsible
        for managing them.
        """
        raise AppSysPanelError('solentware_grid *grid* classes not supported')


class PanelWithGrids(AppSysPanel):
    
    """This is the base class for pages in a notebook style user interface
    which support the *grid* classes in the solentware_grid package.
    
    One or more grids may be put on the panel, with a record selector for
    each grid if the useselector argument is True.

    The record selector is a tkinter.Entry widget whose content is used to
    control the records shown in the grid.  Multiple selectors are put in
    a row at the top of the panel.

    Subclasses of PanelWithGrids may arrange grids and selectors differently.
    """

    def __init__(
        self,
        parent,
        useselector=True,
        gridhorizontal=True,
        cnf=dict(),
        **kargs):
        """Create panel to which grids and selectors may be added.

        parent - passed to superclass as parent argument.
        useselector - if True a selector is provided for each grid.
        gridhorizontal - if True grids are arranged horizontally.
        cnf - passed to superclass as cnf argument.
        **kargs - passed to superclass as **kargs argument.

        Selectors are either present for all grids or absent for all grids.

        Grids are arranged horizontally or vertically.
        
        """
        super(PanelWithGrids, self).__init__(
            parent=parent, cnf=cnf, **kargs)
        self.useselector = useselector is True
        self.gridhorizontal = gridhorizontal is True
        self.gridselector = dict()
        self.activegridhint = dict()

    def add_grid_to_panel(
        self,
        gridmaster,
        selector,
        grid=None,
        selectlabel=None,
        gridfocuskey=None,
        selectfocuskey=None,
        keypress_grid_to_select=True,
        **kargs
        ):
        """Add selector and grid to panel.

        gridmaster - to be passed as master argument in grid() call.
        selector - the grid's selector instance (a tkinter.Entry widget).
        grid - class or function to create the grid.
        selectlabel - the text displayed as the selector's name.
        gridfocuskey - sequence to give keyboard focus to grid.
        selectfocuskey - sequence to give keyboard focus to grid's selector.
        keypress_grid_to_select - if True pressing a key while grid has
                                keyboard focus switches keyboard focus to
                                grid's selector.
        **kargs - not used.

        The gridfocuskey and selectfocuskey sequences switch the keyboard
        focus to the grid and selector respectively from any widget in
        the panel.

        The gridmaster argument is usually self.frame.
        """
        gridframe = grid(
            gridmaster,
            selecthintlabel=selectlabel,
            appsyspanel=self,
            receivefocuskey=gridfocuskey,
            focus_selector=selectfocuskey,
            keypress_grid_to_select=keypress_grid_to_select)
        if selector:
            (self.activegridhint[gridframe],
             self.gridselector[gridframe],
             ) = selector
            gridframe.set_select_hint_label()
        return gridframe

    def clear_selector(self, grid):
        """Clear the record selector tkentry.Entry widget for grid.

        grid - a solentware_grid.DataGrid instance.
        """
        if grid is True:
            for w in set(self.gridselector.values()):
                w.delete(0, tkinter.END)
        else:
            w = self.gridselector.get(grid)
            if w is not None:
                w.delete(0, tkinter.END)

    def get_active_grid_hint(self, grid):
        """Return Tkinter.Label for grid.

        grid - a solentware_grid.DataGrid instance.
        """
        return self.activegridhint.get(grid)

    def get_grid_selector(self, grid):
        """Return Tkinter.Entry containing selection text for grid.

        grid - a solentware_grid.DataGrid instance.
        """
        return self.gridselector.get(grid)

    def set_panels_grid_bindings(self, grids, gridarguments):
        """Set grid navigation bindings for grids on page."""
        # Each grid sets bindings to switch focus to all the other grids
        gridargs = list(gridarguments)
        for g in range(len(grids)):
            w = grids.pop(0)
            ga = gridargs.pop(0)
            w.grid_bindings(grids, gridargs, **ga)
            grids.append(w)
            gridargs.append(ga)
        ba = {}
        for ga, g in zip(gridarguments, grids):
            ba[ga['gridfocuskey']] = g.focus_to_grid
        self.make_explicit_focus_bindings(ba)


class PanelGridSelector(PanelWithGrids):
    
    """Display data grids in equal share of space next to their selectors.
    
    """

    def __init__(self, parent, **kargs):
        """Delegate to superclass then create Tkinter.Frame to which grids
        and selectors may be added.

        parent - passed to superclass as parent argument.
        **kargs - passed to superclass as **kargs argument.

        The extra widget in the hierarchy adjusts the behaviour of the
        widgets when the application is resized.
        """
        super(PanelGridSelector, self).__init__(parent, **kargs)

        self.gridpane = tkinter.Frame(master=self.get_widget())
        self.gridpane.pack(
            side=tkinter.TOP, expand=tkinter.TRUE, fill=tkinter.BOTH)

    def make_grids(self, gridarguments):
        """Create data grids and selectors controlled by grid geometry manager.

        gridarguments is a list of dictionaries of arguments for method
        add_grid_to_panel.

        The creation order of widgets is chosen to cause a selector widget
        to disappear after the associated data grid, which is adjacent above
        or below, and to cause widgets lower in the application window to
        disappear before higher ones; except panel buttons are the last of
        the panel widgets to go when the application is resized smaller.

        Selector widgets are fixed size and data grid widgets grow and
        shrink equally to fill the remaining space in the application
        window.

        """
        def make_selector(a):
            if a.get('selectfocuskey') is None:
                return (None, None)
            s = tkinter.Frame(master=self.gridpane)
            sl = tkinter.Label(master=s)
            se = tkinter.Entry(master=s)
            return (s, (sl, se))

        grids = []
        for e, ga in enumerate(gridarguments):
            selector, selector_widgets = make_selector(ga)
            grids.append(
                self.add_grid_to_panel(
                    self.gridpane,
                    selector_widgets,
                    **ga))
            gf = grids[-1]
            if selector:
                selector.grid_columnconfigure(0, weight=1)
                self.activegridhint[gf].grid(column=0, row=0, sticky='nes')
                selector.grid_columnconfigure(1, weight=1)
                self.gridselector[gf].grid(column=1, row=0, sticky='nsw')
                if self.gridhorizontal:
                    if self.useselector:
                        selector.grid(column=e, row=0, sticky='nesw')
                    else:
                        selector.grid(column=e, row=1, sticky='nesw')
                elif self.useselector:
                    self.gridpane.grid_rowconfigure(
                        e * 2, weight=0, uniform='select')
                    selector.grid(column=0, row=e * 2, sticky='nesw')
                else:
                    self.gridpane.grid_rowconfigure(
                        e * 2 + 1, weight=0, uniform='select')
                    selector.grid(column=0, row=e * 2 + 1, sticky='nesw')
            if self.gridhorizontal:
                self.gridpane.grid_columnconfigure(e, weight=1, uniform='data')
                if self.useselector:
                    gf.get_frame().grid(column=e, row=1, sticky='nesw')
                else:
                    gf.get_frame().grid(column=e, row=0, sticky='nesw')
            elif self.useselector:
                self.gridpane.grid_rowconfigure(
                    e * 2 + 1, weight=1, uniform='data')
                gf.get_frame().grid(column=0, row=e * 2 + 1, sticky='nesw')
            else:
                self.gridpane.grid_rowconfigure(
                    e * 2, weight=1, uniform='data')
                gf.get_frame().grid(column=0, row=e * 2, sticky='nesw')
        if self.gridhorizontal:
            self.gridpane.grid_rowconfigure(1, weight=1)
        else:
            self.gridpane.grid_columnconfigure(0, weight=1)
                
        self.set_panels_grid_bindings(grids, gridarguments)
        if len(grids):
            self.give_focus(grids[0].get_frame())
        return grids


class PanelGridSelectorBar(PanelWithGrids):
    
    """Display data grids in equal share of space with selectors in own row.
    
    """

    def __init__(self, parent, **kargs):
        """Delegate to superclass then create Tkinter.Frame to which grids
        and selectors may be added.

        parent - passed to superclass as parent argument.
        **kargs - passed to superclass as **kargs argument.

        The extra widget in the hierarchy adjusts the behaviour of the
        widgets when the application is resized.
        """
        super(PanelGridSelectorBar, self).__init__(parent, **kargs)

        self.gridpane = tkinter.Frame(master=self.get_widget())
        self.gridpane.pack(
            side=tkinter.TOP, expand=tkinter.TRUE, fill=tkinter.BOTH)

    def make_grids(self, gridarguments):
        """Create data grids and selectors controlled by grid geometry manager.

        gridarguments is a list of dictionaries of arguments for method
        add_grid_to_panel.

        Selector widgets are in a row above or below all data grid widgets.

        The creation order of widgets is chosen to cause the row of selector
        widgets to disappear after all the data grids and to cause widgets
        lower in the application window to disappear before higher ones;
        except panel buttons are the last of the panel widgets to go when
        the application is resized smaller.

        Selector widgets are fixed size and data grid widgets grow and
        shrink equally to fill the remaining space in the application
        window.

        """
        def make_selector(a):
            if a.get('selectfocuskey') is None:
                return (None, None)
            s = tkinter.Frame(master=self.gridpane)
            sl = tkinter.Label(master=s)
            se = tkinter.Entry(master=s)
            return (s, (sl, se))

        gsize = len(gridarguments)
        grids = []
        for e, ga in enumerate(gridarguments):
            selector, selector_widgets = make_selector(ga)
            grids.append(
                self.add_grid_to_panel(
                    self.gridpane,
                    selector_widgets,
                    **ga))
            gf = grids[-1]
            if selector:
                selector.grid_columnconfigure(0, weight=1)
                self.activegridhint[gf].grid(column=0, row=0, sticky='nes')
                selector.grid_columnconfigure(1, weight=1)
                self.gridselector[gf].grid(column=1, row=0, sticky='nsw')
                if self.useselector:
                    selector.grid(column=e, row=0, sticky='nesw')
                else:
                    selector.grid(column=e, row=gsize, sticky='nesw')
                if not self.gridhorizontal:
                    self.gridpane.grid_columnconfigure(
                        e, weight=1, uniform='select')
            if self.gridhorizontal:
                self.gridpane.grid_columnconfigure(e, weight=1, uniform='data')
                if self.useselector:
                    gf.get_frame().grid(column=e, row=1, sticky='nesw')
                else:
                    gf.get_frame().grid(column=e, row=0, sticky='nesw')
            else:
                if self.useselector:
                    r = e + 1
                else:
                    r = e
                gf.get_frame().grid(
                    column=0, row=r, sticky='nesw', columnspan=gsize)
                self.gridpane.grid_rowconfigure(r, weight=1, uniform='data')
        if self.gridhorizontal:
            if self.useselector:
                self.gridpane.grid_rowconfigure(1, weight=1)
            else:
                self.gridpane.grid_rowconfigure(0, weight=1)
                
        self.set_panels_grid_bindings(grids, gridarguments)
        if len(grids):
            self.give_focus(grids[0].get_frame())
        return grids


class PanelGridSelectorShared(PanelWithGrids):
    
    """Display data grids in equal share of space with a shared selector.
    
    """

    def __init__(self, parent, **kargs):
        """Delegate to superclass then create Tkinter.Frame to which grids
        and selectors may be added.

        parent - passed to superclass as parent argument.
        **kargs - passed to superclass as **kargs argument.

        The extra widget in the hierarchy adjusts the behaviour of the
        widgets when the application is resized.
        """
        super(PanelGridSelectorShared, self).__init__(parent, **kargs)

        self.gridpane = tkinter.Frame(master=self.get_widget())
        self.gridpane.pack(
            side=tkinter.TOP, expand=tkinter.TRUE, fill=tkinter.BOTH)

    def make_grids(self, gridarguments):
        """Create data grids and selectors controlled by grid geometry manager.

        gridarguments is a list of dictionaries of arguments for method
        add_grid_to_panel.

        The selector widget is shared by the data grid widgets and is on a
        row above or below all the data grids.

        The creation order of widgets is chosen to cause the row with the
        selector widget to disappear after all the data grids and to cause
        widgets lower in the application window to disappear before higher
        ones; except panel buttons are the last of the panel widgets to go
        when the application is resized smaller.

        Selector widgets are fixed size and data grid widgets grow and
        shrink equally to fill the remaining space in the application
        window.

        """
        for ga in gridarguments:
            if ga.get('selectfocuskey'):
                def csf():
                    s = tkinter.Frame(master=self.gridpane)
                    sl = tkinter.Label(master=s)
                    se = tkinter.Entry(master=s)
                    def rcsf():
                        return (s, (sl, se))
                    return rcsf
                make_selector = csf()
                break
        else:
            def make_selector():
                return (None, None)
        selector, selector_widgets = make_selector()
        gsize = len(gridarguments)
        grids = []
        for e, ga in enumerate(gridarguments):
            grids.append(
                self.add_grid_to_panel(
                    self.gridpane,
                    selector_widgets,
                    **ga))
            gf = grids[-1]
            if self.gridhorizontal:
                self.gridpane.grid_columnconfigure(e, weight=1, uniform='data')
                if self.useselector:
                    gf.get_frame().grid(column=e, row=1, sticky='nesw')
                else:
                    gf.get_frame().grid(column=e, row=0, sticky='nesw')
            else:
                if self.useselector:
                    r = e + 1
                else:
                    r = e
                gf.get_frame().grid(
                    column=0, row=r, sticky='nesw', columnspan=gsize)
                self.gridpane.grid_rowconfigure(r, weight=1, uniform='data')
        if selector:
            selector.grid_columnconfigure(0, weight=1)
            selector_widgets[0].grid(column=0, row=0, sticky='nes')
            selector.grid_columnconfigure(1, weight=1)
            selector_widgets[1].grid(column=1, row=0, sticky='nsw')
            if self.useselector:
                if self.gridhorizontal:
                    selector.grid(
                        column=0, row=0, sticky='nesw', columnspan=gsize)
                else:
                    selector.grid(column=0, row=0, sticky='nesw')
            elif self.gridhorizontal:
                selector.grid(
                    column=0, row=gsize, sticky='nesw', columnspan=gsize)
            else:
                selector.grid(column=0, row=gsize, sticky='nesw')
        if self.gridhorizontal:
            if self.useselector:
                self.gridpane.grid_rowconfigure(1, weight=1)
            else:
                self.gridpane.grid_rowconfigure(0, weight=1)
        else:
            self.gridpane.grid_columnconfigure(0, weight=1)
                
        self.set_panels_grid_bindings(grids, gridarguments)
        if len(grids):
            self.give_focus(grids[0].get_frame())
            if selector:
                grids[0].bind_return(setbinding=True)
        return grids


class PanedPanelGridSelector(PanelWithGrids):
    
    """Display data grids in adjustable space next to their selectors.
    
    """

    def __init__(self, parent, **kargs):
        """Delegate to superclass then create Tkinter.PanedWindow to which
        grids and selectors may be added.

        parent - passed to superclass as parent argument.
        **kargs - passed to superclass as **kargs argument.

        The extra widget in the hierarchy adjusts the behaviour of the
        widgets when the application is resized.
        """
        super(PanedPanelGridSelector, self).__init__(parent, **kargs)

        if self.gridhorizontal:
            orient = tkinter.HORIZONTAL
        else:
            orient = tkinter.VERTICAL
        self.gridpane = tkinter.PanedWindow(
            master=self.get_widget(),
            opaqueresize=tkinter.FALSE,
            orient=orient)
        self.gridpane.pack(
            side=tkinter.TOP, expand=True, fill=tkinter.BOTH)

    def make_grids(self, gridarguments):
        """Create data grids and selectors controlled by paned window.

        gridarguments is a list of dictionaries of arguments for method
        add_grid_to_panel.

        The creation order of widgets is chosen to cause a selector widget
        to disappear after the associated data grid, which is adjacent above
        or below, and to cause widgets lower in the application window to
        disappear before higher ones; except panel buttons are the last of
        the panel widgets to go when the application is resized smaller.

        Selector widgets are fixed size.  Data grid widgets are created with
        equal size each in a pane with the associated selector.  Extra space
        is added to the rightmost or bottommost pane and shrinking removes
        space in reverse order to add.  Panes can be resized by dragging the
        sash between two panes.

        """
        def make_selector(a, sm):
            if a.get('selectfocuskey') is None:
                return (None, None)
            s = tkinter.Frame(master=sm)
            sl = tkinter.Label(master=s)
            se = tkinter.Entry(master=s)
            s.grid_columnconfigure(0, weight=1)
            sl.grid(column=0, row=0, sticky='nes')
            s.grid_columnconfigure(1, weight=1)
            se.grid(column=1, row=0, sticky='nsw')
            return (s, (sl, se))

        grids = []
        for e, ga in enumerate(gridarguments):
            gridmaster = tkinter.Frame(master=self.gridpane)
            selector, selector_widgets = make_selector(ga, gridmaster)
            grids.append(
                self.add_grid_to_panel(
                    gridmaster,
                    selector_widgets,
                    **ga))
            gf = grids[-1]
            if self.useselector:
                if selector:
                    selector.pack(side=tkinter.TOP, fill=tkinter.X)
                    gf.bind_return(setbinding=True)
                gf.get_frame().pack(
                    side=tkinter.TOP, fill=tkinter.BOTH, expand=tkinter.TRUE)
            else:
                gf.get_frame().pack(
                    side=tkinter.TOP, fill=tkinter.BOTH, expand=tkinter.TRUE)
                if selector:
                    selector.pack(side=tkinter.TOP, fill=tkinter.X)
                    gf.bind_return(setbinding=True)
            self.gridpane.add(gridmaster)
                
        self.set_panels_grid_bindings(grids, gridarguments)
        if len(grids):
            self.give_focus(grids[0].get_frame())
        return grids


class PanedPanelGridSelectorBar(PanelWithGrids):
    
    """Display data grids in adjustable space with selectors in own row.
    
    """

    def __init__(self, parent, **kargs):
        """Delegate to superclass then create Tkinter.PanedWindow to which
        grids and selectors may be added.

        parent - passed to superclass as parent argument.
        **kargs - passed to superclass as **kargs argument.

        The extra widget in the hierarchy adjusts the behaviour of the
        widgets when the application is resized.
        """
        super(PanedPanelGridSelectorBar, self).__init__(parent, **kargs)

        if self.gridhorizontal:
            orient = tkinter.HORIZONTAL
        else:
            orient = tkinter.VERTICAL
        self.gridpane = tkinter.PanedWindow(
            master=self.get_widget(),
            opaqueresize=tkinter.FALSE,
            orient=orient)
        self.selectormaster = tkinter.Frame(master=self.get_widget())
        if self.useselector:
            self.selectormaster.pack(
                side=tkinter.TOP, fill=tkinter.X)
            self.gridpane.pack(
                side=tkinter.BOTTOM, expand=tkinter.TRUE, fill=tkinter.BOTH)
        else:
            self.selectormaster.pack(
                side=tkinter.BOTTOM, fill=tkinter.X)
            self.gridpane.pack(
                side=tkinter.TOP, expand=tkinter.TRUE, fill=tkinter.BOTH)

    def make_grids(self, gridarguments):
        """Create data grids and selectors controlled by paned window.

        gridarguments is a list of dictionaries of arguments for method
        add_grid_to_panel.

        Selector widgets are in a row above or below all the data grid
        widgets not controlled by panes.

        The creation order of widgets is chosen to cause the row of selector
        widgets to disappear after all the data grids.  The panel buttons
        are the last of the panel widgets to go when the application is
        resized smaller.

        Selector widgets are fixed size.  Data grid widgets are created with
        equal size each in a separate pane.  Extra space is added to the
        rightmost or bottommost pane and shrinking removes space in reverse
        order to add.  Panes can be resized by dragging the sash between two
        panes.

        """
        def make_selector(a, col):
            if a.get('selectfocuskey') is None:
                return (None, None)
            sl = tkinter.Label(master=self.selectormaster)
            se = tkinter.Entry(master=self.selectormaster)
            self.selectormaster.grid_columnconfigure(col * 2, weight=1)
            sl.grid(column=col * 2, row=0, sticky='nes')
            self.selectormaster.grid_columnconfigure(
                col * 2 + 1, weight=1)
            se.grid(column=col * 2 + 1, row=0, sticky='nsw')
            return (self.selectormaster, (sl, se))

        selector = False
        grids = []
        for e, ga in enumerate(gridarguments):
            selector, selector_widgets = make_selector(ga, e)
            grids.append(
                self.add_grid_to_panel(
                    self.gridpane,
                    selector_widgets,
                    **ga))
            gf = grids[-1]
            self.gridpane.add(gf.get_frame())
        if not selector:
            self.selectormaster.pack_forget()
                
        self.set_panels_grid_bindings(grids, gridarguments)
        if len(grids):
            self.give_focus(grids[0].get_frame())
            if selector:
                grids[0].bind_return(setbinding=True)
        return grids


class PanedPanelGridSelectorShared(PanelWithGrids):
    
    """Display data grids in adjustable space with a shared selector.
    
    """

    def __init__(self, parent, **kargs):
        """Delegate to superclass then create Tkinter.PanedWindow to which
        grids and selectors may be added.

        parent - passed to superclass as parent argument.
        **kargs - passed to superclass as **kargs argument.

        The extra widget in the hierarchy adjusts the behaviour of the
        widgets when the application is resized.
        """
        super(PanedPanelGridSelectorShared, self).__init__(parent, **kargs)

        if self.gridhorizontal:
            orient = tkinter.HORIZONTAL
        else:
            orient = tkinter.VERTICAL
        self.gridpane = tkinter.PanedWindow(
            master=self.get_widget(),
            opaqueresize=tkinter.FALSE,
            orient=orient)
        self.selectormaster = tkinter.Frame(master=self.get_widget())
        if self.useselector:
            self.selectormaster.pack(
                side=tkinter.TOP, fill=tkinter.X)
            self.gridpane.pack(
                side=tkinter.BOTTOM, expand=tkinter.TRUE, fill=tkinter.BOTH)
        else:
            self.selectormaster.pack(
                side=tkinter.BOTTOM, fill=tkinter.X)
            self.gridpane.pack(
                side=tkinter.TOP, expand=tkinter.TRUE, fill=tkinter.BOTH)

    def make_grids(self, gridarguments):
        """Create data grids and selectors controlled by paned window.

        gridarguments is a list of dictionaries of arguments for method
        add_grid_to_panel.

        The selector widget is shared by the data grid widgets and is on a
        row above or below all the data grids.

        The creation order of widgets is chosen to cause the row with the
        selector widget to disappear after all the data grids.  The panel
        buttons are the last of the panel widgets to go when the application
        is resized smaller.

        The selector widget is fixed size and data grid widgets are created
        with equal size each in a separate pane.  Extra space is added to
        the rightmost or bottommost pane and shrinking removes space in
        reverse order to add.  Panes can be resized by dragging the sash
        between two panes.

        """
        for ga in gridarguments:
            if ga.get('selectfocuskey'):
                def csf():
                    sl = tkinter.Label(master=self.selectormaster)
                    se = tkinter.Entry(master=self.selectormaster)
                    self.selectormaster.grid_columnconfigure(0, weight=1)
                    sl.grid(column=0, row=0, sticky='nes')
                    self.selectormaster.grid_columnconfigure(1, weight=1)
                    se.grid(column=1, row=0, sticky='nsw')
                    def rcsf():
                        return (self.selectormaster, (sl, se))
                    return rcsf
                make_selector = csf()
                break
        else:
            def make_selector():
                return (None, None)
        selector, selector_widgets = make_selector()
        grids = []
        for ga in gridarguments:
            grids.append(
                self.add_grid_to_panel(
                    self.gridpane,
                    selector_widgets,
                    **ga))
            gf = grids[-1]
            self.gridpane.add(gf.get_frame())
        if not selector:
            self.selectormaster.pack_forget()
                
        self.set_panels_grid_bindings(grids, gridarguments)
        if len(grids):
            self.give_focus(grids[0].get_frame())
            if selector:
                grids[0].bind_return(setbinding=True)
        return grids
