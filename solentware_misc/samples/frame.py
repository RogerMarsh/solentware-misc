# frame.py
# Copyright 2007 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Demonstrate notebook style database User Interface class."""


if __name__ == "__main__":
    import tkinter

    from solentware_misc.gui import panel

    from solentware_misc.gui.frame import AppSysFrame

    class addressAppSysPanel(panel.AppSysPanel):
        """Define a sample application panel.

        The panel has update, clear, and cancel, buttons.
        """

        _btn_update = 200
        _btn_clear = 201
        _btn_cancel = 203

        def __init__(self, parent, cnf=dict(), **kargs):
            """Create a sample application panel."""
            super(addressAppSysPanel, self).__init__(
                parent=parent, cnf=cnf, **kargs
            )
            self.create_buttons()

        def describe_buttons(self):
            """Define application panel action buttons."""
            self.define_button(
                self._btn_update,
                text="Update",
                tooltip="Update button Tooltip.",
                switchpanel=True,
                underline=0,
                command=self.on_update,
            )
            self.define_button(
                self._btn_clear,
                text="Clear",
                tooltip="Clear button Tooltip.",
                command=self.on_clear,
            )
            self.define_button(
                self._btn_cancel,
                text="Cancel",
                tooltip="Cancel button Tooltip.",
                switchpanel=True,
                underline=2,
                command=self.on_cancel,
            )

        def on_cancel(self, event=None):
            """Handle cancel button events."""
            print("on_cancel")

        def on_clear(self, event=None):
            """Handle clear button events."""
            print("on_clear")

        def on_update(self, event=None):
            """Handle update button events."""
            print("on_update")

    class nameAppSysPanel(panel.AppSysPanel):
        """Define a sample application panel.

        The panel has ok, refresh, and cancel, buttons.
        """

        _btn_ok = 100
        _btn_refresh = 101
        _btn_cancel = 103

        def __init__(self, parent, cnf=dict(), **kargs):
            """Create a sample application panel."""
            super(nameAppSysPanel, self).__init__(
                parent=parent, cnf=cnf, **kargs
            )
            self.create_buttons()

        def describe_buttons(self):
            """Define application panel action buttons."""
            self.define_button(
                self._btn_ok,
                text="OK",
                tooltip="OK button Tooltip.",
                switchpanel=True,
                command=self.on_ok,
            )
            self.define_button(
                self._btn_cancel,
                text="Cancel",
                tooltip="Cancel button Tooltip.",
                underline=2,
                command=self.on_cancel,
            )
            self.define_button(
                self._btn_refresh,
                text="Refresh",
                tooltip="Refresh button Tooltip.",
                underline=0,
                command=self.on_refresh,
                position=1,
            )

        def on_cancel(self, event=None):
            """Handle cancel button events."""
            print("on_cancel")

        def on_ok(self, event=None):
            """Handle ok button events."""
            print("on_ok")

        def on_refresh(self, event=None):
            """Handle refresh button events."""
            print("on_refresh")

    class testAppSysFrame(AppSysFrame):
        """Define a custom AppSysFrame.

        The AppSysFrame has two tabs and two states.
        """

        _tab_name = 10
        _tab_address = 11

        _state_start = 1
        _state_address = 2

    class AppSys(object):
        """Define a sample application using testAppSysFrame class."""

        def __init__(self):
            """Create the sample application."""
            self.root = tkinter.Tk()
            self.root.wm_title("Test Application")
            self.mf = testAppSysFrame(
                master=self.root,
                background="cyan",
                width=200,
                height=100,
            )

            self.mf.define_tab(
                testAppSysFrame._tab_name,
                text="Name",
                tooltip="Name tooltip text",
                underline=1,
                tabclass=nameAppSysPanel,
            )
            self.mf.define_tab(
                testAppSysFrame._tab_address,
                text="Address",
                tooltip="Address tooltip text",
                underline=1,
                tabclass=addressAppSysPanel,
            )

            self.mf.create_tabs()

            self.mf.define_state_transitions(
                tab_state={
                    testAppSysFrame._state_start: (
                        testAppSysFrame._tab_name,
                        testAppSysFrame._tab_address,
                    ),
                    testAppSysFrame._state_address: (
                        testAppSysFrame._tab_name,
                        testAppSysFrame._tab_address,
                    ),
                },
                switch_state={
                    (None, None): [
                        testAppSysFrame._state_start,
                        testAppSysFrame._tab_name,
                    ],
                    (testAppSysFrame._state_start, nameAppSysPanel._btn_ok): [
                        testAppSysFrame._state_address,
                        testAppSysFrame._tab_address,
                    ],
                    (
                        testAppSysFrame._state_address,
                        addressAppSysPanel._btn_update,
                    ): [
                        testAppSysFrame._state_start,
                        testAppSysFrame._tab_name,
                    ],
                    (
                        testAppSysFrame._state_address,
                        addressAppSysPanel._btn_cancel,
                    ): [
                        testAppSysFrame._state_start,
                        testAppSysFrame._tab_name,
                    ],
                },
            )

            self.mf.get_widget().pack(fill=tkinter.BOTH, expand=True)
            self.mf.get_widget().pack_propagate(False)
            self.mf.show_state()

    app = AppSys()
    app.root.mainloop()
