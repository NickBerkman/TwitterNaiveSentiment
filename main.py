import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import matplotlib.pyplot as plt






class TwitterClient(object):

	def __init__(self):
		# keys and tokens from the Twitter Dev Console
		consumer_key = '?'
		consumer_secret = '?'
		access_token = '?'
		access_token_secret = '?'

		# attempt authentication
		try:
			# create OAuthHandler object
			self.auth = OAuthHandler(consumer_key, consumer_secret)
			# set access token and secret
			self.auth.set_access_token(access_token, access_token_secret)
			# create tweepy API object to fetch tweets
			self.api = tweepy.API(self.auth)
		except:
			print("Error: Authentication Failed")

	def clean_tweet(self, tweet):
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])	|(\w+:\/\/\S+)", " ", tweet).split())

	def get_tweet_sentiment(self, tweet):

		# create TextBlob object of passed tweet text
		analysis = TextBlob(self.clean_tweet(tweet), analyzer=NaiveBayesAnalyzer())
		# set sentiment
		if  analysis.sentiment.p_pos >= .5:
			return 'positive'

		elif  analysis.sentiment.p_neg >= .5:
			return 'negative'
		else:
			return 'neutral'






	def get_tweets(self, query, count) -> object:

		# empty list to store parsed tweets
		tweets = []

		try:
			# call twitter api to fetch tweets
			fetched_tweets = self.api.search_tweets(q = query, count = count)




			# parsing tweets one by one
			for tweet in fetched_tweets:
				# empty dictionary to store required params of a tweet
				parsed_tweet = {}

				# saving text of tweet
				parsed_tweet['text'] = tweet.text
				# saving sentiment of tweet
				parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)



				# appending parsed tweet to tweets list
				if tweet.retweet_count > 0:
					# if tweet has retweets, ensure that it is appended only once
					if parsed_tweet not in tweets:
						tweets.append(parsed_tweet)
				else:
					tweets.append(parsed_tweet)

			# return parsed tweets
			return tweets

		except tweepy.TweepError as e:
			# print error (if any)
			print("Error : " + str(e))





def plotPieChart(positive, negative, neutral):
	labels = ['Positive [' + str(positive) ,
			  'Negative [' + str(negative),
			  'Neutral [' + str(neutral)]
	sizes = [positive, negative, neutral]
	colors = ['darkgreen', 'darkred', 'grey']
	patches, texts = plt.pie(sizes, colors=colors, startangle=90)
	plt.legend(patches, labels, loc="best")
	plt.axis('equal')
	plt.tight_layout()
	plt.show()
	pass


def main():
	# creating object of TwitterClient Class
	api = TwitterClient()

	searchTerm = input("Enter Keyword/Tag to search about: ")
	NoOfTerms = int(input("Enter how many tweets to search: "))
	print('\nLoading ...  ')

	# calling function to get tweets
	tweets = api.get_tweets(searchTerm, count = NoOfTerms)



	# picking positive tweets from tweets
	ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
	# percentage of positive tweets
	print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))
	# picking negative tweets from tweets
	ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
	# percentage of negative tweets
	print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))
	netweets = [tweet for tweet in tweets if tweet['sentiment'] == 'neutral']
	# percentage of neutral tweets
	print("Neutral tweets percentage: {} %".format(100 * len(netweets) / len(tweets)))


	

	plotPieChart(len(ptweets),len(ntweets), len(netweets))











if __name__ == "__main__":
	# calling main function
	main()

