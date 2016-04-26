'''
Created on 24 Apr 2016

@author: RAJESH
'''

from bs4 import BeautifulSoup
import urllib2


class Crawler:
	
	@staticmethod
	def get_soup(url):
		soup = None
		try:
			request = urllib2.urlopen(url)
			page = request.read()
			soup = BeautifulSoup(page, 'html.parser')
		except Exception, e:
			print 'Failed to read webpage : %s' % e

		return soup