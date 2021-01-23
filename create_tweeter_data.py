# Get Historical tweets using snscrape.modules.twitter
import snscrape.modules.twitter as sntwitter
import pandas as pd
import datetime
from datetime import timedelta

def bring_tweets():
    words = ['traffic', 'Traffic', 'trafic', 'Trafic', 'crash', 'Crash', 'incident', 'Incident',
             'accident', 'Accident', 'road', 'Road']
    tweets_list = []
    for word in words:
        string = word + ' from:DublinLive since:2017-01-01 until:2020-10-20'
        print(string)
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(string).get_items()):
            tweets_list.append([tweet.date, tweet.id, tweet.content, tweet.username])
    df_tweets = pd.DataFrame(tweets_list, columns=['Datetime', 'Tweet Id', 'Tweet', 'Username'])
    df_tweets = df_tweets.drop_duplicates()
    df_tweets['Datetime'] = pd.to_datetime(df_tweets['Datetime'])
    # create hour and date columns
    df_tweets['hour'] = df_tweets['Datetime'].dt.hour
    df_tweets['date'] = df_tweets['Datetime'].dt.date

    df_tweets['Datetime'] = df_tweets['Datetime'].apply(lambda dt: datetime.datetime(dt.year, dt.month, dt.day, dt.hour,0))
    df_tweets.to_csv('tweets.csv')
    print(df_tweets)
    return df_tweets

def create_hourly_range_column(df_tweets):
    df_twitter_events = pd.DataFrame()
    df_hourly = pd.date_range(start='2017-07-03', end='2018-09-15', freq='H')
    df_twitter_events['date'] = df_hourly
    event = []
    for i, row in df_twitter_events.iterrows():
        curr_date = row['date']
        hour_ahead = curr_date + timedelta(hours=1)
        if (curr_date in list(df_tweets['Datetime'].values)) or (
                hour_ahead in list(df_tweets['Datetime'].values)):
            event.append(1)
        else:
            event.append(0)

    df_twitter_events['event'] = event
    df_twitter_events.to_csv('event_tweet_update1.csv')
    return df_twitter_events

if __name__ == '__main__':
    df_tweets = bring_tweets()
    df_twitter_events = create_hourly_range_column(df_tweets)
    # df_hourly = pd.date_range(start='2017-07-03', end='2018-09-15', freq='H')
    # print(df_hourly)
