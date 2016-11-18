"""
@date:   November 17, 2016
@author: Lior Bialik
"""

import argparse
import datetime

options = None

def assertOptionsInit():
    assert options is not None, "options not initialized yet"


def getCmdLineOptions():
    parser = argparse.ArgumentParser(description='Twitter Statuses Fetcher')

    parser.add_argument('-n', '--screenName', required=True, action='append',
                        help='The screen name of the person you want to fetch. Use -n <NAME1> -n <NAME2> for multiple names')
    parser.add_argument('-t', '--tweetsToFetch', default=None, type=assertValidTweetsToFetch,
                        help='The amount of twits you want to fetch. Can use \'all\'. If left empty the default is 50')
    parser.add_argument('-s', '--startDate', default='user_creation_time', type=assertValidDate,
                        help='The start date of all twits, use format y-m-d')
    parser.add_argument('-e', '--endDate', default='current_time', type=assertValidDate,
                        help='The end date of all twits, use format y-m-d')

    cmdLineOptions = parser.parse_args()
    
    return cmdLineOptions


def getScreenName():
    assertOptionsInit()
    return options.screenName

def getTweetsToFetch():
    assertOptionsInit()
    return options.tweetsToFetch

def getDatesToFetch():
    assertOptionsInit()
    return options.startDate, options.endDate


def assertValidTweetsToFetch(tweetsToFetch):
    if tweetsToFetch == "all" or tweetsToFetch ==None:
        return tweetsToFetch
    else:
        try:
            int(tweetsToFetch)
            return tweetsToFetch
        except ValueError:
            raise ValueError("Wrong input. tweetsToFetchcan be either an integer or \"all\"")

def assertValidDate(date):
    if date == 'user_creation_time' or date == 'current_time':
        return None
    else:
        try:
            date = datetime.datetime.strptime(date, '%y-%m-%d')
            return date
        except ValueError:
            raise ValueError("Wrong input. Date should be in format y-m-d")

