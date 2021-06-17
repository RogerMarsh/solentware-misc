# dptdatasourceset.py
# Copyright 2008 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Provide bsddb style access to a list of DPT record sets and lists

Each record set in the list is displayed in record number order but the
records will not appear in an obvious sort order like alphabetical.  There
will be an application specific reason for the list of record sets to be in
the given order.

Typical use is:
Find the records that match each of the forenames initials and surname in a
given name.  Build sets that match as many as possible of the name elements
and display the reords with those that match most at start.

See www.dptoolkit.com for details of DPT

List of classes

DataSourceSet
CursorRS

"""

from dptdb import dptapi

from basesup.dptbase import CursorDPT

from gridsup.core.dataclient import DataSource


class DataSourceSet(DataSource):
    
    """Define an interface between a database and GUI controls.
    
    The database is an instance of a subclass of ./dptapi.DPTapi.
    
    Methods added:

    close
    get_recordset
    set_recordsets
    _clear_recordsets
    _in_recordset_field_equals_value

    Methods overridden:

    get_cursor

    Methods extended:

    __init__
    
    """

    def __init__(self, dbhome, dbset, dbname, newrow=None):
        """Define an interface between DPT database and GUI controls.
        
        See superclass for description of arguments.

        """
        super(DataSourceSet, self).__init__(
            dbhome, dbset, dbname, newrow=newrow)

        self.key_sets = []
        self.recordsets = dict()
        #self.partial_keys = dict()
        #self._fieldvalue = dptapi.APIFieldValue()
        
    def close(self):
        """Close resources."""
        self._clear_recordsets()
        
    def get_cursor(self):
        """Return cursor on record set, or list, associated with datasource."""
        if self.recordsets:
            return CursorRS(
                self.dbhome._dptfiles[self.dbset],
                self.dbhome._dptfiles[self.dbname]._primary,
                recordset=self.recordsets)
        else:
            dbfile = self.dbhome.get_database(self.dbset, self.dbname)
            empty = dbfile.CreateRecordList()
            return CursorRS(
                self.dbhome._dptfiles[self.dbset],
                self.dbhome._dptfiles[self.dbname]._primary,
                recordset={None:empty})

    def get_recordset(
        self,
        dbname,
        key=None,
        from_=None):
        """Create a recordset of records with key==key.

        dbname: secondary (index) used to partition records
        key: find records with value key on dbname
        When key=None find all records in from_
        from_: find records in record set from_ or record list from_.
        When from_=None find from all records in file.
        """
        if key is None:
            if from_ is None:
                return self._find_all_records()
            else:
                return self._in_recordset_find(dbname, from_)
        elif from_ is None:
            return self._find_field_equals_value(dbname, key)
        else:
            return self._in_recordset_field_equals_value(dbname, from_, key)

    def set_recordsets(
        self,
        dbname,
        partial_keys=None,
        constant_keys=None,
        include_without_constant_keys=False,
        population=None):
        """Create all combinations of partial keys.

        dbname: secondary (index) containing partial key values
        partial_keys: all combinations used as a partial key
        constant_keys: values added to each combintion
        include_without_constant_keys: all combinations without constant_keys
        added, as well, if True
        population: subset of records to partition by partial_keys.  Use all
        records if None
        """

        def set_partial_keys(
            partial,
            constant,
            new,
            old,
            add_without_constant=False):
            include_constant = [constant]
            if add_without_constant:
                include_constant.append(set())
            for ic in include_constant:
                for n in new:
                    new_without_n = new.copy()
                    new_without_n.remove(n)
                    old_with_n = ic.union(old)
                    old_with_n.add(n)
                    partial.add(tuple(sorted(old_with_n)))
                    if new_without_n:
                        set_partial_keys(
                            partial,
                            constant,
                            new_without_n,
                            old_with_n,
                            add_without_constant)

        if partial_keys is None:
            partial_keys = set()
        if constant_keys is None:
            constant_keys = set()
        combinations = set()
        set_partial_keys(
            combinations,
            constant_keys,
            partial_keys,
            set(),
            add_without_constant=include_without_constant_keys)

        dpn = []
        for pn in combinations:
            pns = set(pn)
            dpn.append((
                len(constant_keys) != len([n for n in constant_keys
                                           if n in pns]),
                -len([n for n in pn if len(n) > 1]),
                -len(pn),
                pn))
        self.key_sets = [pk[-1] for pk in sorted(dpn)]

        self._clear_recordsets()

        dbfile = self.dbhome.get_database(self.dbset, self.dbname)
        dbindex = self.dbhome._dptfiles[self.dbset]._secondary[dbname]
        all_records = self.get_recordset(
            dbindex, from_=population) # should be fd not fdwol
        unmatched_records = dbfile.CreateRecordList()
        unmatched_records.Place(all_records)
        for ks in self.key_sets:
            foundset = unmatched_records
            for k in ks:
                onfoundset = foundset
                foundset = self._in_recordset_field_equals_value(
                    dbindex, onfoundset, k)
                if onfoundset is not unmatched_records:
                    dbfile.DestroyRecordSet(onfoundset)
            if foundset is not unmatched_records:
                unmatched_records.Remove(foundset)
            if foundset.Count():
                self.recordsets[ks] = foundset
            elif foundset is not unmatched_records:
                dbfile.DestroyRecordSet(foundset)
        if unmatched_records.Count():
            self.recordsets[None] = unmatched_records
            self.key_sets.append(None)
        dbfile.DestroyRecordSet(all_records)
        self.key_sets = [ks for ks in self.key_sets if ks in self.recordsets]

    def _clear_recordsets(self):
        """Destroy Record Sets."""
        dbfile = self.dbhome.get_database(self.dbset, self.dbname)
        for rs in self.recordsets.itervalues():
            dbfile.DestroyRecordSet(rs)
        self.recordsets.clear()
        
    def _find_all_records(self):
        """Return APIFoundset containing all records on DPT file.
        """
        dbfile = self.dbhome.get_database(self.dbset, self.dbname)
        return dbfile.FindRecords()

    def _find_field_equals_value(self, dbname, value):
        """Return APIFoundset from foundset where fieldname contains value.

        value: field value
        """
        dbfile = self.dbhome.get_database(self.dbset, self.dbname)
        #dbname = self.dbhome._dptfiles[self.dbset]._secondary[self.dbname]
        return dbfile.FindRecords(
            dptapi.APIFindSpecification(
                dbname,#'Playerpartialname',#self.dbname,
                dptapi.FD_EQ,
                dptapi.APIFieldValue(value)))

    def _in_recordset_find(self, dbname, recordset):
        """Return APIFoundset containing all records on DPT file.
        """
        dbfile = self.dbhome.get_database(self.dbset, self.dbname)
        #dbname = self.dbhome._dptfiles[self.dbset]._secondary[self.dbname]
        return dbfile.FindRecords(
            dptapi.APIFindSpecification(
                dbname,#'Playerpartialname',#self.dbname,
                dptapi.FD_ALLRECS,
                dptapi.APIFieldValue('')),
            recordset)

    def _in_recordset_field_equals_value(self, dbname, recordset, value):
        """Return APIFoundset from foundset where fieldname contains value.

        recordset: DPT foundset or list.
        value: field value
        """
        dbfile = self.dbhome.get_database(self.dbset, self.dbname)
        #dbname = self.dbhome._dptfiles[self.dbset]._secondary[self.dbname]
        return dbfile.FindRecords(
            dptapi.APIFindSpecification(
                dbname,#'Playerpartialname',#self.dbname,
                dptapi.FD_EQ,
                dptapi.APIFieldValue(value)),
            recordset)


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

    def __init__(self, dptdb, fieldname, keyrange=None, recordset=None):
        """For testing use recordset[None] record set in a CursorDPT cursor.

        Detail of managing cursors on all the record sets in recordset are
        to be determiined.

        """
        super(CursorRS, self).__init__(
            dptdb, fieldname, keyrange=keyrange, recordset=recordset[None])

    def set_partial_key(self, partial):
        """Set partial key to None.  Always.
        
        Always set to None because the record set or list should be trimmed
        to the required records before passing to the cursor.
        
        """
        self._partial = None

