import os
import redis
import requests
from urllib import quote

API_KEY = os.getenv("IMPORTIO_API_KEY")
#API = "https://api.import.io/store/connector/_magic?url={url}&format=JSON&js=false&_apikey={apikey}&_apikey={apikey}"
API = "https://api.import.io/store/connector/_magic?url={url}&format=JSON&js=false&_apikey={apikey}"
SOURCE = "http://online.lsk.or.ke/index.php/index.php?option=com_content&id=4&catid=8&qw=active&finder=Active&view=article&base=%s"
PAGES = 204 # Get this from the site
TIMEOUT = 23 # Request timeout in seconds
redis_host = os.getenv('REDIS_HOST', 'localhost:6379')
REDIS = dict(
        host=redis_host.split(':')[0],
        port=redis_host.split(':')[1],
        db='3',
        password=os.getenv('REDIS_PASSWORD', None),
        socket_timeout=2,
        socket_connect_timeout=2,
        )


class LSKScraper(object):
    def __init__(self,):
        self.api = API
        self.apikey = API_KEY
        self.db = redis.StrictRedis(**REDIS)
        self.db_prefix = "lsk-"
        self.source = SOURCE

    def scrape_page(self, page):
        try:
            args = dict(
                    url=quote(self.source % page),
                    apikey=self.apikey
                    )
            response = requests.get(self.api.format(**args), timeout=TIMEOUT)
            response.raise_for_status()
            resp = response.json()
            results = resp['tables'][0]['results']
            for result in results:
                print "{content_2} - {content_1}".format(**result)
            print "Extracted %s names from page %s" % (len(results), page)
            return results
        except Exception, err:
            print "ERROR: Failed to scrape data from page %s -- %s -- %s" % (page, args.get('url'), err)
            raise err


def main():
    """
    Execute scraper
    """
    for page in range(1, PAGES+1):
        url = SOURCE % str(page)
        response = requests.get(url, timeout=TIMEOUT)

