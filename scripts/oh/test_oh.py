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


# Run from top-level fiftystates directory. 
if __name__ == '__main__':
    unittest.main()
