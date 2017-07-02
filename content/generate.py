import re
import sys
sys.path.insert(1, '.')

from common.database import Database

reviews = Database().db.reviews
phones = Database().db.phones

phones_cursor = phones.find({})
sentiments = ['battery', 'design', 'camera', 'display', 'sound', 'heat']

for phone in phones_cursor:
	phone_name = phone['phone_name']
	print 'Phone Name : %s' % phone_name
	print 'Network: %s ' % (phone['network'])
	print 'SIM: %s ' % (phone['no_of_sims'])
	print 'Size: %s ' % (phone['size'])
	print 'Display: %s ' % (phone['resolution'])
	print 'Operating System: %s ' % (phone['operating_system'])
	print 'CPU: %s ' % (phone['cpu'])
	print 'Chipset: %s ' % (phone['chipset'])
	print 'GPU: %s ' % (phone['gpu'])
	print 'Internal Memory: %s ' % (phone['memory_internal'])
	print 'Card Slot: %s ' % (phone['memory_cart_slot'])
	print 'Primary Camera: %s ' % (phone['camera_back'])
	print 'Secondary Camera: %s ' % (phone['camera_front'])
	print 'Battery : %s' % phone['battery']

	for sentiment in sentiments:
		score_query_part = "$sentiment_score.%s" % (sentiment)
		cursor = reviews.aggregate([{ 
		    "$project": {
		        "_id": 0,
		        "positive_sentiment": {"$cond": [{"$gt": [score_query_part, 0]}, 1, 0]},
		        "negative_sentiment": {"$cond": [{"$lt": [score_query_part, 0]}, 1, 0]}
		    }
		},
		{ 
		    "$group": {
		    	"_id": "null",
		    	"positive": {"$sum": "$positive_sentiment"},
		    	"negative": {"$sum": "$negative_sentiment"}
		    }
		}])

		print sentiment.upper()
		for count in cursor:
			print 'Positive: %d' % (count['positive'])
			print 'Negative: %d' % (count['negative'])

	reviews_cursor = reviews.aggregate([
	{
		 "$match" : { "phone_name" : phone_name }
	},
	{ 
	    "$project": {
	        "_id": 0,
	        "positive_sentiment": {"$cond": [{"$gt": ["$sentiment_score.overall", 0]}, 1, 0]},
	        "negative_sentiment": {"$cond": [{"$lt": ["$sentiment_score.overall", 0]}, 1, 0]},
	        "neutral_sentiment": {"$cond": [{"$eq": ["$sentiment_score.overall", 0]}, 1, 0]}
	    }
	},
	{ 
	    "$group": {
	    	"_id": "null",
	    	"positive": {"$sum": "$positive_sentiment"},
	    	"negative": {"$sum": "$negative_sentiment"},
	    	"neutral": {"$sum": "$neutral_sentiment"}
	    }
	}])

	print 'Overall'
	for count in reviews_cursor:
		print 'Positive: %d' % (count['positive'])
		print 'Negative: %d' % (count['negative'])
		print 'Neutral: %d' % (count['neutral'])