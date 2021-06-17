# textapi.py
# Copyright 2008 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Provide text file access using bsddb style methods.

Access is read only

List of classes

TextapiError - Exceptions
Textapi - Text database definition and API
TextapiRoot - Text file record level access
CursorText - Define cursor on file and access methods
_CursorText - Text file cursor operating on list of text lines

"""

import os
import os.path

from basesup.api.database import DatabaseError, Database
from basesup.api.database import Cursor

FILE = 'file'
FOLDER = 'folder'


class TextapiError(DatabaseError):
    pass


class Textapi(Database):
    
    """Implement Database API on a text file

    The database is read only.
    textdb databases consist of one or more files each of which has zero
    fields defined. File names are unique. Each file contains zero or more
    records where each record contains one line of text.
    Records are identified by line number within a file. The lowest possible
    record number is zero.
    Applications are expected to store instances of one class on a file.
    Each instance is a line of text on a file.

    Methods added:

    make_root

    Methods overridden:

    __init__ - define the text files in the database
    close_context - close text files
    exists - return True if text file exists
    make_cursor - create cursor on text file
    get_database - return the open text file
    get_primary_record - return (line number, line of text)
    is_primary - return True
    is_primary_recno - return True
    is_recno - return True
    open_context - open all text files in database
    decode_as_primary_key

    Methods extended:

    None
    
    """

    def __init__(self, textdbfiles, textdbfolder):
        """Define database structure
        
        textdb = {
            file:{
                folder:name,
                }, ...
            }

        dBasefolder = folder for files unless overridden in textdb

        """
        # The database definition from dBasefiles after validation
        self.textdbfiles = None
        
        # The folder from dBasefolder after validation
        self.textdbfolder = None

        # TextapiRoot objects for all textdb names.
        # {name:TextapiRoot instance, ...}
        self.main = dict()

        files = dict()
        pathnames = dict()

        try:
            textdbfolder = os.path.abspath(textdbfolder)
        except:
            msg = ' '.join(['Main folder name', str(textdbfolder),
                            'is not valid'])
            raise TextapiError, msg
        
        for dd in textdbfiles:
            if len(dd) == 0:
                raise TextapiError, 'Zero length file name'
            
            try:
                folder = textdbfiles[dd].get(FOLDER, None)
            except:
                msg = ' '.join(['textdb file definition for', repr(dd),
                                'must be a dictionary'])
                raise TextapiError, msg
            
            if folder == None:
                folder = textdbfolder
            try:
                folder = os.path.abspath(folder)
                fname = os.path.join(folder,
                                     textdbfiles[dd].get(FILE, None))
            except:
                msg = ' '.join(['File name for', dd, 'is invalid'])
                raise TextapiError, msg
            
            if fname in pathnames:
                msg = ' '.join(['File name', fname,
                                'linked to', pathnames[fname],
                                'cannot link to', dd])
                raise TextapiError, msg
            
            pathnames[fname] = dd
            files[dd] = {
                FILE:fname,
                }

            self.main[dd] = self.make_root(files[dd][FILE])

        self.textdbfiles = files
        self.textdbfolder = textdbfolder

    def close_context(self):
        """Close files."""
        for n in self.main:
            self.main[n].close()

    def exists(self, dbname, dummy):
        """Return True if dbname is one of the defined files.

        dummy is ignored.  It is present for compatibility with bsddb.

        """
        return dbname in self.main

    def make_cursor(self, dbname, dummy, keyrange=None):
        """Create a cursor on dbname.
        
        keyrange is an addition for DPT. It may yet be removed.
        dummy is ignored.  It is present for compatibility with bsddb.
        
        """
        if self.main[dbname]._object != None:
            return self.main[dbname].make_cursor()

    def get_database(self, dbname, dummy):
        """Return file for dbname.

        dummy is ignored.  It is present for compatibility with bsddb.

        """
        return self.main[dbname]._object

    def get_primary_record(self, dbname, record):
        """Return record.

        dbname is ignored.  It is present for compatibility with bsddb.

        """
        return record

    def is_primary(self, dbname, dummy):
        """Return True.

        dbname and dummy are ignored.  They are present for compatibility
        with bsddb.

        """
        return True

    def is_primary_recno(self, dbname):
        """Return True.

        dbname is ignored.  It is present for compatibility with bsddb.

        """
        return True

    def is_recno(self, dbname, dummy):
        """Return True.

        dbname and dummy are ignored.  They are present for compatibility
        with bsddb.

        """
        return True

    def open_context(self):
        """Open all files."""
        for n in self.main:
            self.main[n].open_root()
            if self.main[n]._object == None:
                for m in self.main:
                    self.main[n].close()
                msg = ' '.join(['Open file', repr(n)])
                raise TextapiError, msg

    def decode_as_primary_key(self, dbname, srkey):
        """Return srkey.

        dbname is ignored.  It is present for compatibility with bsddb.

        """
        return srkey

    def make_root(self, filename):

        return TextapiRoot(filename)


class TextapiRoot(object):
    
    """Provide record access to a text file in bsddb style.

    The cursor instance returned by Cursor() duplicates many methods in
    this class.  The bsddb interface provides similar methods on the
    underlying database and via cursors on that database.  In that
    context the behaviour can be very diferrent.
    
    Methods added:

    __del__
    close - close text file
    make_cursor - create a cursor
    open_root
    first
    last
    nearest
    next
    prior
    setat
    _set_closed_state
    _first_record
    _get_record
    _last_record
    _next_record
    _prior_record
    _select_first
    _select_last
    _select_next
    _select_prior
    _set_record_number
    
    Methods overridden:

    __init__ - define a text file

    Methods extended:

    None
    
    """

    def __init__(self, filename):
        
        self.filename = filename
        self._cursors = dict()
        self._set_closed_state()

    def __del__(self):
        
        self.close()

    def close(self):

        try:
            try:
                self._object.close()
            except:
                pass
        finally:
            self._set_closed_state()

    def make_cursor(self):
        """Create and return a record (line) cursor on the text file"""
        if self._object == None:
            return

        c = CursorText(self)
        self._cursors[c] = True
        return c

    def open_root(self):
        
        try:
            self._object = open(self.filename, 'rb')
            self.textlines = self._object.read().splitlines()
            self.record_count = len(self.textlines)
            self.record_number = None
            self.record_select = None
        except:
            self._object = None

    def first(self):
        """Return first record."""
        value = self._first_record()
        if value is not None:
            return (self.record_select, value)

    def last(self):
        """Return last record."""
        value = self._last_record()
        if value is not None:
            return (self.record_select, value)

    def nearest(self, current):
        """Return nearest record."""
        self._set_record_number(current)
        value = self._get_record()
        if value is not None:
            return (self.record_select, value)

    def next(self, current):
        """Return next record."""
        self._set_record_number(current)
        value = self._next_record()
        if value is not None:
            return (self.record_select, value)

    def prior(self, current):
        """Return prior record."""
        self._set_record_number(current)
        value = self._prior_record()
        if value is not None:
            return (self.record_select, value)

    def setat(self, current):
        """Return current record."""
        self._set_record_number(current)
        value = self._get_record()
        if value is not None:
            return (self.record_select, value)

    def _set_closed_state(self):
        
        self._object = None
        self.textlines = None
        self.record_count = None
        self.record_number = None
        self.record_select = None
        for c in self._cursors:
            c.close()
        self._cursors.clear()
        
    def _first_record(self):
        """Position at and return first line of text"""
        self._select_first()
        return self._get_record()

    def _get_record(self):
        """Return selected line of text."""
        if self._object == None:
            return None
        if self.record_select < 0:
            self.record_select = -1
            return None
        elif self.record_select >= self.record_count:
            self.record_select = self.record_count
            return None
        self.record_number = self.record_select
        return self.textlines[self.record_number]

    def _last_record(self):
        """Position at and return last line of text"""
        self._select_last()
        return self._get_record()

    def _next_record(self):
        """Position at and return next line of text"""
        self._select_next()
        return self._get_record()

    def _prior_record(self):
        """Position at and return prior line of text"""
        self._select_prior()
        return self._get_record()

    def _select_first(self):
        """Set record selection cursor at first record"""
        self.record_select = 0
        return self.record_select

    def _select_last(self):
        """Set record selection cursor at last record"""
        self.record_select = self.record_count - 1
        return self.record_select

    def _select_next(self):
        """Set record selection cursor at next record"""
        self.record_select = self.record_number + 1
        return self.record_select

    def _select_prior(self):
        """Set record selection cursor at prior record"""
        self.record_select = self.record_number - 1
        return self.record_select

    def _set_record_number(self, number):
        """Set record selection cursor at the specified record"""
        if not isinstance(number, int):
            self.record_select = -1
        elif number > self.record_count:
            self.record_select = self.record_count
        elif number < 0:
            self.record_select = -1
        else:
            self.record_select = number


class CursorText(Cursor):
    
    """Define cursor implemented using the Berkeley DB cursor methods.

    Methods added:

    __del__
    _get_record
    
    Methods overridden:

    __init__ - define a text file cursor
    close - close text file
    database_cursor_exists
    first
    last
    nearest
    next
    prev
    setat
    set_partial_key

    Methods extended:

    None
    
    """
    
    def __init__(self, dbobject):
        
        self._cursor = _CursorText(dbobject)

    def __del__(self):
        self.close()

    def close(self):
        if self._cursor is not None:
            self._cursor.close()
            self._cursor = None

    def database_cursor_exists(self):
        """Return True if database cursor exists and False otherwise"""
        return bool(self._cursor)

    def first(self):
        """First record taking partial key into account"""
        return self._get_record(self._cursor.first())

    def last(self):
        """Last record taking partial key into account"""
        return self._get_record(self._cursor.last())

    def set_partial_key(self, partial):
        """Set a partial key. Does nothing"""
        pass
        
    def _get_record(self, record):
        """Return record if key matches partial key (if any)."""
        return record

    def nearest(self, key):
        """Nearest record taking partial key into account"""
        return self._get_record(self._cursor.set_range(key))

    def next(self):
        """Next record taking partial key into account"""
        return self._get_record(self._cursor.next())

    def prev(self):
        """Previous record taking partial key into account"""
        return self._get_record(self._cursor.prev())

    def setat(self, record):
        """Position cursor at record taking partial key into account."""
        key, value = record
        return self._get_record(self._cursor.set(key))


class _CursorText(object):
    
    """Define a text file cursor

    Wrap the TextapiRoot methods in corresponding cursor method names.
    The methods with all lower case names emulate the bsddb cursor
    methods.

    Methods added:

    __del__
    close
    current
    first
    last
    next
    prev
    set
    set_both
    set_range
    
    Methods overridden:

    __init__ - define a text file cursor

    Methods extended:

    None
    
    """
    
    def __init__(self, dbobject):
        
        self._object = dbobject
        self._current = -1

    def __del__(self):
        self.close()

    def close(self):
        """Close cursor"""
        try:
            try:
                del self._object._cursors[self]
            except:
                pass
        finally:
            self._set_closed_state()

    def current(self):
        """Read current record."""
        r = self._object.setat(self._current)
        if r:
            self._current = r[0]
            return r

    def first(self):
        """Read first record."""
        r = self._object.first()
        if r:
            self._current = r[0]
            return r

    def last(self):
        """Read last record."""
        r = self._object.last()
        if r:
            self._current = r[0]
            return r

    def next(self):
        """Read next record."""
        r = self._object.next(self._current)
        if r:
            self._current = r[0]
            return r

    def prev(self):
        """Read prior record."""
        r = self._object.prior(self._current)
        if r:
            self._current = r[0]
            return r

    def set(self, key):
        """Read current record."""
        r = self._object.setat(key)
        if r:
            self._current = r[0]
            return r

    def set_range(self, key):
        """Read nearest record."""
        r = self._object.nearest(key)
        if r:
            self._current = r[0]
            return r

    def set_both(self, key, value):
        """Read nearest record."""
        r = self._object.nearest(key)
        if r:
            self._current = r[0]
            return r

    def _set_closed_state(self):

        self._object = None
        self._current = None

