'''
Created on 24 Apr 2016

@author: RAJESH
'''

from database import Database

class Phone:
    def __init__(self):
        self.phone_id = ''
        self.phone_name = ''
        self.no_of_sims = ''
        self.size = ''
        self.resolution = ''
        self.operating_system = ''
        self.chipset = ''
        self.cpu = ''
        self.gpu = ''
        self.memory_internal = ''
        self.memory_cart_slot = ''
        self.camera_front = ''
        self.camera_back = ''
        self.network = ''
        self.battery = ''

    def save(self):
        phones = Database().db.phones
        try:
            phones.insert_one({
                'phone_id': self.phone_id  ,
                'phone_name': self.phone_name,
                'no_of_sims': self.no_of_sims,
                'size': self.size,
                'resolution': self.resolution,
                'operating_system': self.operating_system,
                'chipset': self.chipset,
                'cpu': self.cpu,
                'gpu': self.gpu,
                'memory_internal': self.memory_internal,
                'memory_cart_slot': self.memory_cart_slot,
                'camera_front': self.camera_front,
                'camera_back': self.camera_back,
                'network': self.network,
                'battery': self.battery
            })
        except:
            print "Error in Phone.save method"