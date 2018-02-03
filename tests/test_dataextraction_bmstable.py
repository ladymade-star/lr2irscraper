# -*- coding: utf-8 -*-
import unittest

from lr2irscraper.helper.dataextraction.bmstable import *
from tests.util import resource


class TestDataExtractionBMSTable(unittest.TestCase):
    def test_extract_old_style_bms_table(self):
        insane = extract_bms_table_from_html(resource("insane.html"))
        self.assertEqual(tuple(insane.iloc[0]),
                         ("★1", "星の器～STAR OF ANDROMEDA (ANOTHER)", 15,
                          "<a href='http://bit.ly/eoD0dZ'>ZUN (Arr.sun3)</a>",
                          "<a href=''></a>",
                          ""))

        overjoy = extract_bms_table_from_html(resource("overjoy.html", "utf-8"), is_overjoy=True)
        self.assertEqual(tuple(overjoy.iloc[201]),
                         ("★★5", "FREEDOM DiVE [FOUR DIMENSIONS]", 1031,
                          "<a href='http://manbow.nothing.sh/event/event.cgi"
                          "?action=More_def&num=15&event=50'>MAXBEAT</a>",
                          "<a href='http://airlab.web.fc2.com/'>air</a>",
                          ""))



if __name__ == '__main__':
    unittest.main()