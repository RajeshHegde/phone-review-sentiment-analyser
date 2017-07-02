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
                'source': self.source,
                'phone_name': self.phone_name,
                'review_raw_text': self.review_raw_text,
                'sentiment_score': {
                    'battery': 0,
                    'design': 0,
                    'camera': 0,
                    'display': 0,
                    'sound': 0,
                    'heat': 0,
                    'overall': 0
                }
            })
        except:
            print "Error in Review.save method"