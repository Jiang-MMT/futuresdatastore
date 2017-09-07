#!/Users/gene/.virtualenvs/fdsv/bin/python

from scrape import Scraper


url = 'https://www.barchart.com/futures/prices-by-exchange'
selenium_query = 'bc-glyph-plus'
bs_query = 'a.commodity'
scraper = Scraper(url=url,
                  selenium_query=selenium_query,
                  bs_query=bs_query)
scraper.parse_data()
print 'symbol dataset is ready!'
