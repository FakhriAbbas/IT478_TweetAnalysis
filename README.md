IT478_TweetAnalysis
===================

Sentiment analysis of ISU Twitter followers

Rewrite in progress

1. Set up stream with criteria for ISU
    1. @IllinoisStateU
    2. #ISU
    3. #ilstu
    4. #illinoisstate
2. Listen for tweets
3. When tweet collected, extract the fields we want (and fake up some fields)
4. Transform data types when necessary
5. Load to the staging tables for sentiment scoring
5. Et finito/ad infinitum

### TODO
1. Set up the db in a different script which will get called when the listener starts. The script will check to see that all of the tables/indices are created and create them if not.
2. Write a new parser/db program which will take in a raw tweet, extract the user/text/etc, mock up an age/gender, and then write that to the staging tables
3. Also, need to add markers (per/see Mike)
