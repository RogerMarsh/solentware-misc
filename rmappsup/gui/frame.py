# frame.py
# Copyright 2007 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""A notebook style database User Interface class

List of classes:

AppSysFrameButton
AppSysFrame
AppSysTab
AppSysTabDefinition

"""

import Tkinter

import gridsup.core.dataregister


class AppSysFrameButton(object):
    
    """Tab selection buttons for AppSysFrame.

    Methods added:

    bind_frame_button - Bind specified command to Alt-key on tab
    make_command - Bind specified command to button click
    unbind_frame_button - Unbind specified command from Alt-key on tab
    
    Methods overridden:

    __init__

    Methods extended:

    None
    
    """
    
    def __init__(self, parent, cnf=dict(), **kargs):
        """Create tab selection button

        **kargs:
        command - the method to be bound to the button
        Others are assumed to be Tkinter.Button options and passed on

        """
        self.button = Tkinter.Button(
            master=parent.get_tab_buttons_frame(),
            cnf=cnf,
            **kargs)

        self.command = kargs.get('command')

        tags = list(self.button.bindtags())
        tags.insert(0, parent.explicit_focus_tag)
        self.button.bindtags(tuple(tags))

    def bind_frame_button(self, tab):
        """Bind button command to tab in Alt-key style."""
        conf = self.button.configure()
        underline = conf['underline'][-1]
        text = conf['text'][-1]
        if isinstance(text, tuple):
            text = ' '.join(text)
        try:
            if not underline < 0:
                tab.panel.bind(
                    sequence=''.join((
                        '<Alt-KeyPress-',
                        text[underline].lower(),
                        '>')),
                    func=self.command,
                    add=True)
        except:
            pass

    def make_command(self, command, tab):
        """Bind command(tab) to button for KeyPress-Return and mouse click"""

        def on_click(event=None):
            command(tab)

        self.command = on_click
        self.button.configure(command=on_click)
        self.button.bind(
            sequence='<KeyPress-Return>',
            func=on_click,
            add=True)

    def unbind_frame_button(self, tab):
        """Unbind button command from tab in Alt-key style."""
        conf = self.button.configure()
        underline = conf['underline'][-1]
        text = conf['text'][-1]
        if isinstance(text, tuple):
            text = ' '.join(text)
        try:
            if not underline < 0:
                tab.panel.bind(
                    sequence=''.join((
                        '<Alt-KeyPress-',
                        text[underline].lower(),
                        '>')))
        except:
            pass


class AppSysFrame(object):
    
    """Base class for database User Interface.

    The main frame of an application. Contains a frame for buttons that
    switch between the detail frames (panels) of application and a frame
    that contains the selected panel.

    Methods added:

    create_tabs
    get_data_register
    define_state_transitions
    define_tab
    get_tab_buttons_frame
    get_state
    get_current_tab
    get_tab_data
    get_widget
    set_state
    set_current_tab
    show_current_tab
    show_state
    switch_context
    _hide_buttons
    _hide_tab
    _make_tab
    _show_buttons
    _show_tab
    
    Methods overridden:

    __init__

    Methods extended:

    None
    
    Notes

    The _tab_state _switch_state _switch_tab attributes are used to control
    navigation in the application.

    _tab_state defines the application states and for each state identifies
    the tabs that are available for display.

    _switch_state identifies the state that becomes current for each action
    in every state.  The absence of a <state, action> item in this map means
    the current state remains current.  The tab to be shown on switching to
    the new state is identified in <state, action>: <newstate, show> as show.
    If no tabs are associated with newstate show must be None otherwise show
    must be one of the tabs in the _tab_state entry for show.

    _switch_tab appears to be redundant but has not been removed yet.

    Tabs are defined but not created by the CreateTab method.  A tab is created
    if it does not exist when the associated tab button is invoked.  A set of
    actions that cause the tab to be created may be identified in define_tab.
    A set of actions that cause the tab to be destroyed may be given in
    define_tab.  (This will likely change to <state, action>.)

    A tab, and the tab buttons for the associated state, are not displayed if
    creation of the tab is a consequence of an action that does not alter the
    current state.

    """

    explicit_focus_tag = 'explicitfocus'

    def __init__(self, master=None, cnf=dict(), **kargs):
        """Define the basic structure of the notebook-like application

        Subclasses define the tabs and their interactions

        The following arguments are passed on to Tkinter.Frame
        cnf = Tkinter.Frame configuration
        **kargs = Tkinter.Frame arguments.
        
        """
        self._frame = Tkinter.Frame(
            master=master,
            cnf=cnf,
            **kargs)

        self._tab_description = dict()
        self._tab_order = []
        self._tab_state = dict()
        self._switch_tab = dict()
        self._switch_state = dict()
        self._tabs = dict()
        self._state = None
        self._current_tab = None
        self._datasources = gridsup.core.dataregister.DataRegister(
            **kargs)

        # create frames for tab switching buttons and tab but leave mapping
        # to screen until a tab is actually created
        self._tab_button_frame = Tkinter.Frame(master=self._frame)
        # _TAB_FRAME
        #self._tab_frame = Tkinter.Frame(master=self._frame)

    def create_tabs(self):
        """Create tab buttons and attach tab switching commands.

        Tab buttons are along top side of frame and switch the tab (notebook
        page) that is displayed.  If the tab does not exist when the button
        is clicked, it is created.  This method does not create the tab.

        """
        for p, l, t in sorted(self._tab_order):
            if t not in self._tabs:
                self._tabs[t] = AppSysTab(self, self._tab_description[t])
                self._tabs[t].bind_tab_button(self.show_current_tab)

    def get_data_register(self):
        """Return the data register object.

        Tabs should use this interface to register their widgets for update
        notification.

        """
        return self._datasources
    
    def define_state_transitions(
        self,
        tab_state=None,
        switch_tab=None,
        switch_state=None):
        """Define tab navigation for application.

        Subclasses must extend this method to define the application's
        navigation between tabs.  Each tab, an AppSysPanel instance, has a
        set of buttons along its bottom edge which can be used to do actions,
        switch to another tab, or both.

        tab_state - dictionary containning application states as the panels to
        be available for display and the panel switching buttons displayed.
        
        switch_tab - dictionary containing rule for defining context of panel
        being switched to as a new context. None means current panel is
        context. Otherwise take context from tab_description if possible with
        current panel as default.

        switch_state - dictionary containing state changes for application
        consisting of
        {..., (<current state>,<panel button>):[<new state>,<new panel>], ...}.
        <current state> and <new state> values must be keys in tab_state.
        
        """
        if isinstance(tab_state, dict):
            self._tab_state.update(tab_state)
        if isinstance(switch_tab, dict):
            self._switch_tab.update(switch_tab)
        if isinstance(switch_state, dict):
            self._switch_state.update(switch_state)
    
    def define_tab(
        self,
        identity,
        text='',
        tooltip='',
        underline=-1,
        tabclass=None,
        position=-1,
        create_actions=None,
        destroy_actions=None):
        """Create a tab description.

        see AppSysTab for description of remaining arguments.

        It is sensible to ensure that the order of buttons in _tab_order is
        the same as the order of buttons in _tab_state entries.
        
        """
        if identity in self._tab_description:
            for e in range(len(self._tab_order)):
                t = self._tab_order.pop(0)
                if t[-1] != identity:
                    self._tab_order.append(t)
        if position < 0:
            self._tab_order.append(
                (len(self._tab_order), len(self._tab_order), identity))
        else:
            self._tab_order.append(
                (position, len(self._tab_order), identity))
        self._tab_description[identity] = AppSysTabDefinition(
            identity,
            text=text,
            tooltip=tooltip,
            tabclass=tabclass,
            underline=underline,
            create_actions=create_actions,
            destroy_actions=destroy_actions)
    
    def get_tab_buttons_frame(self):
        """Return Frame containing tab buttons."""
        return self._tab_button_frame

    def get_state(self):
        """Return current location in tab navigation map."""
        return self._state

    def get_current_tab(self):
        """Return tab currently displayed."""
        return self._current_tab

    def get_tab_data(self, tab):
        """Return definition data for tab."""
        try:
            return self._tabs[tab].tab
        except:
            return None

    def get_widget(self):
        """Return the Frame containing application."""
        return self._frame

    def set_state(self, state):
        """Set location in tab navigation map to state."""
        self._state = state

    def set_current_tab(self, tab):
        """Set tab currently displayed to tab"""
        self._current_tab = tab

    def show_current_tab(self, tab):
        """Hide displayed tab then make tab current and display it.

        This method is the command for the AppSysFrame buttons but can be
        used separately.

        """
        self._hide_buttons()
        self._hide_tab()
        self._make_tab(tab)
        self.set_current_tab(tab)
        self._show_tab()
        self._show_buttons()

    def show_state(self, eid=None):
        """Change the displayed tab as directed by eid.

        This method is similar to show_current_tab but takes into account
        the current location in the navigation map and the event (usually
        a button click or equivalent) when choosing the new tab.

        Assumes that the AppSysPanel subclass defines a close method.

        """
        self._hide_buttons()
        state, tab = self._switch_state[(self._state, eid)]
        if state != None:
            self._hide_tab()
            for t in self._tabs.itervalues():
                # destroy tabs from AppSysTabDefinition.destroy_actions
                if eid in t.description.destroy_actions:
                    if t.tab is not None:
                        t.tab.close()
                        t.tab = None
                # create tabs from AppSysTabDefinition.create_actions
                if eid in t.description.create_actions:
                    self._make_tab(t.description.identity)
            self._make_tab(tab)
            self.set_state(state)
            # display the tab if it is one displayable in new state ??????
            if tab in self._tab_state[state]:
                self.set_current_tab(tab)
                self._show_tab()
            # forget frame containing tab switching buttons and tab if no tab
            # exists
            for t in self._tabs.itervalues():
                if t.tab is not None:
                    break
            else:
                if self._tab_button_frame.winfo_ismapped() == 1:
                    self._tab_button_frame.pack_forget()
                # _TAB_FRAME
                '''if self._tab_frame.winfo_ismapped() == 1:
                    self._tab_frame.pack_forget()'''
            self._show_buttons()
    
    def switch_context(self, button):
        """Provide switch_context interface to show_state for AppSysPanel.

        This allows AppSysPanel to call switch_context without worrying about
        whether it is calling an AppSysPanel or AppSysFrame method.  If it is
        calling the AppSysFrame method show_state does the work.
        
        """
        self.show_state(eid=button)

    def _hide_buttons(self):
        """Hide the frame buttons."""
        for p, l, b in self._tab_order:
            if self._current_tab:
                self._tabs[b].button.unbind_frame_button(
                    self._tabs[self._current_tab].tab)
            self._tabs[b].button.button.pack_forget()

    def _hide_tab(self):
        """Hide the current tab"""
        if self._state == None:
            return
        tab = self._current_tab
        if tab is None:
            return
        if self._tabs[tab].tab == None:
            return
        self._tabs[tab].tab.hide_panel()
        for s in self._frame.bind_class(self.explicit_focus_tag):
            self._frame.unbind_class(self.explicit_focus_tag, s)

    def _make_tab(self, tab):
        """Create tab if it does not exist."""
        if tab is None:
            return
        if self._tabs[tab].tab != None:
            return
        # Assume some tab will be displayed if a tab is created so ensure
        # that tab switching buttons are displayed.  Actually need this even
        # if no tab is displayed so tabs can be accessed anyway
        if self._tab_button_frame.winfo_ismapped() == 0:
            self._tab_button_frame.pack(fill=Tkinter.BOTH)
        self._tabs[tab].tab = self._tab_description[tab].tabclass(parent=self)

    def _show_buttons(self):
        """Show frame buttons for current location in navigation map."""
        for b in self._tab_state[self._state]:
            self._tabs[b].button.button.pack(side=Tkinter.LEFT)
            if self._current_tab:
                self._tabs[b].button.bind_frame_button(
                    self._tabs[self._current_tab].tab)

    def _show_tab(self):
        """Show current tab and give it the focus."""
        tab = self._current_tab
        if tab is None:
            return
        # pack frame containing tab switch buttons and tab if any tab exists
        for t in self._tabs.itervalues():
            if t.tab is not None:
                if t.description.identity in self._tab_state[self._state]:
                    # _TAB_FRAME
                    '''if self._tab_frame.winfo_ismapped() == 0:
                        self._tab_frame.pack(fill=Tkinter.BOTH)'''
                    break
        self._tabs[tab].tab.show_panel()
        self._tabs[tab].tab.panel.focus_set()
        

# maybe combine AppSysTab and AppSysTabDefinition classes
class AppSysTab(object):
    
    """Instantiated Tab details for active tabs on AppSysFrame.

    Methods added:

    bind_tab_button
    
    Methods overridden:

    __init__

    Methods extended:

    None
    
    """

    def __init__(self, parent, description):
        """Create tab instantiator

        description - AppSysTabDefinition used to create tab.

        """
        self.tab = None
        self.button = AppSysFrameButton(
            parent,
            text=description.text,
            underline=description.underline)
        self.description = description

    def bind_tab_button(self, command):
        """Set bindings to raise tab to front of application."""
        self.button.make_command(command, self.description.identity)


# maybe combine AppSysTab and AppSysTabDefinition classes
class AppSysTabDefinition(object):
    
    """Tab definitions for AppSysFrame.

    Methods added:

    None
    
    Methods overridden:

    __init__

    Methods extended:

    None
    
    """

    def __init__(
        self,
        identity,
        text='',
        tooltip='',
        underline=-1,
        tabclass=None,
        position=-1,
        create_actions=None,
        destroy_actions=None):
        """Create tab definition

        identity - arbitrary identifier for tab.

        text - text displayed on button associated with tab.

        tooltip - tooltip text for button.

        underline - position of character in text for use in Alt-<character>
        to invoke button command. <0 means no Alt binding.

        tabclass - class to instantiate to create tab.

        position - button position in tab order relative to other tab buttons.
        <0 means add at end of list.

        create_actions - set of actions causing tabclass to be instantiated if
        not already done.  The action causing creation via the switch context
        method need not be in this set.

        destroy_actions - set of actions causing the current instatiation of
        tabclass to be destroyed if it exists.  All such actions must be in
        this set.  tabclass must provide a close method to tidy up before
        destruction.

        The actions are usually associated with an AppSysPanelButton or a
        MenuButton but never with an AppSysFrameButton.

        """
        self.identity = identity
        self.text = text
        self.tooltip = tooltip
        self.underline = underline
        self.tabclass = tabclass
        self.position = position
        try:
            self.create_actions = set(create_actions)
        except:
            self.create_actions = set()
        try:
            self.destroy_actions = set(destroy_actions)
        except:
            self.destroy_actions = set()

