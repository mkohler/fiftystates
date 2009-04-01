import unittest
import urllib

import sys
sys.path.append('./scripts/pyutils')
import legislation

import get_legislation

class TestOH(unittest.TestCase):
    def test_year_to_session(self):
        self.assertEqual(get_legislation.year_to_session(2009), 128)
        self.assertEqual(get_legislation.year_to_session(2008), 127)
        self.assertEqual(get_legislation.year_to_session(2007), 127)
        self.assertEqual(get_legislation.year_to_session(1998), 122)
        self.assertEqual(get_legislation.year_to_session(1997), 122)

    def test_year_limits(self):
        self.assertRaises(legislation.NoDataForYear,
                          get_legislation.year_to_session,
                          1996)
        self.assertRaises(legislation.NoDataForYear,
                          get_legislation.year_to_session,
                          0)
        self.assertRaises(legislation.NoDataForYear,
                          get_legislation.year_to_session,
                          0.5)


class TestURLs(unittest.TestCase):
    def test_id(self):
        bill = get_legislation.OhioBill('upper', 2005, 1)
        self.assertEqual('SB 1', bill.id)
        self.assertEqual('SB_1', bill.id_url)
        bill = get_legislation.OhioBill('lower', 2005, 1)
        self.assertEqual('HB 1', bill.id)
        self.assertEqual('HB_1', bill.id_url)

    def test_clean1(self):
        url = ('http://www.legislature.state.oh.us/' +
               'BillText127/127_HB_1_N.html')

        bill = get_legislation.OhioBill('lower', 2008, 1)
        self.assertEqual(url, bill.url)

    def test_clean2(self):
        url = ('http://www.legislature.state.oh.us/' +
               'BillText127/127_HB_1_PHC_N.html')
        bill = get_legislation.OhioBill('lower', 2008, 1)
        bill.url = get_legislation.make_url_2(bill.session, bill.id_url)
        self.assertEqual(url, bill.url)

    def test_clean3(self):
        url = ('http://www.legislature.state.oh.us/' +
              'BillText127/127_HB_1_I_N.html')
        bill = get_legislation.OhioBill('lower', 2008, 1)
        bill.url = get_legislation.make_url_3(bill.session, bill.id_url)
        self.assertEqual(url, bill.url)

    def test_unclean(self):
        url = ('http://www.legislature.state.oh.us/' +
               'bills.cfm?ID=127_HB_1')
        bill = get_legislation.OhioBill('lower', 2008, 1)
        bill.url = get_legislation.make_url_framed(bill.session, bill.id_url)
        self.assertEqual(url, bill.url)





# Run from top-level fiftystates directory. 
if __name__ == '__main__':
    unittest.main()
