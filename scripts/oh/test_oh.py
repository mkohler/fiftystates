import unittest

import get_legislation



class TestOH(unittest.TestCase):
    def test_year_to_session(self):
        self.assertEqual(get_legislation.year_to_session(2009), 128)
        self.assertEqual(get_legislation.year_to_session(2008), 127)
        self.assertEqual(get_legislation.year_to_session(2007), 127)
        self.assertEqual(get_legislation.year_to_session(1998), 122)
        self.assertEqual(get_legislation.year_to_session(1997), 122)




# Run from top-level fiftystates directory. 
if __name__ == '__main__':
    unittest.main()
