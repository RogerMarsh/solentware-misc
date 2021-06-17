# dbaseapi.py
# Copyright (c) 2007 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""dBaseIII file access using bsddb style methods.

<Reference to code copied to be inserted if ever found again>

Access is read only and provided to support existing data import processes.

List of classes

dBaseapiError - Exceptions
dBaseapi - dBaseIII database definition and API
dBaseIII - Provide (key, value) style access to dBaseIII record structure
CursordBaseIII - dBaseIII cursor
_dBaseapiRoot - dBaseIII file definition and file level access
dBaseapiRoot - dBaseIII record level access
CursordBase - dBaseIII cursor (to be completed)

"""

import os
import os.path
from cPickle import dumps

from basesup.api.database import DatabaseError, Database, Cursor
from basesup.api.database import decode_record_number, encode_record_number
from basesup.api.constants import PRIMARY, SECONDARY, FILE, FOLDER, FIELDS

# dBaseIII specific items are not yet worth putting in api.constants
# because the definition is provided to support data import only
START = 'start'
LENGTH = 'length'
TYPE = 'type'
DBASE_FIELDATTS = {
    START:int,
    LENGTH:int,
    TYPE:str,
    }
_VERSIONMAP = {'\x03':'dBase III'}
C, N, L, D, F = 'C', 'N', 'L', 'D', 'F'
_FIELDTYPE = {
    C:'Character',
    N:'Numeric',
    L:'Boolean',
    D:'Date',
    F:'Float',
    }
_DELETED = chr(42)
_EXISTS = chr(32)
_PRESENT = {_DELETED:None, _EXISTS:None}


class dBaseapiError(DatabaseError):
    pass


class dBaseapi(Database):
    
    """Define a dBaseIII database structure.
    
    The database is read only.
    dBaseIII databases consist of one or more files each of which has zero
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

    def __init__(self, dBasefiles, dBasefolder):
        """Define database structure
        
        dBasefiles = {
            file:{
                folder:name,
                fields:{
                    name:{start:value, length:value, type:value}, ...
                    }
                }, ...
            }
        Field names and properties specified are constraints that must
        be true of the file

        dBasefolder = folder for files unless overridden in dBasefiles

        """
        # The database definition from dBasefiles after validation
        self.dBasefiles = None
        
        # The folder from dBasefolder after validation
        self.dBasefolder = None

        files = dict()
        pathnames = dict()
        sfi = 0

        try:
            dBasefolder = os.path.abspath(dBasefolder)
        except:
            msg = ' '.join(['Main folder name', str(dBasefolder),
                            'is not valid'])
            raise dBaseapiError, msg
        
        for dd in dBasefiles:
            try:
                folder = dBasefiles[dd].get(FOLDER, None)
            except:
                msg = ' '.join(['dBase file definition for', repr(dd),
                                'must be a dictionary'])
                raise dBaseapiError, msg
            
            if folder == None:
                folder = dBasefolder
            try:
                folder = os.path.abspath(folder)
                fname = os.path.join(folder,
                                     dBasefiles[dd].get(FILE, None))
            except:
                msg = ' '.join(['File name for', dd, 'is invalid'])
                raise dBaseapiError, msg
            
            if fname in pathnames:
                msg = ' '.join(['File name', fname,
                                'linked to', pathnames[fname],
                                'cannot link to', dd])
                raise dBaseapiError, msg
            
            pathnames[fname] = dd
            files[dd] = self.make_root(
                dd,
                fname,
                dBasefiles[dd],
                sfi)
            sfi += 1

        self.dBasefiles = files
        self.dBasefolder = dBasefolder

    def close_context(self):
        """Close files."""
        for n in self.dBasefiles:
            self.dBasefiles[n].close()

    def exists(self, dbset, dbname):
        """Return True if dbname is one of the defined files.

        dbset is ignored.  It is present for compatibility with bsddb.

        """
        return dbname in self.dBasefiles

    def make_cursor(self, dbname, indexname, keyrange=None):
        """Create a cursor on indexname in dbname.
        
        keyrange is an addition for DPT. It may yet be removed.
        
        """
        return self.dBasefiles[dbname].make_cursor(
            indexname,
            keyrange)

    def get_database(self, dbset, dbname):
        """Return file for dbname.

        dbset is ignored.  It is present for compatibility with bsddb.

        """
        return self.dBasefiles[dbname]._dbaseobject

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
        for n in self.dBasefiles:
            try:
                self.dBasefiles[n].open_root()
            except:
                for m in self.dBasefiles:
                    self.dBasefiles[n].close()
                raise

    def decode_as_primary_key(self, dbname, srkey):
        """Return srkey.

        dbname is ignored.  It is present for compatibility with bsddb.

        """
        return srkey

    def make_root(self, dd, fname, dptdesc, sfi):

        return dBaseapiRoot(dd, fname, dptdesc, sfi)


