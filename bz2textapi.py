# bz2textapi.py
# Copyright 2008 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Provide bsddb style access to a database of bz2 compressed text files.

List of classes

BZ2Textapi
BZ2TextapiRoot

"""

import textapi
import bz2


class BZ2Textapi(textapi.Textapi):
    
    """Define a textdb database structure for a bz2 compressed file.
    
    See superclass for description.
    
    Methods added:

    None
    
    Methods overridden:

    make_root

    Methods extended:

    None
    
    """

    def make_root(self, filename):
        """Return a BZ2TextapiRoot instance for filename"""
        return BZ2TextapiRoot(filename)


class BZ2TextapiRoot(textapi.TextapiRoot):
    
    """Define a bz2 compressed text file.
    
    See superclass for description.
    
    Methods added:

    None
    
    Methods overridden:

    open_root

    Methods extended:

    None
    
    """
    
    def open_root(self):
        """Open a bz2 compressed text file and read all lines"""
        try:
            self._object = bz2.BZ2File(self.filename, 'rb')
            self.textlines = self._object.read().splitlines()
            self.record_count = len(self.textlines)
            self.record_number = None
            self.record_select = None
        except:
            self._object = None

