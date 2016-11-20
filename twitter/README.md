
### Introduction ###
This program will get all the tweets made by a given user or users (maxing at 3240).
user can filter by start and end dates

### How to run the program:

1. clone the repository.
2. enter the project directory: ```<Location on local>/TAU_EE_FinalProject/twitter```
3. run the script using the following command:
```$ python ./src/statusFetch.py <Flags>```

4. the output tweets will appear in a CSV file (different file for each user) in the home direcory ```<Location on local>/TAU_EE_FinalProject/twitter```

where the possible flags are:

``` -u / --screenName ``` : The screen name of the person you want to fetch. 
Use ```-u <NAME1> -u <NAME2>``` for multiple names.

``` -s / --startDate ```: Filter the start date of all twits, use format dd-mm-yy

``` -e / --endDate ```: Filter the end date of all twits, use format dd-mm-yy

``` -h / --help ```: Displace all the fpossible flags and uses

### Example:

```$ python ./src/statusFetch.py -u @realDonaldTrump  -u @BarackObama -s 1-11-16```

```$ python ./src/statusFetch.py -u @BarackObama -s 1-11-15 -e 1-11-16```
