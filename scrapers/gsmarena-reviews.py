'''
Created on 24 Apr 2016

@author: RAJESH
'''
import sys
sys.path.insert(1, '.')

#System Library
from bs4 import BeautifulSoup
import urllib2
import logging
import json
import re

from common.review import Review
from common.crawler import Crawler

class GSMAreanaReviewCrawler:
    def __init__(self, url):
        self.url = url

    def crawl(self):
        soup = Crawler.get_soup(self.url)
        self.url = 'http://www.gsmarena.com/' + soup.find('a', text = 'Read all opinions')['href']
        phone_name = soup.find('h1', {'class': 'specs-phone-name-title'}).getText().strip()

        soup = Crawler.get_soup(self.url)

        review_page_count = int(soup.find('div', {'id': 'user-pages'}).findAll('a')[-2].getText())

        url = self.url
        for i in xrange(2, review_page_count):
            reviews = soup.findAll('p', {'class': 'uopin'})
            for r in reviews:
                for tag in r.findAll('a'):
                    tag.replaceWith('')

                for tag in r.findAll('span'):
                    tag.replaceWith('')

                review = Review()
                review.source = 'gsmarena'
                review.phone_name = phone_name
                review.review_raw_text = r.getText().strip()
                review.save()
                print review.review_raw_text
            

            url = self.url.replace('.php', 'p%d.php' % i)
            soup = Crawler.get_soup(url)
    
GSMAreanaReviewCrawler('http://www.gsmarena.com/motorola_moto_e_dual_sim-6323.php').crawl()