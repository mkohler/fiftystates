import unittest

import get_legislation



class TestNC(unittest.TestCase):
    def test_2009_upper(self):
        upper_html = open('scripts/nc/test_2009_upper.html').read()
        bill_ids = get_legislation.get_bills_from_session(upper_html)
        for count in range(1, 1093 + 1):
            self.assert_(u'S%s' % count in bill_ids)

    def test_2009_lower(self):
        lower_html = open('scripts/nc/test_2009_lower.html').read()
        bill_ids = get_legislation.get_bills_from_session(lower_html)
        for count in range(1, 868 + 1):
            self.assert_(u'H%s' % count in bill_ids)


# Run from top-level fiftystates directory. 
if __name__ == '__main__':
    unittest.main()
