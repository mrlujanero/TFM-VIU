import os
import sys
import traceback

import nltk
from nltk.corpus import stopwords

from classifiers.ObjectiveClassifier import ObjectiveClassifier
from classifiers.TotalClassifier import TotalClassifier

import weka.core.jvm as jvm

from constants import TwitterConstants
from twitter_utils.TwitterConnector import TwitterConnector

import time

def fetch_and_classify_last_tweet():
    pass

if __name__ == "__main__":

    nltk.download('twitter_samples')
    nltk.download("stopwords")
    nltk.download('averaged_perceptron_tagger')
    nltk.download('wordnet')
    nltk.download('punkt')

    abs_dir = os.path.dirname(__file__)

    models_path = abs_dir + "/resources/modelos"
    senti_dir = abs_dir + "/resources/SentiWordNet.txt"

    total_model = abs_dir + "/resources/modelos/total_model.model"
    total_ngrams = abs_dir + "/resources/ngrams/total_ngrams.csv"

    objective_model = abs_dir + "/resources/modelos/objective_model.model"
    objective_ngrams = abs_dir + "/resources/ngrams/objective_ngrams.csv"

    stop_words = set(stopwords.words())

    try:
        jvm.start()
        last_tweet_id = ""
        total_classifier = TotalClassifier(total_model, senti_dir, stop_words, total_ngrams)
        objective_classifier = ObjectiveClassifier(objective_model, senti_dir, stop_words, objective_ngrams)

        twitter_connector = TwitterConnector(TwitterConstants.consumer_key,
                                             TwitterConstants.consumer_secret,
                                             TwitterConstants.access_token_key,
                                             TwitterConstants.access_token_secret,
                                             "ramon_lujan")

        while True:
            print("polling...")
            (tweet_text, tweet_id) = twitter_connector.get_tweets()
            if last_tweet_id != tweet_id:
                print("classifying tweet: ", tweet_text)
                print("clasificacion modelo total")
                total_classifier.classify_tweet(tweet_text)
                print("clasificacion modelo objetivo")
                objective_classifier.classify_tweet(tweet_text)
                last_tweet_id = tweet_id
            time.sleep(15)


    except Exception as e:
        print(traceback.format_exc())
    finally:
        jvm.stop()

