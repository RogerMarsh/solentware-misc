# dbdatasource.py
# Copyright 2008 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Emulate DPT record sets and provide bsddb style access.

Likely to be very slow compared with DPT version.

Current implementation supports a very limited set of selection criteria.
In fact just sufficient to see that the technique is capable of producing
the same answer as the DPT version.

Typical use is:
Build a dictionary representing a record set by calling build_recordset with
appropriate selection criteria.  Call set_recordset(<dictionary>) to give the
cursor a sorted record set.  The DBDataSource instance links the sorted record
set to a grid control (GUI) to display the records in a scrollable list.

List of classes

DBDataSource
CursorRS

"""

from basesup.api.database import Cursor

from gridsup.core.dataclient import DataSource


class DBDataSource(DataSource):
    
    """Define an interface between a database and GUI controls.
    
    The database is an instance of a subclass of ./dbapi.DBapi.
    
    Methods added:

    build_recordset
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
        super(DBDataSource, self).__init__(
            dbhome, dbset, dbname, newrow=newrow)

        self.keymap = dict()
        self.recordset = []
        
    def build_recordset(self, specification):
        """Return record set built from specification.
        
        specification := ( operator, condition <, condition> )
        condition := specification | ( comparison, file, field, value )
        operator := 'and' | 'or'
        comparison := '==' | '!='
        file := '*dbset name to search*'
        field := '*secondary index name on dbset*'
        value := '*string*'
        A symbol cannot be both operator and comparison.

        Perhaps it would be better to provide a parser of the SQL select
        statement (select * ... only) and scan the database using CursorRS
        cursors defined as specified by the select statement to build the
        record set.
        
        """
        records = None
        operator = None
        searches = dict()
        
        for s in specification:
            if isinstance(s, tuple):
                condition, dbset, dbname, value = s
                if condition == '==':
                    cursordb = self.dbhome.make_cursor(dbset, dbname)
                    cursor = cursordb._cursor
                    r = cursor.set_range(value)
                    if s not in searches:
                        sr = searches[s] = dict()
                        while r is not None:
                            k, v = r
                            if k != value:
                                break
                            sr[v] = k
                            r = cursor.next()
                    cursordb.close()
            elif isinstance(s, str):
                if operator is None:
                    operator = s
        for s in searches:
            if records is None:
                records = searches[s]
            elif operator == 'and':
                pruned = dict()
                for p in searches[s]:
                    if p in records:
                        pruned[p] = searches[s][p]
                records = pruned
            elif operator == 'or':
                for p in searches[s]:
                    records[p] = searches[s][p]
        if records is None:
            return dict()
        else:
            return records

    def get_cursor(self):
        """Return cursor on the record set associated with datasource."""
        return CursorRS(self.keymap, self.recordset)

    def set_recordset(self, records):
        """Set self.recordset to sorted records (a dictionary)."""
        records.sort()
        self.recordset = records
        self.keymap.clear()
        for k, v in self.recordset:
            self.keymap[k] = len(self.keymap)


class CursorRS(Cursor):
    
    """A Cursor cursor that does not implement partial keys.
    
    If a subset of the records on self.recordset is needed do more selection
    to get the subset and pass this to the cursor.

    Methods added:

    database_cursor_exists

    Methods overridden:

    close
    first
    last
    set_partial_key
    nearest
    next
    prev
    setat

    Methods extended:

    __init__
    
    """

    def __init__(self, keymap, recordset):
        """Define a cursor to access recordset in the order given in keymap."""
        super(CursorRS, self).__init__()

        self.current = None
        self.direct = keymap
        self.records = recordset

    def close(self):

        self.current = None
        self.direct = None
        self.records = None

    def database_cursor_exists(self):
        """Return True if self.records is not None and False otherwise

        Simulates existence test for a database cursor.

        """
        # The cursor methods are defined in this class and operate on
        # self.records if it is a list so do that test here as well.
        return self.records is not None

    def first(self):
        """Return first record."""
        if self.records is None:
            return None
        if len(self.records):
            self.current = 0
            return self.records[self.current]

    def last(self):
        """Return last record."""
        if self.records is None:
            return None
        if len(self.records):
            self.current = len(self.records) - 1
            return self.records[self.current]

    def set_partial_key(self, partial):
        """Set partial key to None.  Always.
        
        Always set to None because the recordset oand keymap should be trimmed
        to the required records before passing to the cursor.
        
        """
        self._partial = None
        
    def nearest(self, key):
        """Return nearest record."""
        if self.records is not None:
            if key in self.direct:
                n = self.direct[key]
                if n < len(self.records):
                    self.current = n
                    return self.records[n]
        return None

    def next(self):
        """Return next record."""
        if self.records is None:
            return None
        if self.current is None:
            return self.first()
        elif self.current == len(self.records) - 1:
            return None
        else:
            self.current += 1
        return self.records[self.current]

    def prev(self):
        """Return previous record."""
        if self.records is None:
            return None
        if self.current is None:
            return self.last()
        elif self.current == 0:
            return None
        else:
            self.current -= 1
        return self.records[self.current]

    def setat(self, record):
        """Return record after positioning cursor at record."""
        if self.records is not None:
            k, v = record
            if k in self.direct:
                n = self.direct[k]
                if n < len(self.records):
                    self.current = n
                    return self.records[n]
        return None

