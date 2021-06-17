# csvapi.py
# Copyright (c) 2007 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""CSV file access using bsddb style methods.

Adapted from dbaseapi.py adding index access

Access is read only and provided to support existing data import processes.

List of classes

CSVapiError - Exceptions
CSVapi - CSV database definition and API
CSV - Provide (key, value) style access to CSV record structure
CursorCSVfile - CSV cursor
_CSVapiRoot - CSV file definition and file level access
CSVapiRoot - CSV record level access
CursorCSV - CSV cursor (to be completed)

"""

import os
from cPickle import dumps
import csv
import bz2

from basesup.api.database import DatabaseError, Database, Cursor
from basesup.api.database import decode_record_number, encode_record_number
from basesup.api.constants import PRIMARY, SECONDARY, FILE, FOLDER, FIELDS


class CSVapiError(DatabaseError):
    pass


class CSVapi(Database):
    
    """Define a CSV database structure.
    
    The database is read only.
    CSV databases consist of one or more files each of which has zero
    or more fields defined. File names are unique and field names are
    unique within a file. Each file contains zero or more records where
    each record contains one occurrence of each field defined on the file.
    Records are identified by a record number that is unique within
    a file. The lowest possible record number is zero.
    Applications are expected to store instances of one class on a file.
    Each instance is a dictionary containing a subset of the fields
    defined for the file.
    
    Methods added:

    None

    Methods overridden:

    __init__
    close_context
    exists
    make_cursor
    get_database
    get_primary_record
    is_primary
    is_primary_recno
    is_recno
    open_context
    decode_as_primary_key

    Methods extended:

    None
    
    """

    def __init__(self, CSVfiles, CSVfolder):
        """Define database structure
        
        CSVfiles = {
            file:{
                folder:name,
                fields:{
                    name:{start:value, length:value, type:value}, ...
                    }
                }, ...
            }
        Field names and properties specified are constraints that must
        be true of the file

        CSVfolder = folder for files unless overridden in CSVfiles

        """
        # The database definition from CSVfiles after validation
        self.CSVfiles = None
        
        # The folder from CSVfolder after validation
        self.CSVfolder = None

        files = dict()
        pathnames = dict()
        sfi = 0

        try:
            CSVfolder = os.path.abspath(CSVfolder)
        except:
            msg = ' '.join(['Main folder name', str(CSVfolder),
                            'is not valid'])
            raise CSVapiError, msg
        
        for dd in CSVfiles:
            try:
                folder = CSVfiles[dd].get(FOLDER, None)
            except:
                msg = ' '.join(['dBase file definition for', repr(dd),
                                'must be a dictionary'])
                raise CSVapiError, msg
            
            if folder == None:
                folder = CSVfolder
            try:
                folder = os.path.abspath(folder)
                fname = os.path.join(folder,
                                     CSVfiles[dd].get(FILE, None))
            except:
                msg = ' '.join(['File name for', dd, 'is invalid'])
                raise CSVapiError, msg
            
            if fname in pathnames:
                msg = ' '.join(['File name', fname,
                                'linked to', pathnames[fname],
                                'cannot link to', dd])
                raise CSVapiError, msg
            
            pathnames[fname] = dd
            files[dd] = self.make_root(
                dd,
                fname,
                CSVfiles[dd],
                sfi)
            sfi += 1

        self.CSVfiles = files
        self.CSVfolder = CSVfolder

    def close_context(self):
        """Close files."""
        for n in self.CSVfiles:
            self.CSVfiles[n].close()

    def exists(self, dbset, dbname):
        """Return True if dbname is one of the defined files.

        dbset is ignored.  It is present for compatibility with bsddb.

        """
        return dbname in self.CSVfiles

    def make_cursor(self, dbname, indexname, keyrange=None):
        """Create a cursor on indexname in dbname.
        
        keyrange is an addition for DPT. It may yet be removed.
        
        """
        return self.CSVfiles[dbname].make_cursor(
            indexname,
            keyrange)

    def get_database(self, dbset, dbname):
        """Return file for dbname.

        dbset is ignored.  It is present for compatibility with bsddb.

        """
        return self.CSVfiles[dbname]._CSVobject

    def get_primary_record(self, dbname, record):
        """Return record.

        dbname is ignored.  It is present for compatibility with bsddb.

        """
        return record

    def is_primary(self, dbset, dbname):
        """Return True.

        dbset and dbname are ignored.  They are present for compatibility
        with bsddb.

        """
        return True

    def is_primary_recno(self, dbname):
        """Return True.

        dbname is ignored.  It is present for compatibility with bsddb.

        """
        return True

    def is_recno(self, dbset, dbname):
        """Return True.

        dbset and dbname are ignored.  They are present for compatibility
        with bsddb.

        """
        return True

    def open_context(self):
        """Open all files."""
        for n in self.CSVfiles:
            try:
                self.CSVfiles[n].open_root()
            except:
                for m in self.CSVfiles:
                    self.CSVfiles[n].close()
                raise

    def decode_as_primary_key(self, dbname, srkey):
        """Return srkey.

        dbname is ignored.  It is present for compatibility with bsddb.

        """
        return srkey

    def make_root(self, dd, fname, dptdesc, sfi):

        return CSVapiRoot(dd, fname, dptdesc, sfi)


class CSV(object):
    
    """Emulate Berkeley DB file and record structure for CSV files.
    
    The first, last, nearest, next, prior, and Set methods return the
    pickled value for compatibility with the bsddb and DPT interfaces.
    This is despite the data already being available as a dictionary
    of values keyed by field name.
    
    Methods added:

    __del__
    close - close text file
    Cursor - create a cursor
    open_csv
    first
    last
    nearest
    next
    prior
    Set
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
    _decode_number
    
    Methods overridden:

    __init__ - define a CSV file

    Methods extended:

    None
    
    """

    def __init__(self, filename):
        
        self.filename = filename
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
        """Create and return a record cursor on the CSV file"""
        if self._object == None:
            return

        return CursorCSVfile(self)

    def first(self):
        """Return first record not marked as deleted."""
        value = self._first_record()
        while value:
            if self.record_control == _EXISTS:
                return (self.record_select, dumps(value))
            elif self.record_control not in _PRESENT:
                return None
            value = self._next_record()

    def last(self):
        """Return last record not marked as deleted."""
        value = self._last_record()
        while value:
            if self.record_control == _EXISTS:
                return (self.record_select, dumps(value))
            elif self.record_control not in _PRESENT:
                return None
            value = self._prior_record()

    def nearest(self, current):
        """Return nearest record not marked as deleted."""
        self._set_record_number(current)
        value = self._get_record()
        while value:
            if self.record_control == _EXISTS:
                return (self.record_select, dumps(value))
            elif self.record_control not in _PRESENT:
                return None
            value = self._next_record()

    def next(self, current):
        """Return next record not marked as deleted."""
        self._set_record_number(current)
        value = self._next_record()
        while value:
            if self.record_control == _EXISTS:
                return (self.record_select, dumps(value))
            elif self.record_control not in _PRESENT:
                return None
            value = self._next_record()

    def open_csv(self):
        
        try:
            # use open or bz2 open depending on extension
            if os.path.splitext(self.filename)[-1].lower() == '.bz2':
                self._object = bz2.BZ2File(self.filename, 'r')
            else:
                self._object = open(self.filename, 'rb')
            reader = csv.DictReader(self._object)
            self.records = [row for row in reader]
            self.fields = reader.fieldnames
            print self.fields, len(self.records)
            self._object.close()
        except:
            print 'except'
            self._object = None

    def prior(self, current):
        """Return prior record not marked as deleted."""
        self._set_record_number(current)
        value = self._prior_record()
        while value:
            if self.record_control == _EXISTS:
                return (self.record_select, dumps(value))
            elif self.record_control not in _PRESENT:
                return None
            value = self._prior_record()

    def setat(self, current):
        """Return current record.  Return None if deleted."""
        self._set_record_number(current)
        value = self._get_record()
        if value:
            if self.record_control == _EXISTS:
                return (self.record_select, dumps(value))

    def _set_closed_state(self):
        
        self._object = None
        self.version = None
        self.record_count = None
        self.first_record_seek = None
        self.record_length = None
        self.fields = dict()
        self.record_number = None
        self.record_select = None
        self.record_control = None
        self.fieldnames = None
        self.sortedfieldnames = None
        
    def _first_record(self):
        """Position at and return first record."""
        self._select_first()
        return self._get_record()

    def _get_record(self):
        """Return selected record.
        
        Copy record deleted/exists marker to self.record_control.
        
        """
        if self._object == None:
            return None
        if self.record_select < 0:
            self.record_select = -1
            return None
        elif self.record_select >= self.record_count:
            self.record_select = self.record_count
            return None
        self.record_number = self.record_select
        seek = self.first_record_seek + self.record_number * self.record_length
        tell = self._object.tell()
        if seek != tell:
            self._object.seek(seek - tell, 1)
        fielddata = self._object.read(self.record_length)
        self.record_control = fielddata[0]
        '''if self.record_control in _PRESENT:
            result = {}
            for fieldname in self.fieldnames:
                s = self.fields[fieldname][START]
                f = self.fields[fieldname][START] + self.fields[fieldname][LENGTH]
                result[fieldname] = fielddata[s:f].strip()
            return result
        else:
            return None'''

    def _last_record(self):
        """Position at and return last record."""
        self._select_last()
        return self._get_record()

    def _next_record(self):
        """Position at and return next record."""
        self._select_next()
        return self._get_record()

    def _prior_record(self):
        """Position at and return prior record."""
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

    def _decode_number(self, number):
        """Return base256 string converted to integer."""
        result = 0
        for i in range(len(number),0,-1):
            result = 256 * result + ord(number[i - 1])
        return result


class CursorCSVfile(object):
    
    """Define a dBase III file cursor

    Wrap the CSV methods in corresponding cursor method names.
    
    Methods added:

    __del__
    close - close text file
    first
    last
    next
    prev
    setat
    
    Methods overridden:

    __init__ - define a CSV file cursor

    Methods extended:

    None
    
    """

    def __init__(self, dbobject):
        
        if isinstance(dbobject, CSV):
            self._object = dbobject
            self._current = -1
        else:
            self._object = None
            self._current = None

    def __del__(self):
        
        self.close()

    def close(self):

        self._object = None
        self._current = None

    def first(self):
        """Return first record not marked as deleted."""
        r = self._object.first()
        if r:
            self._current = r[0]
            return r

    def last(self):
        """Return last record not marked as deleted."""
        r = self._object.last()
        if r:
            self._current = r[0]
            return r

    def next(self):
        """Return next record not marked as deleted."""
        r = self._object.next(self._current)
        if r:
            self._current = r[0]
            return r

    def prev(self):
        """Return prior record not marked as deleted."""
        r = self._object.prior(self._current)
        if r:
            self._current = r[0]
            return r

    def setat(self, record):
        """Return current record.  Return None if deleted."""
        k, v = record
        r = self._object.setat(k)
        if r:
            self._current = r[0]
            return r


class _CSVapiRoot(object):
    
    """Provide file level access to a CSV file.

    This class containing methods to open and close dBase files.
    Record level access is the responsibility of subclasses.
    
    Methods added:

    __del__
    close - close CSV file
    is_field_primary
    open_root
    
    Methods overridden:

    __init__

    Methods extended:

    None
    
    """

    def __init__(self, dd, fname, dptdesc):
        """Define a CSV file.
        
        dd = file description name
        fname = path to data file (.dbf) for dd
        dptdesc = field description for data file
        
        """
        self._ddname = dd
        self._fields = None
        self._file = fname
        self._primary = None
        self._secondary = None
        self._CSVobject = None

        # Functions to convert numeric keys to string representation.
        # By default base 256 with the least significant digit at the right.
        # least_significant_digit = string_value[-1] (lsd = sv[-1])
        # most_significant_digit = string_value[0]
        # This conversion makes string sort equivalent to numeric sort.
        # These functions introduced to allow dbapi.py and dptapi.py to be
        # interchangeable for user classes. Another use found.
        # Use decode_record_number and encode_record_number

        fields = dptdesc.get(FIELDS, dict())
        if not isinstance(fields, dict):
            msg = ' '.join(['Field description of file', repr(dd),
                            'must be a dictionary'])
            raise CSVapiError, msg

        for fieldname in fields:
            if not isinstance(fieldname, str):
                msg = ' '.join(['Field name must be string not',
                                repr(fieldname),
                                'in file', dd,])
                raise CSVapiError, msg
            
            if not fieldname.isupper():
                msg = ' '.join(['Field name', fieldname,
                                'in file', dd,
                                'must be upper case'])
                raise CSVapiError, msg

            if fields[fieldname] == None:
                fields[fieldname] = dict()

        primary = dptdesc.get(PRIMARY, dict())
        if not isinstance(primary, dict):
            msg = ' '.join(['Field mapping of file', repr(dd),
                            'must be a dictionary'])
            raise CSVapiError, msg

        for p in primary:
            if not isinstance(p, str):
                msg = ' '.join(['Primary field name', str(p),
                                'for', dd,
                                'must be a string'])
                raise CSVapiError, msg

            f = primary[p]
            if f == None:
                f = p.upper()
                primary[p] = f
            elif not isinstance(f, str):
                msg = ' '.join(['Field', str(f),
                                'for primary field name', p,
                                'in file', dd,
                                'must be a string'])
                raise CSVapiError, msg

            if f not in fields:
                msg = ' '.join(['Field', f,
                                'for primary field name', p,
                                'in file', dd,
                                'must have a field description'])
                raise CSVapiError, msg

        secondary = dptdesc.get(SECONDARY, dict())
        if not isinstance(secondary, dict):
            msg = ' '.join(['Index definition of file', repr(dd),
                            'must be a dictionary'])
            raise CSVapiError, msg
        
        for s in secondary:
            if not isinstance(s, str):
                msg = ' '.join(['Index name', str(s),
                                'for', dd,
                                'must be a string'])
                raise CSVapiError, msg

            i = secondary[s]
            if i == None:
                i = (s.upper(),)
                secondary[s] = i
            elif not isinstance(i, tuple):
                msg = ' '.join(['Index definition', str(i),
                                'in field', s,
                                'in file', dd,
                                'must be a tuple of strings'])
                raise CSVapiError, msg

            for f in i:
                if not isinstance(f, str):
                    msg = ' '.join(['Field name', str(f),
                                    'in index definition for', s,
                                    'in file', dd,
                                    'must be a string'])
                    raise CSVapiError, msg

                if f not in fields:
                    msg = ' '.join(['Field', f,
                                    'for index definition', s,
                                    'in file', dd,
                                    'must have a field description'])
                    raise CSVapiError, msg

        self._fields = fields
        self._primary = primary
        self._secondary = secondary

    def close(self):
        """Close file."""
        try:
            self._CSVobject.close()
        except:
            pass
        self._CSVobject = None

    def is_field_primary(self, dbfield):
        """Return true if field is primary (not secondary test used)."""
        return dbfield not in self._secondary

    def open_root(self):
        """Open CSV file."""
        if self._CSVobject == True:
            opendb = CSV(self._file)
            opendb.open_csv()
            for f in self._fields:
                if f not in opendb.fields:
                    raise CSVapiError, ' '.join((
                        'Field', f, 'not in file', self._ddname))
            self._CSVobject = opendb
        elif self._CSVobject == False:
            raise CSVapiError, 'Create csv file not supported'
        return True
            
            
class CSVapiRoot(_CSVapiRoot):

    """Provide record level access to a CSV file.

    Methods added:

    make_cursor
    _get_deferable_update_files
    get_first_primary_key_for_index_key
    get_primary_record
    
    Methods overridden:

    None

    Methods extended:

    __init__
    close - close CSV file
    open_root
    
    """

    def __init__(self, dd, fname, dptdesc, sfi):
        """Define a CSV file.
        
        See base class for argument descriptions.
        sfi - for compatibility with bsddb
        
        """
        super(CSVapiRoot, self).__init__(dd, fname, dptdesc)
        
        # All active CursorCSV objects opened by make_cursor
        self._cursors = dict()

    def close(self):
        """Close file and cursors."""
        for c in self._cursors:
            c.close()
        self._cursors.clear()

        super(CSVapiRoot, self).close()
        

    def get_database(self):
        """Return the open file."""
        return self._CSVobject

    def make_cursor(self, indexname, keyrange=None):
        """Create a cursor on the CSV file."""
        if indexname not in self._secondary:
            #c = self._CSVobject.Cursor()
            c = CursorCSV(self._CSVobject, keyrange)
            if c:
                self._cursors[c] = True
            return c
        else:
            raise CSVapiError, 'Indexes not supported'

    def _get_deferable_update_files(self, defer, dd):
        """Return a dictionary of empty lists for the CSV files.

        Provided for compatibility with DPT

        """
        defer[dd] = {self._ddname : []} # _file rather than _ddname?
            
            
    def get_first_primary_key_for_index_key(self, dbfield, key):
        """Return None.  Deny existence of primary key.

        Provided for compatibility with DPT.

        """
        return None

    def get_primary_record(self, dbname, key):
        """Return None.  Deny existence of primary record.

        Provided for compatibility with DPT.

        """
        return None # return the pickled dictionary of field values


    def open_root(self):
        """Open CSV file."""
        pathname = self._file
        foldername, filename = os.path.split(pathname)
        if os.path.exists(foldername):
            if not os.path.isdir(foldername):
                msg = ' '.join([foldername, 'exists but is not a folder'])
                raise CSVapiError, msg
            
        else:
            os.makedirs(foldername)
        if os.path.exists(pathname):
            if not os.path.isfile(pathname):
                msg = ' '.join([pathname, 'exists but is not a file'])
                raise CSVapiError, msg

            if self._CSVobject == None:
                self._CSVobject = True
        elif self._CSVobject == None:
            self._CSVobject = False
            
        return super(CSVapiRoot, self).open_root()
            

class CursorCSV(CursorCSVfile, Cursor):
    
    """Define a CSV cursor.
    
    Clearly not finished.  So notes left as found.

    A cursor implemented using a CursorCSVfile cursor for access in
    record number order. Index access is not supported.
    This class and its methods support the api.dataclient.DataClient class
    and may not be appropriate in other contexts.
    CursorCSV is a subclass of CursorCSVfile at present. The methods
    of CursorCSVfile are named to support DataClient directly but
    set_partial_key is absent. May be better to follow CursorDB and
    CursorDPT classes and make the CursorCSVfile instance an attibute
    of CursorCSV. CSV.Cursor() supports this.
    
    Methods added:

    None
    
    Methods overridden:

    set_partial_key

    Methods extended:

    __init__
    
    """

    def __init__(self, dbasedb, keyrange=None):
        
        super(CursorCSV, self).__init__(dbobject=dbasedb)

    def set_partial_key(self, partial):
        """Do nothing.  Partial key not relevant."""
        pass

