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

from common.phone import Phone

class GSMAreanaCrawler:
    def __init__(self, url):
        self.url = url

    def crawl(self):
        try:
            request = urllib2.urlopen(self.url)
            page = request.read().encode('utf8')
        except Exception, e:
            print 'Failed to read webpage : %s' % e

        soup = BeautifulSoup(page, 'html.parser')

        spec_tables = soup.findAll('table')

        phone = Phone()
        phone.phone_name = soup.find('h1', {'class': 'specs-phone-name-title'}).getText().strip()
        phone.phone_id = phone.phone_name.replace(' ', '-').lower()

        for table in spec_tables:
            specs_row = table.findAll('tr')    
            for row in specs_row:
                try:
                    key = row.find('td', {'class': 'ttl'}).getText().strip()
                    value = row.find('td', {'class': 'nfo'}).getText().strip()

                    if  key == 'Technology':
                        phone.network = value
                    elif key == 'SIM':
                        phone.no_of_sims = value
                    elif key == 'Size':
                        phone.size = value
                    elif key == 'Resolution':
                        phone.resolution = value
                    elif key == 'OS':
                        phone.operating_system = value
                    elif key == 'CPU':
                        phone.cpu = value
                    elif key == 'Chipset':
                        phone.chipset = value
                    elif key == 'GPU':
                        phone.gpu = value
                    elif key == 'Internal':
                        phone.memory_internal = value
                    elif key == 'Card slot':
                        phone.memory_cart_slot = value
                    elif key == 'Primary':
                        phone.camera_front = value
                    elif key == 'Secondary':
                        phone.camera_back = value
                    else:
                        battery_regex = re.compile('.*\d*\s?mAh.*')
                        matches = battery_regex.search(value)
                        if matches:
                            phone.battery = matches.group(0)                
                    
                except Exception, e:
                    continue

        phone.save()

# logging.basicConfig(filename='phone_specs_crawl.log', level=logging.DEBUG)

GSMAreanaCrawler('http://www.gsmarena.com/motorola_moto_e_dual_sim-6323.php').crawl()
