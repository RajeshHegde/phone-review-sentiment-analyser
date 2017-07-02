# url = 'http://www.gsmarena.com/motorola_moto_e_dual_sim-6323.php'

# http://stackoverflow.com/questions/10610131/checking-if-a-field-contains-a-string



# http://blog.mashape.com/list-of-20-sentiment-analysis-apis/
# https://github.com/hackreduce/Hackathon/wiki/Amazon-review-dataset

from sentimental_analysis import *
from common.database import Database

print get_sentiment_score("it is bad")

# reviews = Database().db.reviews