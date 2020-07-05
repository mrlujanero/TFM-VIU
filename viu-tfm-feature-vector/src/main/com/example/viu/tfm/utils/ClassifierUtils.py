import collections

import nltk
from nltk.classify.scikitlearn import SklearnClassifier
from nltk.metrics.scores import f_measure
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier


class ClassifierUtils:

    def __init__(self, train_data, test_data, stop_words):
        self.train_data = train_data
        self.test_data = test_data
        self.stop_words = stop_words

    def classify(self):
        naiveBayesClassif = nltk.classify.NaiveBayesClassifier.train(self.train_data)
        self.showResults(naiveBayesClassif, "NaiveBayesClassifier")

        sklearn1 = SklearnClassifier(LinearSVC())
        sklearn1.train(self.train_data)
        self.showResults(sklearn1, "LinearSVC")

        sklearn2 = SklearnClassifier(DecisionTreeClassifier())
        sklearn2.train(self.train_data)
        self.showResults(sklearn2, "DecisionTreeClassifier")

        sklearn3 = SklearnClassifier(MLPClassifier())
        sklearn3.train(self.train_data)
        self.showResults(sklearn3, "MLPClassifier")

        sklearn4 = SklearnClassifier(KNeighborsClassifier())
        sklearn4.train(self.train_data)
        self.showResults(sklearn4, "KNeighborsClassifier")

        sklearn5 = SklearnClassifier(LogisticRegression())
        sklearn5.train(self.train_data)
        self.showResults(sklearn5, "LogisticRegression")

        sklearn6 = SklearnClassifier(KMeans(n_clusters=2, max_iter=10000))
        sklearn6.train(self.train_data)
        self.showResults(sklearn6, "KMeans")

    def showResults(self, classif, clasificador):
        refsets = collections.defaultdict(set)
        testsets = collections.defaultdict(set)
        for i, (feats, label) in enumerate(self.test_data):
            refsets[label].add(i)
            observed = classif.classify(feats)
            testsets[observed].add(i)
        print("F1 Score del clasificador:", clasificador, f_measure(refsets['"positive"'], testsets['"positive"']))

    def customAnalyzerTFIDF(self, tweet_features_and_class):
        aux_feature_array = []
        no_ngrams_features = set(
            ["uppercase_tokens_count", "reduced_length_tokens", "pos_tokens", "neg_tokens", "obj_tokens",
             "entity_mention"])
        features = tweet_features_and_class[0]
        for (pair1, pair2), boolean_value in features.items():
            if pair1 not in no_ngrams_features:
                aux_feature_array.append((pair1, pair2))
        return aux_feature_array

    def generateBOWCluster(self, tweet_features_and_class):
        pass
