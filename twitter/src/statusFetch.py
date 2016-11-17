"""
@date:   November 17, 2016
@author: Lior Bialik
"""

import twitter
import config
import sys

twitterConsumerKey = 'kPIBTAAB1n9Wp5MEu1fdwzsXj'
twitterConsumerSecret = 'dFj6lz5iLtUvXXacQLWuJ3xubMelP2WQep5efvm195TEMoo4JW'
twitterAccessTokenKey = '799287561332162560-UFz71F1VPcNDns1fWV9qAj4qKRxkyxU'
twitterAccessTokenSecret = '9KebOrRMw63HHZK9l31SsM5BnYJpz9nqyq1905zpYUCCQ'


def getTwitterApi():
    api = twitter.Api(consumer_key=twitterConsumerKey,
                      consumer_secret=twitterConsumerSecret,
                      access_token_key=twitterAccessTokenKey,
                      access_token_secret=twitterAccessTokenSecret)
    return api


def fetchStatusText(screenName, tweetsToFetch):
    api = getTwitterApi()
    statuses = api.GetUserTimeline(screen_name=screenName, count=tweetsToFetch) # TODO: add the options to get for multiple users' statuses
    return [status.text for status in statuses]


if __name__ == "__main__":
    try:
        config.options = config.getCmdLineOptions()
    except AssertionError as e:
        print(e.message)
        sys.exit(1)


    completeStatusText = fetchStatusText(screenName=config.getScreenName(),
                                         tweetsToFetch=config.getTweetsToFetch())

    # TODO: need to create a printing function that allows printing by hashtaags
    for singleStatusText in completeStatusText:
        print(singleStatusText)
