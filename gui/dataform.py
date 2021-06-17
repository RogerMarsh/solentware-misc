# dataform.py
# Copyright 2007 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Base class for displaying a single record (a form)."""

#######
# not tested as not completed
#
# Actually this will not be completed.  A form is a grid where one row is
# displayed.  Thus a subclass of datagrid, along with a subclass of DataRow
# relevant to the form style, will be used.
#
#######
import Tkinter

from gridsup.core.dataclient import DataClient
from datacontrol import DataControl


class DataForm(DataClient, DataControl):
    """Display a DB record.

    The row definition class given to the DataClient via
    a DataSource class must provide a number of methods
    with pre-determined names that create and populate
    the widgets placed in the DataForm sizer. This in
    turn is used as a component in a parent widget.
    """

    def __init__(self, parent):
        """Create form.

        self.parent: parent widget for all widgets in this sizer
        self.rows: DataClient provides one record
        """
        
        super(DataForm, self).__init__()

        self.parent = parent
        self.rows = 1
        
        # Top frame for form widget
        self.frame = frame = Tkinter.Frame(parent)
        frame.bind('<KeyRelease>', self.on_key_release)

    def load_control(self):
        """Replace existing rows in sizer and fill it."""

        #self.destroy_children(self.container.GetChildren())
        
        self.objects[self.keys[0]].form_row(self.parent, self)

    def load_data_change(self, oldkeys, newkeys):
        """Replace existing rows in sizer and fill it."""

        if newkeys == None:
            for key in oldkeys:
                if key in self.keys:
                    self.keys.remove(key)
            self.fill_view_from_item_index(0)
        elif newkeys == False:
            self.fill_view_from_record(oldkeys[0])
        else:
            self.fill_view_from_record(newkeys[0])

    def on_key_release(self, event=None):
        """Process form commands."""

        k = event.keysym
        if k == 'Up':
            pass #self.LoadControlUp(0, -1)
        elif k == 'Down':
            pass #self.LoadControlDown(-1, 1)
        elif k == 'Home':
            pass #self.LoadControlDown()
        elif k == 'End':
            pass #self.LoadControlUp()
        elif k == 'Insert':
            pass #self.edit_dialog(self.keys[0], event)
        elif k == 'Delete':
            pass #self.delete_dialog(self.keys[0], event)
