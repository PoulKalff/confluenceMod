#!/usr/bin/env python3

import sys
import json
import time
import sqlite3
import datetime
import requests
import urllib.parse as urlparse
#from resources.lib.tvapi import *
from modified_tvapi import *
from db_class import HandleDB


# --- Variables -----------------------------------------------------------------------------------

API_URL = 'http://www.dr.dk/mu-online/api/1.4'
allPrograms = {}

# --- Calls ---------------------------------------------------------------------------------------

class ProgressBar:
	""" will output a line of <size> dots after being called <total> times"""

	def __init__(self, total, size):
		self.progress = 0
		self.step = total / size
		self.total = self.step

	def showProgress(self):
		self.progress += 1
		if self.progress >= round(self.total, 5):	# must round, to correct python deviation
			self.total += self.step
			print('.', end="")


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



# --- Main  ---------------------------------------------------------------------------------------

# fully clean and re-populate the DB
startTime = time.time()
print('Program init')
objDB = HandleDB()
print('  Clearing tables...........................', end='')
objDB.clearTables()
print('done!')
print('  Fetching program indexes..................', end='')
programIndexes = getProgramIndexes()
print('done!')
print('  Writing program indexes to database.......', end='')
objDB.writeProgramIndexes(programIndexes)
print('done!')
print('  Fetching programs.........................', end='')
for index in programIndexes:
	allPrograms[index['Title']] = getSeries(index['_Param'])
print('done!')
print('  Writing programs to database..............', end='')
objDB.writePrograms(allPrograms)
print('done!')
for i in programIndexes:
	print('  Processing index', i['Title'] + str(':'))
	data = objDB.getProgramsByIndex(i['Title'])
	episodes = []
	objProgress = ProgressBar(len(data), 15)
	print('    Fetching program episodes', end='')
	for d in data:
		objProgress.showProgress()
		episodes += getEpisodes(d[3])
	print('done!')
	print('    Writing Episodes to database............', end='')
	objDB.writeEpisodes(episodes)
	print('done!')
endTime = time.time()
print('\n---------------------------------------------------------------------------')
print('Program completed gracefully')
print('   Errors encountered  :', objDB.errorCount)
print('   Execution took      :', round((endTime - startTime) / 60, 3), 'minutes\n')






