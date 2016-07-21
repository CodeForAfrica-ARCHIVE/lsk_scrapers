"""
"""

import dataset
from lsk_scrapers.config import DATABASE, MESSAGES

def get_db():
    return dataset.connect('mysql://{username}:{password}@{host}'.format(**DATABASE))

def query(params):
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
    return MESSAGES['miss'] if not resp['hit'] else MESSAGES['hit'].format(**resp)
