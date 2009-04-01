#!/usr/bin/env python
'''Retrieves Ohio legislation.

python scripts/oh/get_legislation.py [--year YYYY] [--upper] [--lower]

By default, all legislation is retrieved.

Must be run from the top-level fifty states directory.
'''

import logging
import optparse
import os
import time
import urllib
from BeautifulSoup import BeautifulSoup

# ugly hack
import sys
sys.path.append('./scripts/pyutils')
import legislation

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s-%(message)s')

# ToDo
#
#  * Find a way to actually filter down the bills by year.
#
#    The bills are organized by session and each session lasts two years,
#    so if we want to retrieve a single year's worth of bills, we need to
#    get the date of each bill. The way we currently deal with it is that
#    we always scrape a whole session (two years), even if only a single
#    year was requested.
#
#  * Handle year ranges
#

def text_is_a_bill(text):
    if not text:
        return False
    if 'could not be found' in text:
        return False
    if 'You have requested a page that does not exist' in text:
        return False
    if 'Bad Request' in text:
        return False
    return True

#
# The make_url_x routines 
#

def make_url_1(session, id_url):
    return ('http://www.legislature.state.oh.us/' +
            'BillText%s/%s_%s_N.html' %
            (session, session, id_url))

def make_url_2(session, id_url):
    return ('http://www.legislature.state.oh.us/' +
            'BillText%s/%s_%s_PHC_N.html' %
            (session, session, id_url))

def make_url_3(session, id_url):
    return ('http://www.legislature.state.oh.us/' +
            'BillText%s/%s_%s_I_N.html' %
            (session, session, id_url))

def make_url_framed(session, id_url):
    return ( 'http://www.legislature.state.oh.us/' +
             'bills.cfm?ID=%s_%s' % (session, id_url))

class OhioBill(object):
    def __init__(self, year, chamber, number):
        self.year = year
        self.chamber = chamber
        self.session = year_to_session(year)
        self.number = number

        self.filename = self.make_filename()
        self.id = self.make_id()
        self.id_url = self.id.replace(' ', '_')
        self.url = make_url_1(self.session, self.id_url)

        self.name = None
        self.version_name = None
        self.text = None

    def make_id(self):
        if self.chamber == 'lower':
            return 'HB %s' % self.number
        return 'SB %s' % self.number

    def make_filename(self):
        return 'data/oh/%s_%s_%s.html' % (self.session, self.chamber,
                                          self.number)

    def parse_bill(self):
        #
        # Example code for using html5 to create BeautifulSoup objects.
        #
        # # BeautifulSoup from html5lib
        #import html5lib
        #from html5lib import treebuilders
        #import urllib2
        #
        #def make_soup():
        #    fd = urllib2.urlopen('http://mehfilindian.com/LunchMenuTakeOut.htm')
        #    parser = html5lib.HTMLParser(tree=treebuilders.getTreeBuilder("beautifulsoup"))
        #    minidom_document = parser.parse(fd)
        #    return minidom_document

        # More info: http://code.google.com/p/html5lib/wiki/UserDocumentation
        #make_tree = make_dom

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
        url_methods = (make_url_1, make_url_2, make_url_3, make_url_framed)

        for url_method in url_methods:
            self.url = url_method(self.session, self.id_url)
            self.text = urllib.urlopen(self.url).read()

            if text_is_a_bill(self.text):
                logging.info('Retrieved %s' % self.url)
                return
            else:
                # For many bills, this is an expected failure.
                logging.debug('%s failed' % self.url)

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

    # By default, all years and both chambers are scraped.
    #
    # To scrape one chamber, specify '--upper' or '--lower'.
    # To scrape one year, specify '--year YYYY'
    def run(self):
        parser = optparse.OptionParser(option_list=self.option_list)
        options, args = parser.parse_args()
        self.scrape_bills(options.upper, options.lower, options.years)

    def scrape_bills(self, upper=False, lower=False, year_range=None):
        if year_range:
            years = year_range
        else:
            years = range(1997, int(time.strftime('%Y')) + 1)

        chambers = ['upper', 'lower']
        if upper and not lower:
            chambers = ['upper']
        if lower and not upper:
            chambers = ['lower']

        for year in years:
            for chamber in chambers:
                bill_number = 1
                while True:
                    bill = OhioBill(year, chamber, bill_number)

                    # If we don't have the bill, go get it and save it.
                    if not os.path.isfile(bill.filename):
                        try:
                            bill.retrieve_bill_text()
                        except legislation.NoDataForYear:
                            logging.info('Stopping.')
                            break
                        bill.save_bill_text_as_file()
                        # Give the poor web server a break.
                        time.sleep(1)
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
