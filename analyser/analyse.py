import re
import sys
sys.path.insert(1, '.')

from sentimental_analysis import *
from common.database import Database

reviews = Database().db.reviews

sentiments = [
		{
			'name': 'battery',
			'alias': ['battery']
		},
		{
			'name': 'design',
			'alias': ['design']
		},
		{
			'name': 'camera',
			'alias': ['camera', 'cam', 'flash']
		},
		{
			'name': 'display',
			'alias': ['display', 'resolution']
		},
		{
			'name': 'sound',
			'alias': ['sound', 'music', 'speaker']
		},
		{
			'name': 'heat',
			'alias': ['heat']
		}
	]

for sentiment in sentiments:
	sentiment_regex = "|".join(sentiment['alias'])
	cursor = reviews.find({
		"review_raw_text" : {
			"$regex" : ".*(%s).*" % (sentiment_regex)
			}
		})
	for review in cursor:
		review_raw_text = review['review_raw_text']
		regex = r"([^.]*?%s[^.]*\.)" % (sentiment_regex)
		sentences = re.findall(regex, review_raw_text)
		sentiment_score = get_sentiment_score(".".join(sentences))

		review['sentiment_score'] = {
			sentiment['name']: sentiment_score
		}

		reviews.save(review)

	score_query_part = "$sentiment_score.%s" % (sentiment['name'])

	cursor = reviews.aggregate([{ 
	    "$project": {
	        "_id": 0,
	        "pos_sentiment": {"$cond": [{"$gt": [score_query_part, 0]}, 1, 0]},
	        "neg_sentiment": {"$cond": [{"$lt": [score_query_part, 0]}, 1, 0]}
	    }
	},
	{ 
	    "$group": {
	    	"_id": "null",
	    	"positive": {"$sum": "$pos_sentiment"},
	    	"negative": {"$sum": "$neg_sentiment"}
	    }
	}])

	for count in cursor:
		print count['positive'], count['negative']

# for review in cursor:
# 	review_raw_text = review['review_raw_text']
# 	regex = r"([^.]*?%s[^.]*\.)" % ("|".join(sentiments[3]['alias']))
# 	sentences = re.findall(regex, review_raw_text)
# 	sentiment_score = get_sentiment_score(".".join(sentences))
# 	print sentiment_score

# 	review['sentiment_score'] = {
# 		"battery": sentiment_score
# 	}

# 	reviews.save(review)	

# cursor = reviews.aggregate([{ 
#     "$group": { 
#         "_id": "null", 
#         "total": { 
#             "$sum": "$sentiment_score.design" 
#         } 
#     } 
# }])

'''
# [{ 
#     "$project": {
#         "_id": 0,
#         "pos_sentiment": {"$cond": [{"$gt": ["$sentiment_score.battery", 0]}, "$sentiment_score.battery", 0]},
#         "neg_sentiment": {"$cond": [{"$lt": ["$sentiment_score.battery", 0]}, "$sentiment_score.battery", 0]}
#     }
# },
# { 
#     "$group": {
#     "_id": null,
#     "SumPosSentiment": {"$sum": "$pos_sentiment"},
#     "SumNegSentiment": {"$sum": "$neg_sentiment"}
#     }
# }]
'''

# for count in cursor:
# 	print count['total']


# import nltk
# from nltk.collocations import *

# bigram_measures = nltk.collocations.BigramAssocMeasures()
# trigram_measures = nltk.collocations.TrigramAssocMeasures()

# # change this to read in your data
# finder = BigramCollocationFinder.from_words(
#    nltk.corpus.genesis.words('/Users/rajesh/work/projects/scrape-phone-info/assets/test.txt'))

# # only bigrams that appear 3+ times
# finder.apply_freq_filter(3) 

# # return the 10 n-grams with the highest PMI
# print finder.nbest(bigram_measures.pmi, 10)  