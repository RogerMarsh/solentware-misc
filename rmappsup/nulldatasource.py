# nulldatasource.py
# Copyright 2008 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Providing bsddb style access to a null source of data."""

from basesup.api.database import Cursor

from gridsup.core.dataclient import DataSource


class NullDataSource(DataSource):
    
    """Define an interface between a database and GUI controls.
    
    This class provides a zero cursor in an otherwise normal datasource.
    Intended use is where dataclient asks for something that the database
    cannot provide.
    
    Methods added:

    build_recordset
    set_recordset

    Methods overridden:

    get_cursor

    Methods extended:

    None
    
    """

    def build_recordset(self, specification):
        """Retun null record."""
        return dict()

    def get_cursor(self):
        """Return cursor on the record set associated with datasource."""
        return CursorNull()

    def set_recordset(self, records):
        """Do nothing.  Null datasource."""
        return


class CursorNull(Cursor):
    
    """A null cursor - all methods do nothing rather than not being implemented

    Methods added:

    None

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

    def __init__(self):
        """Define a cursor to access a null database."""
        super(CursorNull, self).__init__()

    def close(self):
        return None

    def first(self):
        return None

    def last(self):
        return None

    def set_partial_key(self, partial):
        return None
        
    def nearest(self, key):
        return None

    def next(self):
        return None

    def prev(self):
        return None

    def setat(self, record):
        return None

