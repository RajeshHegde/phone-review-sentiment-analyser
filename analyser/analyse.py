import re
import sys
sys.path.insert(1, '.')

from sentimental_analysis import *
from common.database import Database

reviews = Database().db.reviews

# cursor = reviews.find({})
# for review in cursor:
# 	review['sentiment_score'] = {'battery': 0, 'design': 0, 'camera': 0, 'display': 0, 'sound': 0, 'heat': 0, 'overall': 0}
# 	reviews.save(review)

# exit()

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
		overall_score = get_sentiment_score(review_raw_text)

		review['sentiment_score'][sentiment['name']] = sentiment_score
		review['sentiment_score']['overall'] = overall_score

		reviews.save(review)

	score_query_part = "$sentiment_score.%s" % (sentiment['name'])

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

	for count in cursor:
		print count['positive'], count['negative']
	

cursor = reviews.aggregate([{ 
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

for count in cursor:
	print count['positive'], count['negative'], count['neutral']

# cursor = reviews.aggregate([{ 
#     "$group": { 
#         "_id": "null", 
#         "total": { 
#             "$sum": "$sentiment_score.design" 
#         } 
#     } 
# }])


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