import weka.core.serialization as serialization
from weka.classifiers import Classifier
from weka.core.converters import Loader

from utils.FeaturesCalculator import FeaturesCalculator
from utils.Preprocessor import Preprocessor


class TotalClassifier:

    def __init__(self, model_path, senti_path, stop_words, ngrams_path):
        self.loader = Loader(classname="weka.core.converters.ArffLoader")
        self.features_calculator = FeaturesCalculator(ngrams_path)
        self.classifier = Classifier(jobject=serialization.read(model_path))
        self.normalizer = Preprocessor(senti_path)
        self.stop_words = stop_words

    def classify_tweet(self, tweet, polarity = '"positive"'):
        tweet_normalized = self.normalizer.preprocess(tweet, self.stop_words, "")
        self.features_calculator.calculateFeatures(tweet_normalized, "output/tweet_features_total.arff", polarity)
        tweet_features = self.loader.load_file("output/tweet_features_total.arff")
        tweet_features.class_is_last()
        for index, inst in enumerate(tweet_features):
            pred = self.classifier.classify_instance(inst)
            dist = self.classifier.distribution_for_instance(inst)
            print(
                "%d - %s - %s" %
                (index+1,
                 inst.class_attribute.value(int(pred)),
                 str(dist.tolist())))
