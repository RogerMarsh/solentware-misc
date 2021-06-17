# setup.py
# Copyright 2011 Roger Marsh
# Licence: See LICENCE (BSD licence)

import sys
from distutils.core import setup

from rmappsup import _rmappsup_version

setup(
    name='-'.join(
        ('rmappsup',
         ''.join(
             ('py',
              '.'.join(
                  (str(sys.version_info[0]),
                   str(sys.version_info[1]))))),
         )),
    version=_rmappsup_version,
    description='Classes perhaps useful beyond original application',
    author='solentware.co.uk',
    author_email='roger.marsh@solentware.co.uk',
    url='http://www.solentware.co.uk',
    packages=[
        'rmappsup',
        'rmappsup.api', 'rmappsup.gui',
        ],
    package_data={
        'rmappsup': ['README', 'LICENCE'],
        },
    long_description='''Classes perhaps useful beyond original application

    rmappsup:
    
    textapi.py - basesup interface to a text file
    bz2textapi.py - extend textapi to bz2 files
    ziptextapi.py - extend textapi to zip files
    csvapi.py - basesup interface to a csv file
    dbaseapi.py - basesup interface to a dbaseIII file
    nulldatasource.py - basesup interface to nothing
    dptdatasource.py - basesup interface to arbitrary DPT list or record set
    dbdatasource.py - emulation of dptdatasource.py for Berkeley DB
    dptdatasourceset.py - display a set of DPT record sets in arbitrary order.
    datasourceset.py - emulation of dptdatasourceset.py for Berkeley DB

    rmappsup/api:

    indexmap.py - DPT style bitmap manager
    null.py - Null object from Python Cookbook
    utilities.py - Some name and date methods

    rmappsup/gui:

    frame.py - customised Tkinter.Frame widget for notebook style GUI
    panel.py - customised Tkinter.Frame widget for notebook style GUI
    reports.py - customised Tkinter.Toplevel for reports and dialogues
    colourslider.py - widget for choosing colours
    fontchooser.py - widget for selecting fonts
    dataform.py - obsolete part of gridsup (form is grid with one row)
    dbasedatarow.py - row definition for dbaseIII records with dbaseapi.py
    textdatarow.py - row definition for text records with textapi.py
    textentry.py - customised Tkinter.Text widget
    textreadonly.py - customised Tkinter.Text widget
    texttab.py - customised Tkinter.Text widget
    ''',
    )
