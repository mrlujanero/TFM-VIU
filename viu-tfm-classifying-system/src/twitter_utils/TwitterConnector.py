from __future__ import print_function

import twitter


class TwitterConnector:

    def __init__(self, consumer_key, consumer_secret, access_token_key, access_token_secret, screen_name):
        self.api = twitter.Api(consumer_key=consumer_key, consumer_secret=consumer_secret,
                               access_token_key=access_token_key, access_token_secret=access_token_secret)
        print(self.api.VerifyCredentials())
        self.screen_name = screen_name
        print(screen_name)

    def get_tweets(self):
        timeline = self.api.GetUserTimeline(screen_name=self.screen_name, count=1)

        return [(tweet_info.text, tweet_info.id) for tweet_info in timeline][0]
