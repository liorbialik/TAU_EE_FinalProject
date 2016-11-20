"""
@date:   November 17, 2016

This program will get all the tweets made by a given user or users (maxing at 3240).
user can filter by start and end dates

@author: Lior Bialik & Avihai Ezaguy
"""

import twitter # https://github.com/bear/python-twitter
import config
import sys
import datetime
import csv
import os

# authorization keys from https://apps.twitter.com/ for the app TUA_EE_Project_statusFetch:
twitterConsumerKey = 'kPIBTAAB1n9Wp5MEu1fdwzsXj'
twitterConsumerSecret = 'dFj6lz5iLtUvXXacQLWuJ3xubMelP2WQep5efvm195TEMoo4JW'
twitterAccessTokenKey = '799287561332162560-UFz71F1VPcNDns1fWV9qAj4qKRxkyxU'
twitterAccessTokenSecret = '9KebOrRMw63HHZK9l31SsM5BnYJpz9nqyq1905zpYUCCQ'

# The maximum number of tweets to pull in a single request allowed by the API:
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


def fetchTweetsToCsv(screenNames, startDateFilter, endDateFilter):

    # initialize python-twitter API
    api = getTwitterApi()

    # download the tweets of every user specified into a different file
    for screenName in screenNames:
        print("Getting tweets for user %s:" % screenName)
        allTweetsList = []

        # download the first tweet from the website
        newTweets = api.GetUserTimeline(screen_name=screenName, count=1)

        # extend the list of all tweets with the latest batch downloaded
        allTweetsList.extend(newTweets)

        # set the oldest tweet ID number in the current batch to be the latest ID to be pulled in the next batch
        oldestTweetId = allTweetsList[-1].id - 1

        # download tweets batches until there are no more available
        while len(newTweets) > 0:
            newTweets = api.GetUserTimeline(screen_name=screenName, count=MAX_NUMBER_OF_TWEETS_PER_REQUEST,
                                            max_id=oldestTweetId)
            
            # set the oldest tweet ID number in the current batch to be the latest ID to be pulled in the next batch
            oldestTweetId = newTweets[-1].id - 1

            # if newest tweet of newTweets is newer than endDateFilter - continue to next request
            if getTimestamp(newTweets[-1].created_at) > endDateFilter:
                continue 
            
            # extend the list of all tweets with the latest batch downloaded
            allTweetsList.extend(newTweets)

            # if oldest tweet of newTweets is older than startDateFilter - stop requesting for new tweets
            if getTimestamp(newTweets[-1].created_at) < startDateFilter:
                break 
            
        print("Filtering tweets by date")
        readableFormatTweetsList = [[tweet.id_str, stringTimestamp(getTimestamp(tweet.created_at)),
                                     tweet.text.encode("utf-8")] for tweet in allTweetsList
                                    if endDateFilter > getTimestamp(tweet.created_at) > startDateFilter] # filtering out dates

        saveTweetsToFile(screenName, readableFormatTweetsList)


if __name__ == "__main__":
    # initialize configuration options
    try:
        config.options = config.getCmdLineOptions()
    except AssertionError as e:
        print(e.message)
        sys.exit(1)

    # download and save all tweets to csv file
    fetchTweetsToCsv(screenNames=config.getScreenName(),
                     startDateFilter=config.getStartDateToFilter(),
                     endDateFilter=config.getEndDateToFilter())

