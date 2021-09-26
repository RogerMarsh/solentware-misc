# reports.py
# Copyright 2007 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Demonstrate base classes for application dialogues and reports."""


if __name__ == "__main__":

    import tkinter

    from solentware_misc.gui import panel, frame

    from solentware_misc.gui.reports import AppSysReport

    class mAppSysPanel(panel.AppSysPanel):
        """Define report button identity for sample report application."""

        _btn_report = 100

        def __init__(self, parent, cnf=dict(), **kargs):
            """Create AppSysPanel widget with report generation button."""
            super(mAppSysPanel, self).__init__(parent=parent, cnf=cnf, **kargs)
            self.create_buttons()

        def describe_buttons(self):
            """Define report generation button."""
            self.define_button(
                self._btn_report,
                text="Report",
                tooltip="Report button Tooltip.",
                command=self.OnDialogue,
            )

        def get_headers(self):
            """Return sample header."""
            return ("Column0", "Column1", "Column2")

        def OnDialogue(self, event=None):
            """Handle display sample report dialogue event."""
            print("OnDialogue")
            d = AppSysReport(
                self.appsys,
                "Title",
                "Report action done on items",
                self.get_headers(),
                self.get_sample_report(),
                scale=50,
            )

        def get_sample_report(self):
            """Return sample data."""
            return (
                "\n".join(("r0c0", "r1c0", "r2c0", "r3c0")),
                "\n".join(("r0c1", "r1c1", "r2c1", "r3c0")),
                "\n".join(("r0c2", "r1c2", "r2c2", "r3c0")),
            )

    class mFrame(frame.AppSysFrame):
        """Provide tab name and state for application widget."""

        _tab_name = 10
        _state_start = 1

    class mApp(object):
        """Define a simple report application."""

        def __init__(self):
            """Define and display the report widget."""
            self.root = tkinter.Tk()
            self.root.wm_title("Test Report")
            self.mf = mFrame(
                master=self.root,
                background="cyan",
                width=200,
                height=100,
            )
            self.mf.define_tab(
                mFrame._tab_name,
                text="Name",
                tooltip="Name tooltip text",
                underline=1,
                tabclass=mAppSysPanel,
            )
            self.mf.create_tabs()
            self.mf.define_state_transitions(
                tab_state={
                    mFrame._state_start: (mFrame._tab_name,),
                },
                switch_state={
                    (None, None): [mFrame._state_start, mFrame._tab_name],
                },
            )
            self.mf.get_widget().pack(fill=tkinter.BOTH, expand=True)
            self.mf.get_widget().pack_propagate(False)
            self.mf.show_state()

    app = mApp()
    app.root.mainloop()
