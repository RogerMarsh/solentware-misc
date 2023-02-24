# test_utilities.py
# Copyright 2012 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""utilities tests"""

import unittest
import datetime

from .. import utilities

MSG = "Failure of this test invalidates all other tests"


class AppSysDate(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_ymd_re(self):
        ae = self.assertEqual
        ane = self.assertNotEqual
        ymdre = utilities.AppSysDate.ymd_re
        ae(
            ymdre.pattern,
            "".join(
                (
                    r"(\s*)",
                    "([0-9]+|[a-zA-Z]+)",
                    r"(\s+|\.|/|-)",
                    "([0-9]+|[a-zA-Z]+)",
                    r"(\s+|\.|/|-)",
                    "([0-9]+)",
                    r"(\s+.*|\Z)",
                )
            ),
            msg=MSG,
        )

        # accepted
        ane(ymdre.match("30 Nov 2006"), None)
        ane(ymdre.match("30.aNov 2006"), None)
        ane(ymdre.match("30/aNov 2006"), None)
        ane(ymdre.match("30 Nova.2006"), None)
        ane(ymdre.match("30 Nova/2006"), None)
        ane(ymdre.match("30 Nov 2006 string"), None)
        ane(ymdre.match("30 Nov 2006  string"), None)

        # rejected
        ae(ymdre.match("30aNov 2006"), None)
        ae(ymdre.match("30 Nova2006"), None)
        ae(ymdre.match("30aNov 2006"), None)
        ae(ymdre.match("30 Nov 2006string"), None)

    def test_md_re(self):
        ae = self.assertEqual
        ane = self.assertNotEqual
        mdre = utilities.AppSysDate.md_re
        ae(
            mdre.pattern,
            "".join(
                (
                    r"(\s*)",
                    "([0-9]+|[a-zA-Z]+)",
                    r"(\s+|\.|/|-)",
                    "([0-9]+|[a-zA-Z]+)",
                    r"(\s+.*|\Z)",
                )
            ),
            msg=MSG,
        )

        # accepted
        ane(mdre.match("30 Nov 2006"), None)
        ane(mdre.match("30.aNov 2006"), None)
        ane(mdre.match("30/aNov 2006"), None)
        ane(mdre.match("30 Nov 2006string"), None)
        ane(mdre.match("30 Nov 2006 string"), None)
        ane(mdre.match("30 Nov 2006  string"), None)
        ane(mdre.match("30 Nov aa2006  string"), None)

        # rejected
        ae(mdre.match("30aNov 2006"), None)
        ae(mdre.match("30 Nova2006"), None)
        ae(mdre.match("30 Nova.2006"), None)
        ae(mdre.match("30 Nova/2006"), None)
        ae(mdre.match("30aNov 2006"), None)

    def test_date_formats(self):
        ae = self.assertEqual
        ae(
            utilities.AppSysDate.date_formats,
            (
                "%d %b %Y",  # 30 Nov 2006
                "%b %d %Y",  # Nov 30 2006
                "%d %B %Y",  # 30 November 2006
                "%B %d %Y",  # November 30 2006
                "%d %b %y",  # 30 Nov 06
                "%b %d %y",  # Nov 30 06
                "%d %B %y",  # 30 November 06
                "%B %d %y",  # November 30 06
                "%d.%m.%Y",  # 30.11.2006
                "%d.%m.%y",  # 30.11.06
                "%m.%d.%Y",  # 11.30.2006
                "%m.%d.%y",  # 11.30.06
                "%Y-%m-%d",  # 2006-11-30
                "%Y/%m/%d",  # 2006/11/30
                "%y-%m-%d",  # 06-11-30
                "%d/%m/%Y",  # 30/11/2006
                "%d/%m/%y",  # 30/11/06
                "%m/%d/%Y",  # 11/30/2006
                "%m/%d/%y",  # 11/30/06
            ),
            msg=MSG,
        )

    def test___init__(self):
        ae = self.assertEqual
        asd = utilities.AppSysDate()
        ae(asd.date, None)
        ae(asd.re_match, None)
        ae(asd._bytes_input, None)
        ae(len(asd.__dict__), 3)

    def test_iso_format_date(self):
        ae = self.assertEqual
        asd = utilities.AppSysDate()
        asd.date = datetime.datetime(2016, 11, 21, 19, 35)
        ae(asd.iso_format_date(), "2016-11-21")
        asd._bytes_input = True
        ae(asd.iso_format_date(), b"2016-11-21")
        asd.date = None
        ae(asd.iso_format_date(), None)
        asd.date = "not a datetime"
        ae(asd.iso_format_date(), None)

    def test_iso_format_date(self):
        ae = self.assertEqual
        asd = utilities.AppSysDate()
        ae(
            asd.get_current_year(),
            datetime.datetime.now().year,
            msg="".join(
                (
                    "\nWas this test run between 23:59 and 00:01 ",
                    "on New Year's Eve?",
                )
            ),
        )

    def test_get_month_name(self):
        ae = self.assertEqual
        asd = utilities.AppSysDate()
        ae(asd.get_month_name(12), "")
        ae(asd.get_month_name(-1), "")
        ae(asd.get_month_name(0), "Jan")
        for e, m in enumerate(
            (
                "Jan",
                "Feb",
                "Mar",
                "Apr",
                "May",
                "Jun",
                "Jul",
                "Aug",
                "Sep",
                "Oct",
                "Nov",
                "Dec",
            )
        ):
            ae(asd.get_month_name(e), m)

    def test_length_date_string_01(self):
        ae = self.assertEqual
        asd = utilities.AppSysDate()
        s = "  21 Nov 2015 " + chr(156)
        asd.parse_date(s)
        ae(asd.length_date_string(), 13)
        s = chr(155) + "  21 Nov 2015 " + chr(156)
        asd.parse_date(s)
        ae(asd.length_date_string(), -1)

    def test_length_date_string_02(self):
        ae = self.assertEqual
        asd = utilities.AppSysDate()
        s = b"  21 Nov 2015 " + chr(156).encode()
        asd.parse_date(s)
        ae(asd.length_date_string(), 13)
        s = chr(155).encode() + b"  21 Nov 2015 " + chr(156).encode()
        asd.parse_date(s)
        ae(asd.length_date_string(), -1)

    def test_parse_date_01(self):
        ae = self.assertEqual
        asd = utilities.AppSysDate()
        ae(asd.parse_date(b"abc"), -1)
        ae(asd.parse_date(b"21 Nov"), -1)
        ae(asd.parse_date(b"21 Nov", assume_current_year=True), 6)
        ae(asd.parse_date(b"21 Nov 2016"), 11)
        ae(asd.parse_date(b" 21 Nov 2016"), 12)
        ae(asd.parse_date(b" 21 Nov 2016 more text"), 12)

    def test_parse_date_02(self):
        ae = self.assertEqual
        asd = utilities.AppSysDate()
        ae(asd.parse_date("abc"), -1)
        ae(asd.parse_date("21 Nov"), -1)
        ae(asd.parse_date("21 Nov", assume_current_year=True), 6)
        ae(asd.parse_date("21 Nov 2016"), 11)
        ae(asd.parse_date(" 21 Nov 2016"), 12)
        ae(asd.parse_date(" 21 Nov 2016 more text"), 12)

    def test_parse_date_03(self):
        ae = self.assertEqual
        asd = utilities.AppSysDate()
        for d in (
            "30 Nov 2006",
            "Nov 30 2006",
            "30 November 2006",
            "November 30 2006",
            "30 Nov 06",
            "Nov 30 06",
            "30 November 06",
            "November 30 06",
            "30.11.2006",
            "30.11.06",
            "11.30.2006",
            "11.30.06",
            "2006-11-30",
            "2006/11/30",
            "06-11-30",
            "30/11/2006",
            "30/11/06",
            "11/30/2006",
            "11/30/06",
        ):
            ae(asd.parse_date(d), len(d))
            ae(asd.iso_format_date(), "2006-11-30")

        # Two of many formats which can be specified but are not accepted.
        ae(asd.parse_date("30-11-2006"), -1)
        ae(asd.parse_date("2016.11.30"), -1)


class AppSysPersonName(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test___init___001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"__init__\(\) missing 1 required positional argument: ",
                    "'name'",
                )
            ),
            utilities.AppSysPersonName,
        )

    def test___init___002(self):
        name = utilities.AppSysPersonName("Name")
        self.assertEqual(name.name, "Name ")
        self.assertEqual(name.surname, "Name")
        self.assertEqual(name.forenames, "")

    def test___init___003(self):
        name = utilities.AppSysPersonName("Name".encode())
        self.assertEqual(name.name, "Name ".encode())
        self.assertEqual(name.surname, "Name".encode())
        self.assertEqual(name.forenames, "".encode())

    def test___init___004(self):
        name = utilities.AppSysPersonName("Surname,Forename")
        self.assertEqual(name.name, "Surname Forename")
        self.assertEqual(name.surname, "Surname")
        self.assertEqual(name.forenames, "Forename")

    def test___init___005(self):
        name = utilities.AppSysPersonName("Surname,Forename".encode())
        self.assertEqual(name.name, "Surname Forename".encode())
        self.assertEqual(name.surname, "Surname".encode())
        self.assertEqual(name.forenames, "Forename".encode())

    def test___init___004(self):
        name = utilities.AppSysPersonName("Surname,Forename")
        self.assertEqual(name.name, "Surname Forename")
        self.assertEqual(name.surname, "Surname")
        self.assertEqual(name.forenames, "Forename")

    def test___init___005(self):
        name = utilities.AppSysPersonName("Surname,Forename".encode())
        self.assertEqual(name.name, "Surname Forename".encode())
        self.assertEqual(name.surname, "Surname".encode())
        self.assertEqual(name.forenames, "Forename".encode())

    def test___init___006(self):
        name = utilities.AppSysPersonName("Fore Name Surname")
        self.assertEqual(name.name, "Surname Fore Name")
        self.assertEqual(name.surname, "Surname")
        self.assertEqual(name.forenames, "Fore Name")

    def test___init___007(self):
        name = utilities.AppSysPersonName("Fore Name Surname".encode())
        self.assertEqual(name.name, "Surname Fore Name".encode())
        self.assertEqual(name.surname, "Surname".encode())
        self.assertEqual(name.forenames, "Fore Name".encode())

    def test___init___008(self):
        name = utilities.AppSysPersonName("Fore Name S")
        self.assertEqual(name.name, "Fore Name S")
        self.assertEqual(name.surname, "Fore")
        self.assertEqual(name.forenames, "Name S")

    def test___init___009(self):
        name = utilities.AppSysPersonName("Fore Name S".encode())
        self.assertEqual(name.name, "Fore Name S".encode())
        self.assertEqual(name.surname, "Fore".encode())
        self.assertEqual(name.forenames, "Name S".encode())

    def test___init___010(self):
        name = utilities.AppSysPersonName("Last-Fore Name S")
        self.assertEqual(name.name, "Last-Fore Name S")
        self.assertEqual(name.surname, "Last-Fore")
        self.assertEqual(name.forenames, "Name S")

    def test___init___011(self):
        name = utilities.AppSysPersonName("Last-Fore Name S".encode())
        self.assertEqual(name.name, "Last-Fore Name S".encode())
        self.assertEqual(name.surname, "Last-Fore".encode())
        self.assertEqual(name.forenames, "Name S".encode())


