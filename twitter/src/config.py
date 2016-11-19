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
                        help='The screen name of the person you want to fetch. Use -n <NAME1> -n <NAME2> for multiple names.'
                             'Example: -n @BarackObama -n @realDonaldTrump')

    parser.add_argument('-s', '--startDate', default=epochTime, type=assertValidDate,
                        help='Filter the start date of all twits, use format yy-mm-dd')

    parser.add_argument('-e', '--endDate', default=currentTime, type=assertValidDate,
                        help='Filter the end date of all twits, use format yy-mm-dd')

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
    return options.endDate


def assertValidDate(date):
    if date is None:
        return date
    else:
        try:
            date = datetime.datetime.strptime(date, '%y-%m-%d')
            return date
        except ValueError:
            raise ValueError("Wrong input. Date should be in format y-m-d")

