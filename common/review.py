'''
Created on 26 Apr 2016

@author: RAJESH
'''

from database import Database

class Review:
    def __init__(self):
        self.source = ''
        self.phone_name = ''
        self.review_raw_text = ''

    def save(self):
        reviews = Database().db.reviews
        try:
            reviews.insert_one({
                'source': self.source  ,
                'phone_name': self.phone_name,
                'review_raw_text': self.review_raw_text
            })
        except:
            print "Error in Review.save method"