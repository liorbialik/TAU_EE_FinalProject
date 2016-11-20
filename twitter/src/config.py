"""
@date:   November 17, 2016
@author: Lior Bialik
"""

import argparse
import datetime

# times used as defaults in arguments
epochTime = datetime.datetime.strptime('0', '%S')
currentTime = datetime.datetime.now()

options = None

def assertOptionsInit():
    assert options is not None, "options not initialized yet"


def getCmdLineOptions():
    parser = argparse.ArgumentParser(description='Twitter Statuses Fetcher')

    parser.add_argument('-u', '--screenName', required=True, action='append',
                        help='The screen name of the person you want to fetch. Use -u <NAME1> -u <NAME2> for multiple names.'
                             'Example: -u @BarackObama -u @realDonaldTrump')

    parser.add_argument('-s', '--startDate', default=epochTime, type=assertValidDate,
                        help='Filter the start date of all twits, use format dd-mm-yy')

    parser.add_argument('-e', '--endDate', default=currentTime, type=assertValidDate,
                        help='Filter the end date of all twits, use format dd-mm-yy')

    cmdLineOptions = parser.parse_args()
    
    return cmdLineOptions


def getScreenName():
    assertOptionsInit()
    return options.screenName


def getStartDateToFilter():
    assertOptionsInit()
    return options.startDate


def getEndDateToFilter():
    assertOptionsInit()
    # time of day selected is 00:00 therefore need to add one day in order to include it.
    # if date+1d is newer than currentTime twitter API wouldn't fail
    return options.endDate + datetime.timedelta(days=1)


def assertValidDate(date):
    if date is None:
        return date
    else:
        try:
            date = datetime.datetime.strptime(date, '%d-%m-%y')
            return date
        except ValueError:
            raise ValueError("Wrong input. Date should be in format dd-mm-yy")

