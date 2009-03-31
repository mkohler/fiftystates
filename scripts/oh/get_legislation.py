#!/usr/bin/env python

import os
import urllib
import logging
import time
from BeautifulSoup import BeautifulSoup

# ugly hack
import sys
sys.path.append('./scripts/pyutils')
import legislation

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s-%(message)s')

# ToDo
#
#  Find a way to actually filter down the bills by year.
#  Terminate the session year.
class OhioBill(object):
    def __init__(self, chamber, year, session, number):
        self.chamber = chamber
        self.year = year
        self.session = session
        self.number = number
        self.filename = self.make_filename()
        self.id = self.make_id()
        self.url = self.make_url_clean_html()
        self.name = None
        self.version_name = None
        self.text = None

    def has_bill_text(self):
        if not self.text:
            return False
        if 'could not be found' in self.text:
            return False
        if 'You have requested a page that does not exist' in self.text:
            return False
        if 'Bad Request' in self.text:
            return False
        return True

    def make_id(self):
        if self.chamber == 'lower':
            id = 'HB %s' % self.number
        else:
            id = 'SB %s' % self.number
        return id

    def make_filename(self):
        return 'data/oh/%s_%s_%s.html' % (self.session, self.chamber,
                                          self.number)

    def make_url_clean_html(self):
        if self.chamber == 'lower':
            id = 'HB_%s' % self.number
        else:
            id = 'SB_%s' % self.number

        return ('http://www.legislature.state.oh.us/' +
                'BillText%s/%s_%s_1_N.html' %
                (self.session, self.session, self.id))

    def make_url_with_framing(self):
        if self.chamber == 'lower':
            return ( 'http://www.legislature.state.oh.us/' +
                     'bills.cfm?ID=%s_HB_%s' % (self.session, self.number))
        else:
            return ('http://www.legislature.state.oh.us/' +
                     'bills.cfm?ID=%s_SB_%s' % (self.session, self.number))

    def parse_bill(self):
        soup = BeautifulSoup(self.text)

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


    #
    # For some bills, we can get the full text in a clean HTML format. We
    # try that approach first, but if it fails, we fall back to getting the
    # text along with the headers and menus.
    #
    def retrieve_bill_text(self):
        self.text = urllib.urlopen(self.url).read()

        if self.has_bill_text():
            logging.info('Retrieved %s' % self.url)
            return
        else:
            # For many bills, this is an expected failure.
            logging.debug('%s failed' % self.url)

        self.url = self.make_url_with_framing()
        logging.info('Retrieved %s' % self.url)
        self.text = urllib.urlopen(self.url).read()
        if self.has_bill_text():
            return

        logging.warn('Could not find bill: chamber %s, year %s, number %s'
                     % (self.chamber, self.year, self.number))
        raise legislation.NoDataForYear(self.year)

    def save_bill_text_as_file(self):
        f = open(self.filename, 'w')
        assert(self.text != None)
        f.write(self.text)
        f.close()


class OHLegislationScraper(legislation.LegislationScraper):
    state = 'oh'

    # Called by LegislationScraper base class.
    #   chamber is either 'lower' or 'upper'.
    def scrape_bills(self, chamber, year):
        self.scrape_session(year, chamber, year_to_session(year))

    def scrape_session(self, year, chamber, session):
        logging.info('Scraping session %s %s house' % (session, chamber))
        bill_number = 1
        while True:
            bill = OhioBill(chamber, year, session, bill_number)

            # If we don't have the bill, go get it and save it.
            if not os.path.isfile(bill.filename):
                try:
                    bill.retrieve_bill_text()
                except legislation.NoDataForYear:
                    break
                bill.save_bill_text_as_file()
                time.sleep(1)            # Give the poor web server a break.
            else:
                logging.info('Already have bill %s %s %s' %
                             (chamber, year, bill_number))

            bill_number += 1




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