class dBaseIII(object):
    
    """Emulate Berkeley DB file and record structure for dBase III files.
    
    The first, last, nearest, next, prior, and Set methods return the
    pickled value for compatibility with the bsddb and DPT interfaces.
    This is despite the data already being available as a dictionary
    of values keyed by field name.
    
    Methods added:

    __del__
    close - close text file
    make_cursor - create a cursor
    open_dbf
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

    __init__ - define a dBaseIII file

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

    def encode_number(self, number):
        """Convert integer to base 256 string length 4 and return.

        Least significant digit at left as in dbaseIII record count.
        """
        s = []
        while number:
            number, r = divmod(number, 256)
            s.append(chr(r))
        ls = 4 - len(s)
        if ls > 0:
            s.extend([chr(0)] * ls)
        elif  ls < 0:
            return ''.join(s[:4])
        return ''.join(s)

    def make_cursor(self):
        """Create and return a record cursor on the dBaseIII file"""
        if self._object == None:
            return

        return CursordBaseIII(self)

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

    def open_dbf(self):
        
        try:
            # file header consists of 32 bytes
            self._object = open(self.filename, 'rb')
            header = self._object.read(32)
            self.file_header.append(header)
            self.version = header[0]
            self.record_count = self._decode_number(header[4:8])
            self.first_record_seek = self._decode_number(header[8:10])
            self.record_length = self._decode_number(header[10:12])
            #field definitions are 32 bytes
            #field definition trailer is 1 byte \r
            fieldnames = []
            self.fields = {}
            fieldstart = 1
            fielddef = self._object.read(32)
            terminator = fielddef[0]
            while terminator != '\r':
                if len(fielddef) != 32:
                    self._object = self.close()
                    break
                self.file_header.append(fielddef)
                nullbyte = fielddef.find('\x00',0)
                if nullbyte == -1:
                    nullbyte = 11
                elif nullbyte > 10:
                    nullbyte = 11
                fieldname = fielddef[:nullbyte]
                ftype = fielddef[11]
                fieldlength = ord(fielddef[16])
                if _FIELDTYPE.has_key(ftype):
                    fieldnames.append(fieldname)
                    self.fields[fieldname] = {}
                    self.fields[fieldname][LENGTH] = fieldlength
                    self.fields[fieldname][START] = fieldstart
                    self.fields[fieldname][TYPE] = ftype
                fieldstart += fieldlength
                fielddef = self._object.read(32)
                terminator = fielddef[0]
            self.record_number = None
            self.record_select = None
            self.record_control = None
            self.fieldnames = tuple(fieldnames)
            fieldnames.sort()
            self.sortedfieldnames = tuple(fieldnames)
        except:
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
        self.record_data = None # r bytes the most recent _get_record() read
        self.file_header = [] # 1 header + n field definitions each 32 bytes
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
        self.record_data = self._object.read(self.record_length)
        self.record_control = self.record_data[0]
        if self.record_control in _PRESENT:
            result = {}
            for fieldname in self.fieldnames:
                s = self.fields[fieldname][START]
                f = self.fields[fieldname][START] + self.fields[fieldname][LENGTH]
                result[fieldname] = self.record_data[s:f].strip()
            return result
        else:
            return None

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
        """Return base 256 string converted to integer.

        Least significant digit at left as in dbaseIII record count.

        """
        result = 0
        for i in range(len(number),0,-1):
            result = 256 * result + ord(number[i - 1])
        return result


class CursordBaseIII(object):
    
    """Define a dBase III file cursor

    Wrap the dBaseIII methods in corresponding cursor method names.
    
    Methods added:

    __del__
    close - close text file
    first
    is_cursor_open
    last
    next
    prev
    setat
    
    Methods overridden:

    __init__ - define a dBaseIII file cursor

    Methods extended:

    None
    
    """

    def __init__(self, dbobject):
        
        if isinstance(dbobject, dBaseIII):
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

    def is_cursor_open(self):
        """Return True if cursor available for use and False otherwise."""
        return self._object is not None

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


class _dBaseapiRoot(object):
    
    """Provide file level access to a dBaseIII file.

    This class containing methods to open and close dBase files.
    Record level access is the responsibility of subclasses.
    
    Methods added:

    __del__
    close - close dBaseIII file
    is_field_primary
    open_root
    
    Methods overridden:

    __init__

    Methods extended:

    None
    
    """

    def __init__(self, dd, fname, dptdesc):
        """Define a dBaseIII file.
        
        dd = file description name
        fname = path to data file (.dbf) for dd
        dptdesc = field description for data file
        
        """
        self._ddname = dd
        self._fields = None
        self._file = fname
        self._primary = None
        self._secondary = None
        self._dbaseobject = None

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
            raise dBaseapiError, msg

        sequence = dict()
        for fieldname in fields:
            if not isinstance(fieldname, str):
                msg = ' '.join(['Field name must be string not',
                                repr(fieldname),
                                'in file', dd,])
                raise dBaseapiError, msg
            
            if not fieldname.isupper():
                msg = ' '.join(['Field name', fieldname,
                                'in file', dd,
                                'must be upper case'])
                raise dBaseapiError, msg

            attributes = fields[fieldname]
            if attributes == None:
                attributes = dict()
                fields[fieldname] = attributes
            if not isinstance(attributes, dict):
                msg = ' '.join(['Attributes for field', fieldname,
                                'in file', repr(dd),
                                'must be a dictionary or "None"'])
                raise dBaseapiError, msg
            
            for a in attributes:
                if a not in DBASE_FIELDATTS:
                    msg = ' '.join(['Attribute', repr(a),
                                    'for field', fieldname,
                                    'in file', dd,
                                    'is not allowed'])
                    raise dBaseapiError, msg
                
                if type(attributes[a]) != DBASE_FIELDATTS[a]:
                    msg = ' '.join([a,
                                    'for field', fieldname,
                                    'in file', dd,
                                    'is wrong type'])
                    raise dBaseapiError, msg

                if a == TYPE:
                    if attributes[a] not in _FIELDTYPE:
                        msg = ' '.join(['Type for field', fieldname,
                                        'in file', dd,
                                        'must be one of',
                                        str(_FIELDTYPE.keys())])
                        raise dBaseapiError, msg

            if START in attributes:
                if attributes[START] in sequence:
                    msg = ' '.join(['Field', fieldname,
                                    'in file', dd,
                                    'starts at', str(attributes[START]),
                                    'duplicating field',
                                    sequence[attibutes[start]],
                                    'start'])
                    raise dBaseapiError, msg

                sequence[attributes[START]] = fieldname

        sequence = sequence.items()
        sequence.sort()
        while len(sequence):
            s, f = sequence.pop()
            if len(sequence):
                sp, fp = sequence[-1]
                if LENGTH in fields[fp]:
                    if sp + fields[fp][LENGTH] > s:
                        msg = ' '.join(['Field', fp,
                                        'starting at', str(sp),
                                        'length', str(fields[fp][LENGTH]),
                                        'overlaps field', f,
                                        'starting at', str(s),
                                        'in file', dd])
                        raise dBaseapiError, msg
                
        primary = dptdesc.get(PRIMARY, dict())
        if not isinstance(primary, dict):
            msg = ' '.join(['Field mapping of file', repr(dd),
                            'must be a dictionary'])
            raise dBaseapiError, msg

        for p in primary:
            if not isinstance(p, str):
                msg = ' '.join(['Primary field name', str(p),
                                'for', dd,
                                'must be a string'])
                raise dBaseapiError, msg

            f = primary[p]
            if f == None:
                f = p.upper()
                primary[p] = f
            elif not isinstance(f, str):
                msg = ' '.join(['Field', str(f),
                                'for primary field name', p,
                                'in file', dd,
                                'must be a string'])
                raise dBaseapiError, msg

            if f not in fields:
                msg = ' '.join(['Field', f,
                                'for primary field name', p,
                                'in file', dd,
                                'must have a field description'])
                raise dBaseapiError, msg

        secondary = dptdesc.get(SECONDARY, dict())
        if not isinstance(secondary, dict):
            msg = ' '.join(['Index definition of file', repr(dd),
                            'must be a dictionary'])
            raise dBaseapiError, msg
        
        for s in secondary:
            if not isinstance(s, str):
                msg = ' '.join(['Index name', str(s),
                                'for', dd,
                                'must be a string'])
                raise dBaseapiError, msg

            i = secondary[s]
            if i == None:
                i = (s.upper(),)
                secondary[s] = i
            elif not isinstance(i, tuple):
                msg = ' '.join(['Index definition', str(i),
                                'in field', s,
                                'in file', dd,
                                'must be a tuple of strings'])
                raise dBaseapiError, msg

            for f in i:
                if not isinstance(f, str):
                    msg = ' '.join(['Field name', str(f),
                                    'in index definition for', s,
                                    'in file', dd,
                                    'must be a string'])
                    raise dBaseapiError, msg

                if f not in fields:
                    msg = ' '.join(['Field', f,
                                    'for index definition', s,
                                    'in file', dd,
                                    'must have a field description'])
                    raise dBaseapiError, msg

        self._fields = fields
        self._primary = primary
        self._secondary = secondary

    def close(self):
        """Close file."""
        try:
            self._dbaseobject.close()
        except:
            pass
        self._dbaseobject = None

    def is_field_primary(self, dbfield):
        """Return true if field is primary (not secondary test used)."""
        return dbfield not in self._secondary

    def open_root(self):
        """Open DBaseIII file."""
        if self._dbaseobject == True:
            opendb = dBaseIII(self._file)
            opendb.open_dbf()
            for f in self._fields:
                if f not in opendb.fields:
                    raise dBaseapiError, ' '.join((
                        'Field', f, 'not in file', self._ddname))
                else:
                    for a in self._fields[f]:
                        if self._fields[f][a] != opendb.fields[f][a]:
                            raise dBaseapiError, ' '.join((
                                'Declared field attribute',
                                a,
                                'for field',
                                f,
                                'does not match value on file',
                                self._ddname))
            for f in opendb.fields:
                if f not in self._fields:
                    self._primary[f] = f
                    self._fields[f] = dict()
                for a in opendb.fields[f]:
                    if a not in self._fields[f]:
                        self._fields[f][a] = opendb.fields[f][a]
            self._dbaseobject = opendb
        elif self._dbaseobject == False:
            raise dBaseapiError, 'Create dBase file not supported'
        return True
            
            
class dBaseapiRoot(_dBaseapiRoot):

    """Provide record level access to a dBaseIII file.

    Methods added:

    make_cursor
    _get_deferable_update_files
    get_first_primary_key_for_index_key
    get_primary_record
    
    Methods overridden:

    None

    Methods extended:

    __init__
    close - close dBaseIII file
    open_root
    
    """

    def __init__(self, dd, fname, dptdesc, sfi):
        """Define a dBaseIII file.
        
        See base class for argument descriptions.
        sfi - for compatibility with bsddb
        
        """
        super(dBaseapiRoot, self).__init__(dd, fname, dptdesc)
        
        # All active CursordBase objects opened by make_cursor
        self._cursors = dict()

    def close(self):
        """Close file and cursors."""
        for c in self._cursors:
            c.close()
        self._cursors.clear()

        super(dBaseapiRoot, self).close()
        

    def get_database(self):
        """Return the open file."""
        return self._dbaseobject

    def make_cursor(self, indexname, keyrange=None):
        """Create a cursor on the dBaseIII file."""
        if indexname not in self._secondary:
            #c = self._dbaseobject.Cursor()
            c = CursordBase(self._dbaseobject, keyrange)
            if c:
                self._cursors[c] = True
            return c
        else:
            raise dBaseapiError, 'Indexes not supported'

    def _get_deferable_update_files(self, defer, dd):
        """Return a dictionary of empty lists for the dBaseIII files.

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
        """Open dBaseIII file."""
        pathname = self._file
        foldername, filename = os.path.split(pathname)
        if os.path.exists(foldername):
            if not os.path.isdir(foldername):
                msg = ' '.join([foldername, 'exists but is not a folder'])
                raise dBaseapiError, msg
            
        else:
            os.makedirs(foldername)
        if os.path.exists(pathname):
            if not os.path.isfile(pathname):
                msg = ' '.join([pathname, 'exists but is not a file'])
                raise dBaseapiError, msg

            if self._dbaseobject == None:
                self._dbaseobject = True
        elif self._dbaseobject == None:
            self._dbaseobject = False
            
        return super(dBaseapiRoot, self).open_root()
            

class CursordBase(CursordBaseIII, Cursor):
    
    """Define a dBaseIII cursor.
    
    Clearly not finished.  So notes left as found.

    A cursor implemented using a CursordBaseIII cursor for access in
    record number order. Index access is not supported.
    This class and its methods support the api.dataclient.DataClient class
    and may not be appropriate in other contexts.
    CursordBase is a subclass of CursordBaseIII at present. The methods
    of CursordBaseIII are named to support DataClient directly but
    set_partial_key is absent. May be better to follow CursorDB and
    CursorDPT classes and make the CursordBaseIII instance an attibute
    of CursordBase. dBaseIII.Cursor() supports this.
    
    Methods added:

    None
    
    Methods overridden:

    database_cursor_exists
    set_partial_key

    Methods extended:

    __init__
    
    """

    def __init__(self, dbasedb, keyrange=None):
        
        super(CursordBase, self).__init__(dbobject=dbasedb)

    def database_cursor_exists(self):
        """Return True if database cursor exists and False otherwise"""
        return self.is_cursor_open()

    def set_partial_key(self, partial):
        """Do nothing.  Partial key not relevant."""
        pass

        
