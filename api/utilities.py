# utilities.py
# Copyright 2009 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Various utilities.

List of classes:

AppSysDate - Date parsing functions
AppSysPersonName - Pick out surname and forenames from a name
AppSysPersonNameParts - Generate partial names from an AppSysPersonName

"""

import re
import datetime
import calendar

# AppSysPersonName constants
NSPACE = ' '
NCOMMA = ','
NDOT = '.'
NHYPHEN = '-'
NAMEDELIMITER = ''.join((NSPACE, NCOMMA, NDOT))
NAMEHYPHENED = ''.join((NHYPHEN,))


class AppSysDate(object):
    
    """Date parser that accepts various common formats.

    wx.DateTime was used to do these things prior to switch to Tkinter.
    But this class is not an emulation.

    Methods added:

    iso_format_date
    get_current_year
    get_month_name
    length_date_string
    parse_date

    Methods overridden:

    __init__
    
    Methods extended:

    None
    
    """

    ymd_re = re.compile(''.join((
        '(\s*)',
        '([0-9]+|[a-zA-Z]+)',
        '(\s+|.|/|-)',
        '([0-9]+|[a-zA-Z]+)',
        '(\s+|.|/|-)',
        '([0-9]+)',
        '(\s+.*|\Z)')))
    md_re = re.compile(''.join((
        '(\s*)',
        '([0-9]+|[a-zA-Z]+)',
        '(\s+|.|/|-)',
        '([0-9]+|[a-zA-Z]+)',
        '(\s+.*|\Z)')))
    
    date_formats = (
        '%d %b %Y', # 30 Nov 2006
        '%b %d %Y', # Nov 30 2006
        '%d %B %Y', # 30 November 2006
        '%B %d %Y', # November 30 2006
        '%d %b %y', # 30 Nov 06
        '%b %d %y', # Nov 30 06
        '%d %B %y', # 30 November 06
        '%B %d %y', # November 30 06
        '%d.%m.%Y', # 30.11.2006
        '%d.%m.%y', # 30.11.06
        '%m.%d.%Y', # 11.30.2006
        '%m.%d.%y', # 11.30.06
        '%Y-%m-%d', # 2006-11-30
        '%y-%m-%d', # 06-11-30
        '%d/%m/%Y', # 30/11/2006
        '%d/%m/%y', # 30/11/06
        '%m/%d/%Y', # 11/30/2006
        '%m/%d/%y', # 11/30/06
        )

    calendar = calendar

    def __init__(self):

        self.date = None
        self.re_match = None

    def iso_format_date(self):
        """Return ISO format date like 2007-08-26"""
        try:
            return self.date.isoformat(' ').split()[0]
        except AttributeError:
            return None

    def get_current_year(self):
        """Return current year"""
        return datetime.datetime.now().year

    def get_month_name(self, month):
        """Return abbreviated month name.

        Month is in range 0-11 following wx.DateTime convention.

        """
        if month > 11:
            month = -1
        elif month < 0:
            month = -1
        return self.calendar.month_abbr[month + 1]

    def length_date_string(self):
        """Return number of characters interpreted as date by parse_date"""
        if self.re_match is not None:
            groups = self.re_match.groups()
            if len(groups) > 5:
                return len(''.join(groups[:6]))
            else:
                return len(''.join(groups[:4]))

        return -1

    def parse_date(self, date):
        """Return valid date at start of date argument.

        wx.DateTime.ParseDate returns -1 for conversion failure rather than
        None as might be expected from documentation (which says NULL). So
        do this as existing callers expect it.

        """
        self.re_match = self.ymd_re.match(date)
        if self.re_match is None:
            self.re_match = self.md_re.match(date)
            if self.re_match is None:
                self.date = None
                return -1

        groups = self.re_match.groups()
        if len(groups) > 5:
            datestring = ''.join(groups[1:6])
        else:
            datestring = ''.join((
                ''.join((groups[1:4])),
                groups[1],
                str(datetime.datetime.now().year)))

        for f in self.date_formats:
            try:
                self.date = datetime.datetime.strptime(datestring, f)
                return self.length_date_string()
            except ValueError:
                pass

        return -1


class AppSysPersonName(object):
    
    """Name parser that picks out surname and forenames.

    The text before the first comma in a name is the surname.  Without a comma
    a word longer than one character is chosen in order from: last word in name;
    first word in name; latest word in name.  If all words are one character
    the last word is the surname.

    Words are delimited by space comma and dot.

    Methods added:

    None

    Methods overridden:

    __init__
    
    Methods extended:

    None
    
    """

    def __init__(self, name):
        self._name = name
        self.name = None
        self.surname = ''
        self.forenames = None
        partialnames = []
        commasplit = name.split(NCOMMA, 1)
        if len(commasplit) > 1:
            s, name = commasplit
            self.surname = NSPACE.join(s.split())
        partial = []
        for n in name:
            if n in NAMEDELIMITER:
                partialnames.append(''.join(partial))
                partial = []
            else:
                partial.append(n)
        if partial:
            partialnames.append(''.join(partial))
        partialnames = NSPACE.join(partialnames).split()
        if partialnames and not self.surname:
            surname = partialnames.pop()
            if len(surname) < 2:
                partialnames.append(surname)
                surname = partialnames.pop(0)
                if len(surname) < 2:
                    partialnames.insert(0, surname)
                    x = -1
                    for e, p in enumerate(partialnames):
                        if len(p) > 1:
                            x = e
                    surname = partialnames.pop(x)
            self.surname = surname
        self.forenames = NSPACE.join(partialnames)
        self.name = NSPACE.join((self.surname, self.forenames))


class AppSysPersonNameParts(AppSysPersonName):
    
    """Name parser that picks out surname forenames and all partial names.

    The superclass picks out surname and forenames.

    The surname becomes a partial name.  The words formed by splitting surname
    and forenames at whitespace become partial names and these words split by
    hyphens become partial names.

    Methods added:

    None

    Methods overridden:

    None
    
    Methods extended:

    __init__
    
    """

    def __init__(self, name):
        super(AppSysPersonNameParts, self).__init__(name)
        partialnames = self.name.split()
        self.partialnames = set(partialnames)
        self.partialnames.add(self.surname)
        for nh in NAMEHYPHENED:
            if name.find(nh) > -1:
                for pn in partialnames:
                    partial = []
                    for n in pn:
                        if n in NAMEHYPHENED:
                            self.partialnames.add(''.join(partial))
                            partial = []
                        else:
                            partial.append(n)
                    if partial:
                        self.partialnames.add(''.join(partial))
                break

