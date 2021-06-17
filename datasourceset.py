# datasourceset.py
# Copyright 2008 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Provide DataSource interface for dataclients expecting DataSourceSet

DataSourceSet mainly takes advantage of DPT recordsets but a Berkeley DB
emulation is available.  Datagrids that can use the DataSourceSet class may
usefully display data via DataSource class.  This version of DataSourceSet
provides DataSource versions of DataSourceSet methods for compatibility.

Typical use is:
Display records in sorted order rather than in arbitrary recordset order.

See www.dptoolkit.com for details of DPT

List of classes

DataSourceSet

"""

from gridsup.core.dataclient import DataSource


class DataSourceSet(DataSource):
    
    """Define an interface between a database and GUI controls.
    
    Methods added:

    close
    get_recordset
    set_recordsets
    _clear_recordsets
    _in_recordset_field_equals_value

    Methods overridden:

    None

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
        
    def close(self):
        """Close resources."""
        self._clear_recordsets()
        
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
        """Set position in datasource by key.

        dbname: secondary (index) containing partial key values
        partial_keys: all combinations used as a partial key
        constant_keys: values added to each combintion
        include_without_constant_keys: all combinations without constant_keys
        added, as well, if True
        population: subset of records to partition by partial_keys.  Use all
        records if None
        """
        # maybe method _position_identified_players_display_at_selection from
        # playergrids needs to be changed so fill_view can be called in this
        # method


    def _clear_recordsets(self):
        """Destroy Record Sets."""
        self.recordsets.clear()
        
