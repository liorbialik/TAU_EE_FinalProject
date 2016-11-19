"""
@date:   November 17, 2016

This program will get all the tweets made by a given user or users (maxing at 3218).
user can filter

@author: Lior Bialik & Avihai Ezaguy
"""

import twitter # https://github.com/bear/python-twitter
import config
import sys
import datetime
import csv
import os

# keys from https://apps.twitter.com/ for the app TUA_EE_Project_statusFetch:
twitterConsumerKey = 'kPIBTAAB1n9Wp5MEu1fdwzsXj'
twitterConsumerSecret = 'dFj6lz5iLtUvXXacQLWuJ3xubMelP2WQep5efvm195TEMoo4JW'
twitterAccessTokenKey = '799287561332162560-UFz71F1VPcNDns1fWV9qAj4qKRxkyxU'
twitterAccessTokenSecret = '9KebOrRMw63HHZK9l31SsM5BnYJpz9nqyq1905zpYUCCQ'

# Magics:
MAX_NUMBER_OF_TWEETS_PER_REQUEST = 200


def getTimestamp(apiTimeStamp):
    timestamp = datetime.datetime.strptime(apiTimeStamp, '%a %b %d %H:%M:%S +0000 %Y')
    return timestamp


def stringTimestamp(timestamp):
    fmt = '%Y-%m-%d %H:%M:%S: '
    return timestamp.strftime(fmt)


def getTwitterApi():
    api = twitter.Api(consumer_key=twitterConsumerKey,
                      consumer_secret=twitterConsumerSecret,
                      access_token_key=twitterAccessTokenKey,
                      access_token_secret=twitterAccessTokenSecret)
    return api


def saveTweetsToFile(screenName, readableFormatTweetsList):
    outputFileName = '%s_tweets.csv' % screenName
    outputFilePath = os.path.join(os.getcwd(), outputFileName)
    with open(outputFileName, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(["id", "created_at", "text"])
        writer.writerows(readableFormatTweetsList)
    print("%s tweets were saved at %s" % (screenName, outputFilePath))


def fetchStatusText(screenNames, startDateFilter, endDateFilter):
    api = getTwitterApi()
    
    for screenName in screenNames:
        print("Getting tweets for user %s:" % screenName)
        allTweetsList = []
        newTweets = api.GetUserTimeline(screen_name=screenName, count=MAX_NUMBER_OF_TWEETS_PER_REQUEST)
        allTweetsList.extend(newTweets)
        oldestTweetId = allTweetsList[-1].id - 1
        while len(newTweets) > 0:
            newTweets = api.GetUserTimeline(screen_name=screenName, count=MAX_NUMBER_OF_TWEETS_PER_REQUEST,
                                            max_id=oldestTweetId)
            allTweetsList.extend(newTweets)
            oldestTweetId = allTweetsList[-1].id - 1

        print("Filtering tweets by date")
        readableFormatTweetsList = [[tweet.id_str, stringTimestamp(getTimestamp(tweet.created_at)),
                                     tweet.text.encode("utf-8")] for tweet in allTweetsList
                                    if endDateFilter > getTimestamp(tweet.created_at) > startDateFilter]
        saveTweetsToFile(screenName, readableFormatTweetsList)

if __name__ == "__main__":
    try:
        config.options = config.getCmdLineOptions()
    except AssertionError as e:
        print(e.message)
        sys.exit(1)
    fetchStatusText(screenNames=config.getScreenName(),
                    startDateFilter=config.getStartDateToFilter(),
                    endDateFilter=config.getEndDateToFilter())

