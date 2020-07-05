import os
import sys

import nltk
from nltk.corpus import stopwords

from src.main.com.example.viu.tfm.utils.FeaturesCalculator import FeaturesCalculator
from src.main.com.example.viu.tfm.utils.FileReader import FileReader


def get_all_words(cleaned_tokens_list):
    for tokens in cleaned_tokens_list:
        for token in tokens:
            yield token


def get_tweets_for_model(cleaned_tokens_list):
    for tweet_tokens in cleaned_tokens_list:
        yield dict([token, True] for token in tweet_tokens)


if __name__ == "__main__":
    nltk.download('twitter_samples')
    nltk.download("stopwords")
    nltk.download('averaged_perceptron_tagger')
    nltk.download('wordnet')
    nltk.download('punkt')
    abs_dir = os.path.dirname(__file__)
    senti_dir = abs_dir + "\\resources\\SentiWordNet.txt"

    tra_tra_texts_dir_normal = abs_dir + "\\resources\\dataset\\texts"
    tra_label_dir = abs_dir + "\\resources\\dataset\\label"

    stop_words = set(stopwords.words())

    lectorTraining = FileReader(senti_dir, stop_words)
    lectorTraining.createSetTexts(tra_tra_texts_dir_normal)
    lectorTraining.createSetEtiquetas(tra_label_dir, '"false"')

    featuresWritter = FeaturesCalculator(lectorTraining.tweets)
    featuresWritter.calculateBigramOccurrences()
    featuresWritter.deleteBigrams(3, sys.maxsize)
    featuresWritter.writeFeatures(lectorTraining.tweets, "objective_training.arff", "objective_ngrams.csv")