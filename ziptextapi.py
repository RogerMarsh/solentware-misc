# ziptextapi.py
# Copyright 2008 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Provide bsddb style access to a database of zip compressed text files.

List of classes

ZipTextapi
ZipTextapiRoot

"""

import textapi
import zipfile


class ZipTextapi(textapi.Textapi):
    
    """Define a textdb database structure for a zip compressed file.
    
    See superclass for description.
    
    Methods added:

    None
    
    Methods overridden:

    make_root

    Methods extended:

    None
    
    """

    def make_root(self, filename):
        """Return a ZipTextapiRoot instance for filename"""
        return ZipTextapiRoot(filename)


class ZipTextapiRoot(textapi.TextapiRoot):
    
    """Define a zip compressed text file.
    
    See superclass for description.
    
    Methods added:

    None
    
    Methods overridden:

    open_root

    Methods extended:

    None
    
    """
    
    def open_root(self):
        """Open a zip compressed text file and read all lines"""
        try:
            self._object = zipfile.ZipFile(self.filename, 'r')
            #open method added at Python 2.6
            '''self.textlines = [
                t for t in self._object.open(self._object.infolist()[0])]'''
            #should use csv.reader to cope with '\n' as data in csv files
            self.textlines = self._object.read(
                self._object.namelist()[0]).split('\n')
            self.record_count = len(self.textlines)
            self.record_number = None
            self.record_select = None
        except:
            self._object = None

