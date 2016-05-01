import re
import sys
sys.path.insert(1, '.')

from common.database import Database

reviews = Database().db.reviews
phones = Database().db.phones

phones_cursor = phones.find({})

for phone in phones_cursor:
	print phone['phone_name']

	phone_name = phone['phone_name']
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

	for count in reviews_cursor:
		print count['positive'], count['negative'], count['neutral']