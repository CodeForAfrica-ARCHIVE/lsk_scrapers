import os, dataset, requests
from datetime import datetime
from urllib import quote
from lsk_scrapers.config import DATABASE

API_KEY = os.getenv("IMPORTIO_API_KEY")
#API = "https://api.import.io/store/connector/_magic?url={url}&format=JSON&js=false&_apikey={apikey}&_apikey={apikey}"
API = "https://api.import.io/store/connector/_magic?url={url}&format=JSON&js=false&_apikey={apikey}"
SOURCE = "http://online.lsk.or.ke/index.php/index.php?option=com_content&id=4&catid=8&qw=active&finder=Active&view=article&base=%s"
#PAGES = 204 # Get this from the site
PAGES = 2 # Get this from the site
TIMEOUT = 35 # Request timeout in seconds


class LSKScraper(object):
    def __init__(self,):
        self.api = API
        self.apikey = API_KEY
        self.source = SOURCE

        self.db = dataset.connect("mysql://{username}:{password}@{host}".format(**DATABASE))

    def persist(self, json_data):
        '''
        save to db
        '''
        dbtable = self.db[DATABASE['table']]
        dbresp = dbtable.insert(json_data)
        print "db said %s for %s" % (str(dbresp), json_data)
    
    def scrape_page(self, page):
        try:
            args = dict(
                    url=quote(self.source % page),
                    apikey=self.apikey
                    )
            start = datetime.now()
            response = requests.get(self.api.format(**args), timeout=TIMEOUT)
            print "timer - http - %s seconds" % (datetime.now() - start).seconds
            response.raise_for_status()
            resp = response.json()
            results = resp['tables'][0]['results']
            for result in results:
                result['link_1'] = result.get('link_1', "-")
                try:
                    result['name'] = result['content_1']
                    result['number'] = result['content_2']
                    result.pop("link_2/_source")
                    result.pop("link_1/_source")
                    result.pop("link_1/_text")
                    result.pop("link_2/_text")
                    result.pop("link_2")
                    result.pop("content_1")
                    result.pop("content_2")

                    start = datetime.now()
                    self.persist(result)
                    print "timer - db - %s seconds" % (datetime.now() - start).seconds

                except:
                    print "ERROR: Skipped %s" % result
            print "Extracted %s names from page %s" % (len(results), page)
            return results
        except Exception, err:
            print "ERROR: Failed to scrape data from page %s -- %s -- %s" % (page, args.get('url'), err)
            raise err


def main():
    """
    Execute scraper
    """
    lsk = LSKScraper()
    for page in range(1, PAGES+1):
        print "scraping page %s" % str(page)
        results = lsk.scrape_page(str(page))



if __name__ == "__main__":
    main()
