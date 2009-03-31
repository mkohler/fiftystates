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

    def get_bill_info(self, session, bill_id):
        logging.info('get_bill_info')
        return

        bill_detail_url = 'http://www.legislature.state.oh.us/BillText128/128_SB_1_PS_Y.html'

        # parse the bill data page, finding the latest html text
        if bill_id[0] == 'H':
            chamber = 'lower'
        else:
            chamber = 'upper'

        bill_data = urllib.urlopen(bill_detail_url).read()
        bill_soup = BeautifulSoup(bill_data)

        # XXX 
        #
        # self.add_bill(chamber, session, bill_id, bill_title)

        # XXX
        # self.add_bill_version(chamber, session, bill_id, version_name, version_url)

        # XXX
        # self.add_sponsorship(chamber, session, bill_id, 'primary', leg)

        # XXX 
        # self.add_sponsorship(chamber, session, bill_id, 'cosponsor', leg)

        # XXX
        #self.add_action(chamber, session, bill_id, action_chamber, action, date)

    def scrape_session(self, chamber, session):
        logging.info('scrape_session')
        return

        url = 'http://www.ncga.state.nc.us/gascripts/SimpleBillInquiry/displaybills.pl?Session=%s&tab=Chamber&Chamber=%s' % (session, chamber)
        data = urllib.urlopen(url).read()
        bill_ids = get_bills_from_session(data)

        for bill_id in bill_ids:
            self.get_bill_info(session, bill_id)

    # Called by LegislationScraper base class.
    def scrape_bills(self, chamber, year):
        logging.info('scrape_bills')
        year_mapping = {
            '2009': ('2008','2009'),
        }
        chamber = {'lower':'House', 'upper':'Senate'}[chamber]

        if year not in year_mapping:
            raise legislation.NoDataForYear(year)
	
        for session in year_mapping[year]:
            self.scrape_session(chamber, session)

def get_bills_from_session(session_html):
    soup = BeautifulSoup(session_html)
    rows = soup.findAll('table')[5].findAll('tr')[1:]
    bill_ids = []
    for row in rows:
        td = row.find('td')
        bill_id = td.a.contents[0]
        bill_ids.append(bill_id)
    return bill_ids

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
