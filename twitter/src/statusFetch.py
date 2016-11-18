"""
@date:   November 17, 2016
@author: Lior Bialik & Avihai Ezaguy
"""

import twitter # https://github.com/bear/python-twitter
import config
import sys
import datetime

# keys from https://apps.twitter.com/ for the app TUA_EE_Project_statusFetch:
twitterConsumerKey = 'kPIBTAAB1n9Wp5MEu1fdwzsXj'
twitterConsumerSecret = 'dFj6lz5iLtUvXXacQLWuJ3xubMelP2WQep5efvm195TEMoo4JW'
twitterAccessTokenKey = '799287561332162560-UFz71F1VPcNDns1fWV9qAj4qKRxkyxU'
twitterAccessTokenSecret = '9KebOrRMw63HHZK9l31SsM5BnYJpz9nqyq1905zpYUCCQ'

def getTimeStamp(api_TimeStamp):
    timestamp = datetime.datetime.strptime(api_TimeStamp, '%a %b %d %H:%M:%S +0000 %Y')
    return timestamp

def strTimeStamp(timestamp):
    fmt = '%Y-%m-%d %H:%M:%S: '
    return timestamp.strftime(fmt)
    


def getTwitterApi():
    api = twitter.Api(consumer_key=twitterConsumerKey,
                      consumer_secret=twitterConsumerSecret,
                      access_token_key=twitterAccessTokenKey,
                      access_token_secret=twitterAccessTokenSecret)
    return api


def fetchStatusText(screenNames, tweetsToFetch, dates):
    api = getTwitterApi()
    
    for screenName in screenNames:
        if tweetsToFetch != None: # -t was selected
    # TODO: need to create an external function for getting the statuses, and in case of all implement 'def getAllTweets'
            statuses = api.GetUserTimeline(screen_name=screenName, count=tweetsToFetch)
            completeStatusesText = [strTimeStamp(getTimeStamp(status.created_at)) + status.text for status in statuses]
            for singleStatusText in completeStatusesText: # TODO: add separate printing function
                print(singleStatusText)
        
        # -e, -s selected
        else:
            startDate = dates[0]
            endDate = dates[1]
            if endDate == None:
                endDate = datetime.datetime.now()
            if startDate == None:
                startDate = datetime.datetime.strptime('0', '%S') # EPOCH time
            statuses = api.GetUserTimeline(screen_name=screenName, since_id=0)
            completeStatusesText = [strTimeStamp(getTimeStamp(status.created_at)) + status.text for status in statuses
                                    if getTimeStamp(status.created_at) < endDate and getTimeStamp(status.created_at) > startDate]
            for singleStatusText in completeStatusesText: # TODO: add separate printing function
                print(singleStatusText)

            
            


if __name__ == "__main__":
    try:
        config.options = config.getCmdLineOptions()
    except AssertionError as e:
        print(e.message)
        sys.exit(1)


    fetchStatusText(screenNames=config.getScreenName(),
                    tweetsToFetch=config.getTweetsToFetch(),
                    dates=config.getDatesToFetch())

