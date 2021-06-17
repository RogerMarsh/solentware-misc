# dptdatasource.py
# Copyright 2008 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Provide bsddb style access to DPT record sets and lists

Typical use is:
Create a record set or list with whatever selection criteria (DPT Find) are
appropriate.  Pass this record set or list to a CursorRS instance.  The
DPTDataSource instance links the record set or list to a grid control (GUI)
to display the records in a scrollable list.

See www.dptoolkit.com for details of DPT

List of classes

DPTDataSource
CursorRS

"""

from dptdb import dptapi

from basesup.dptbase import CursorDPT

from gridsup.core.dataclient import DataSource


class DPTDataSource(DataSource):
    
    """Define an interface between a database and GUI controls.
    
    The database is an instance of a subclass of ./dptapi.DPTapi.
    
    Methods added:

    close
    join_field_occurrences
    set_recordset

    Methods overridden:

    get_cursor

    Methods extended:

    __init__
    
    """

    def __init__(self, dbhome, dbset, dbname, newrow=None):
        """Define an interface between DPT database and GUI controls.
        
        See superclass for description of arguments.

        """
        super(DPTDataSource, self).__init__(
            dbhome, dbset, dbname, newrow=newrow)

        self.recordset = None
        self._fieldvalue = dptapi.APIFieldValue()
        self.dbhome._dptfiles[self.dbset]._sources[self] = None
        
    def close(self):
        if self.recordset is not None:
            try:
                del self.dbhome._dptfiles[self.dbset]._sources[self]
            except:
                pass
            self.dbhome._dptfiles[self.dbset].get_database().DestroyRecordSet(
                self.recordset)
            self.recordset = None

    def get_cursor(self):
        """Return cursor on record set, or list, associated with datasource."""
        if self.recordset:
            c = CursorRS(
                self.dbhome._dptfiles[self.dbset],
                self.dbhome._dptfiles[self.dbname]._primary,
                recordset=self.recordset)
        else:
            c = CursorRS(
                self.dbhome._dptfiles[self.dbset],
                self.dbhome._dptfiles[self.dbname]._primary,
                recordset=self.dbhome.get_database(
                    self.dbset, self.dbname).CreateRecordList())
        if c:
            self.dbhome._dptfiles[self.dbset]._cursors[c] = True
        return c

    def join_field_occurrences(self, record, field):
        """Return concatenated occurrences of field."""
        i = 1
        v = []
        while record.GetFieldValue(field, self._fieldvalue, i):
            v.append(self._fieldvalue.ExtractString())
            i += 1
        return ''.join(v)

    def set_recordset(self, records):
        """Set self.recordset to records (a DPT record set or list)."""
        self.recordset = records


class CursorRS(CursorDPT):
    
    """A CursorDPT cursor with partial keys disabled.
    
    If a subset of the records on self.recordset is needed do more Finds
    to get the subset and pass this to the cursor.

    Likely to become an independent cursor since the direct value set
    option of CursorDPT is irrelevant.

    Methods added:

    None

    Methods overridden:

    set_partial_key

    Methods extended:

    None
    
    """

    def set_partial_key(self, partial):
        """Set partial key to None.  Always.
        
        Always set to None because the record set or list should be trimmed
        to the required records before passing to the cursor.
        
        """
        self._partial = None