class AppSysPersonNameParts(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test___init___001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"__init__\(\) missing 1 required positional argument: ",
                    "'name'",
                )
            ),
            utilities.AppSysPersonNameParts,
        )

    def test___init___002(self):
        name = utilities.AppSysPersonNameParts("Last-Fore Name S")
        self.assertEqual(name.name, "Last-Fore Name S")
        self.assertEqual(name.surname, "Last-Fore")
        self.assertEqual(name.forenames, "Name S")
        self.assertEqual(
            name.partialnames, {"Fore", "Last-Fore", "Name", "Last", "S"}
        )

    def test___init___003(self):
        name = utilities.AppSysPersonNameParts("Last-Fore Name S".encode())
        self.assertEqual(name.name, "Last-Fore Name S".encode())
        self.assertEqual(name.surname, "Last-Fore".encode())
        self.assertEqual(name.forenames, "Name S".encode())
        self.assertEqual(
            name.partialnames,
            {
                "Fore".encode(),
                "Last-Fore".encode(),
                "Name".encode(),
                "Last".encode(),
                "S".encode(),
            },
        )

    def test___init___004(self):
        name = utilities.AppSysPersonNameParts("Last- Fore Name S".encode())
        self.assertEqual(name.name, "Last- Fore Name S".encode())
        self.assertEqual(name.surname, "Last-".encode())
        self.assertEqual(name.forenames, "Fore Name S".encode())
        self.assertEqual(
            name.partialnames,
            {
                "Fore".encode(),
                "Last-".encode(),
                "Name".encode(),
                "Last".encode(),
                "S".encode(),
            },
        )

    def test___init___005(self):
        name = utilities.AppSysPersonNameParts("Last -Fore Name S".encode())
        self.assertEqual(name.name, "Last -Fore Name S".encode())
        self.assertEqual(name.surname, "Last".encode())
        self.assertEqual(name.forenames, "-Fore Name S".encode())
        self.assertEqual(
            name.partialnames,
            {
                "-Fore".encode(),
                "Fore".encode(),
                "Last".encode(),
                "Name".encode(),
                "Last".encode(),
                "S".encode(),
            },
        )

    def test___init___006(self):
        name = utilities.AppSysPersonNameParts("Last - Fore Name S".encode())
        self.assertEqual(name.name, "Last - Fore Name S".encode())
        self.assertEqual(name.surname, "Last".encode())
        self.assertEqual(name.forenames, "- Fore Name S".encode())
        self.assertEqual(
            name.partialnames,
            {
                "Fore".encode(),
                "-".encode(),
                "Name".encode(),
                "Last".encode(),
                "S".encode(),
            },
        )

    def test___init___007(self):
        name = utilities.AppSysPersonNameParts("Name S Last-".encode())
        self.assertEqual(name.name, "Last- Name S".encode())
        self.assertEqual(name.surname, "Last-".encode())
        self.assertEqual(name.forenames, "Name S".encode())
        self.assertEqual(
            name.partialnames,
            {
                "Last-".encode(),
                "Name".encode(),
                "Last".encode(),
                "S".encode(),
            },
        )

    def test___init___008(self):
        name = utilities.AppSysPersonNameParts("Michael Fernandez -".encode())
        self.assertEqual(name.name, "Michael Fernandez -".encode())
        self.assertEqual(name.surname, "Michael".encode())
        self.assertEqual(name.forenames, "Fernandez -".encode())
        self.assertEqual(
            name.partialnames,
            {
                "-".encode(),
                "Michael".encode(),
                "Fernandez".encode(),
            },
        )


if __name__ == "__main__":
    runner = unittest.TextTestRunner
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    runner().run(loader(AppSysDate))
    runner().run(loader(AppSysPersonName))
    runner().run(loader(AppSysPersonNameParts))
