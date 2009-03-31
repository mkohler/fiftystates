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


class TestURLTypes(unittest.TestCase):
    def test_clean1_html(self):
        pass
        # XXX
        # Need to find an example of the "clean1" URL type.
        # url = ?
        #html = urllib.urlopen(url).read()
        #self.assert_('division of the court' in html)
        
    def test_clean2_html(self):
        url = ('http://www.legislature.state.oh.us/' +
              'BillText125/125_HB_102_PH_Y.html')
        html = urllib.urlopen(url).read()
        self.assert_('division of the court' in html)

    def test_clean3_html(self):
        url = 'http://www.legislature.state.oh.us/BillText127/127_HB_1_I_N.html'
        html = urllib.urlopen(url).read()
        self.assert_('funding reform plan' in html)




# Run from top-level fiftystates directory. 
if __name__ == '__main__':
    unittest.main()
