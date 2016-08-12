"""
"""
import dataset
import requests
from lsk_scrapers.config import DATABASE, MESSAGES, CLOUDSEARCH

def get_db():
    return dataset.connect('mysql://{username}:{password}@{host}'.format(**DATABASE))


def query(params):
    '''
    Query CloudSearch service
    '''
    try:
        args = {
                "q": params.get("name"),
                "q.parser": CLOUDSEARCH["parser"]
                }
        resp = requests.get(CLOUDSEARCH["url"], params=args, timeout=2)
        resp.raise_for_status()
        search_resp = resp.json()
        count = search_resp["hits"]["found"]
        if count:
            return dict(
                    hit=True,
                    count=count,
                    resp=search_resp["hits"]["hit"]
                    )
        else:
            # no results matching your query
            return dict(hit=False)


    except Exception, err:
        print "ERROR: query() - CloudSearch query fail - %s" % err
        raise err


def x_query(params):
    '''
    '''
    db = get_db()
    result = db[DATABASE['table']].find_one(name=params.get('name'))
    if not result:
        return dict(hit=False)
    else:
        response = dict(result)
        response['hit'] = True
        return response


def construct_message(resp):
    if not resp.get("hit"):
        return MESSAGES["miss"]
    else:
        if resp.get("count") == 1:
            return MESSAGES["one"].format(**resp["resp"][0]["fields"])
        else:
            message = ""
            for entry in resp["resp"]:
                message += MESSAGES["multi"].format(**entry["fields"])
            return MESSAGES["count"].format(**resp) + message
