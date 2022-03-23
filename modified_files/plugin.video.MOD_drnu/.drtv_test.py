import sys
import json
import sqlite3
import datetime
import requests
import urllib.parse as urlparse

from modified_tvapi import *
from db_class import HandleDB


# --- Variables -----------------------------------------------------------------------------------

API_URL = 'http://www.dr.dk/mu-online/api/1.4'
allPrograms = {}

# --- Functions -----------------------------------------------------------------------------------

def get_url(url):
        u = requests.get(url, timeout=30)
        if u.status_code == 200:
            content = u.text
            u.close()

        return json.loads(content)
        

def _http_request(url, params=None, cache=True):
        if not url.startswith(('http://','https://')):
            url = API_URL + urlparse.quote(url, '/')

        if params:
            url += '?' + urlparse.urlencode(params, doseq=True)


        u = requests.get(url, timeout=30)
        if u.status_code == 200:
            content = u.text
            u.close()
        else:
            print(u.status_code)
            print(url)

        return json.loads(content)

def getLatestPrograms():
        channel = ''
        result = _http_request('/page/tv/programs', {
            'index': '*',
            'orderBy': 'LastPrimaryBroadcastWithPublicAsset',
            'orderDescending': 'true',
            'channel': channel
        }, cache=False)
        return result['Programs']['Items']

def getAllChannels():
        channels = _http_request('/channel/all-active-dr-tv-channels')
        return [channel for channel in channels if channel['Title'] in ['DR1', 'DR2', 'DR Ramasjang']]


def getProgramIndexes():
        result = _http_request('/page/tv/programs')
        if 'Indexes' in result:
            indexes = result['Indexes']
            for programIndex in indexes:
                programIndex['_Param'] = programIndex['Source'][programIndex['Source'].rindex('/') + 1:]
            return indexes
        return []


def _handle_paging(result):
        items = result['Items']
        while 'Next' in result['Paging']:
            result = _http_request(result['Paging']['Next'])
            items.extend(result['Items'])
        return items

def getSeries(query):
        result = _http_request('/search/tv/programcards-latest-episode-with-asset/series-title-starts-with/{}'.format(query), {'limit': 75})
        return _handle_paging(result)

def getVideoUrl(assetUri):
        result = _http_request(assetUri)
        uri = None
        for link in result['Links']:
            if link['Target'] == 'HLS':
                uri = link['Uri']
                if uri == None:
                    uri = link['EncryptedUri']
                    uri = decrypt_uri(uri)
                break
        return uri


def getEpisodes(slug):
    result = _http_request('/list/{}'.format(slug), {'limit': 48, 'expanded': True})
    return _handle_paging(result)


def getEpisode(slug):
    return _http_request('/programcard/{}'.format(slug))




# --- Main  ---------------------------------------------------------------------------------------



slug = 'den-lille-prinsesse-series'
result = _http_request('/list/{}'.format(slug), {'limit': 48, 'expanded': True})



print(result['Items'][0])


sys.exit('killed for DEV')



# URL fra SLUG som virker:       http://www.dr.dk/mu-online/api/1.2/list/alene-i-vildmarken?limit=48&expanded=True
#API_URL =                       'http://www.dr.dk/mu-online/api/1.4/list/'
query = 'q'
result = _http_request('/search/tv/programcards-latest-episode-with-asset/series-title-starts-with/{}'.format(query), {'limit': 75})
print(type(result))

sys.exit('killed for DEV')

programIndexes = getProgramIndexes()
#print(programIndexes)

#for index in programIndexes:
#    allPrograms[index['Title']] = getSeries(index['_Param'])

example = getSeries('q')[0]

#example = allPrograms['Q'][0]



testSlug = example['Slug']
print(testSlug)

testEpisodes = getEpisode(testSlug)



print(testEpisodes)


