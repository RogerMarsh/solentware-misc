# __init__.py
# Copyright 2007 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""rmappsup.gui package

The rmappsup.gui package assumes that an application is presented in notebook
style.  The frame and panel modules implement this structure.

The AppSysFrame class, in frame.py, provides for a set of tab buttons to switch
between a set of pages each implemented using the AppSysPanel class in panel.py.
Actions are assumed to be invoked by a set of buttons on each page: each button
is an instance of the AppSysPanelButton class in panel.py.

The application menu raises the possibility of actions that are independant of
any page; or are common to several pages perhaps without the presence of buttons
on each page for the action.

Tab buttons, and thus pages, are put in sets that are displayed together.  A tab
button can be put in many sets.  Page buttons, and menu actions, are allowed to
display a different set of tab buttons as part of their action but cannot alter
these sets.


The rmappsup.gui package assumes that an application is presenting records from
a database in a scrollable grid with each record being displayed in appropriate
style.  The datagrid module implements scrolling and the datarow module provides
record display.

Records are assumed to be pickled class instances and access to the data on a
record is via the Record class in rmappsup.api.record.py.
"""
