#!/usr/bin/env python

import urllib
from BeautifulSoup import BeautifulSoup
import logging

# ugly hack
import sys
sys.path.append('./scripts/pyutils')
import legislation

logging.basicConfig(level=logging.DEBUG)

class OHLegislationScraper(legislation.LegislationScraper):
    state = 'oh'

    # Called by LegislationScraper base class.
    #   chamber is either 'lower' or 'upper'.
    def scrape_bills(self, chamber, year):
        self.scrape_session(chamber, year_to_session(year))

    def scrape_session(self, chamber, session):
        logging.info('Scraping session %s %s' % (session, chamber))
        while True:
            bill_number = 1
            url = make_url(chamber, session, bill_number)
            bill_html = urllib.urlopen(url).read()
            logging.debug(bill_html)


def parse_bill(session, chamber, bill_number, bill_html):
    bill_soup = BeautifulSoup(bill_html)

    # XXX 
    #
    # self.add_bill(chamber, session, bill_id, bill_title)

    # XXX
    # self.add_bill_version(chamber, session, bill_id, version_name,
    # version_url)

    # XXX
    # self.add_sponsorship(chamber, session, bill_id, 'primary', leg)

    # XXX 
    # self.add_sponsorship(chamber, session, bill_id, 'cosponsor', leg)

    # XXX
    # self.add_action(chamber, session, bill_id, action_chamber, action,
    # date)


def make_url(session, chamber, bill_number):
    if chamber == 'upper':
        return ('http://www.legislature.state.oh.us/' +
                 'bills.cfm?ID=%s_SB_%s' % (session, bill_number))
    else:
        return ( 'http://www.legislature.state.oh.us/' +
                 'bills.cfm?ID=%s_HB_%s' % (session, bill_number))

def year_to_session(year):
    # As defined on:
    # http://www.legislature.state.oh.us/search.cfm
    session_dates = { 128: (2009, 2010),
                      127: (2007, 2008),
                      126: (2005, 2006),
                      125: (2003, 2004),
                      124: (2001, 2002),
                      123: (1999, 2000),
                      122: (1997, 1998)}

    for session, years in session_dates.iteritems():
        if year in years:
            return session
    raise legislation.NoDataForYear(year)

if __name__ == '__main__':
    logging.debug('Starting OHLegislationsScraper')
    OHLegislationScraper().run()
