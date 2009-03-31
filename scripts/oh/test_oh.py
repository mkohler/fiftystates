import unittest

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

    def test_make_url_lower_chamber(self):
        self.assertEqual(get_legislation.make_url(122, 'lower', 1),
        'http://www.legislature.state.oh.us/bills.cfm?ID=122_HB_1')

        self.assertEqual(get_legislation.make_url(124, 'lower', 99),
        'http://www.legislature.state.oh.us/bills.cfm?ID=124_HB_99')

        self.assertEqual(get_legislation.make_url(128, 'lower', 100),
        'http://www.legislature.state.oh.us/bills.cfm?ID=128_HB_100')

    def test_make_url_upper_chamber(self):
        self.assertEqual(get_legislation.make_url(122, 'upper', 5),
        'http://www.legislature.state.oh.us/bills.cfm?ID=122_SB_5')

        self.assertEqual(get_legislation.make_url(123, 'upper', 42),
        'http://www.legislature.state.oh.us/bills.cfm?ID=123_SB_42')

# Run from top-level fiftystates directory. 
if __name__ == '__main__':
    unittest.main()
