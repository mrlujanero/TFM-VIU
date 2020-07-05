# coding: utf8

class FeaturesCalculator:

    def __init__(self, training_dataset):
        self.bigram_dic = {}
        self.training_tweets = training_dataset
        self.bigram_occurrences = {}
        self.bigram_names = []

    def calculateBigramOccurrences(self):
        for archivo in self.training_tweets.values():
            for tweet_info in archivo:
                features = tweet_info[0]
                bigrams = features[0]
                for bigram in bigrams:
                    if bigram not in self.bigram_occurrences:
                        self.bigram_occurrences[bigram] = 1
                    else:
                        self.bigram_occurrences[bigram] += 1

    def deleteBigrams(self, min_amount, max_amount):
        index = 0
        for (key, value) in self.bigram_occurrences.items():
            if value > min_amount and value < max_amount:
                self.bigram_dic[key] = index
                index += 1
                self.bigram_names.append(key)

    def writeFeatures(self, dataset, features_vector_output_file, ngrams_file):
        features_output = open(features_vector_output_file, 'w', encoding="utf-8")
        ngrams_output = open(ngrams_file, 'w', encoding="utf-8")

        features_output.write("@relation pol" + "\n")
        features_output.write("\n")
        for bigram_name in self.bigram_names:
            str1 = bigram_name[0]
            str2 = bigram_name[1]
            if ("\\" in str1):
                str1 = str1.replace("\\", "\\\\")
            if ("\\" in str2):
                str2 = str2.replace("\\", "\\\\")
            features_output.write("@attribute \"" + str1 + "_" + str2 + "\" numeric" + "\n")
            ngrams_output.write(str1 + ";" + str2 + "\n")

        ngrams_output.close()

        features_output.write("@attribute posvalues numeric" + "\n")
        features_output.write("@attribute negvalues numeric" + "\n")
        features_output.write("@attribute objvalues numeric" + "\n")
        features_output.write("@attribute upperwords numeric" + "\n")
        features_output.write("@attribute repetitions numeric" + "\n")
        features_output.write("@attribute entitymention {True,False}" + "\n")
        features_output.write("@attribute polarity {\"positive\",\"negative\"}" + "\n")  # ,\"neutral\"
        features_output.write("\n")
        features_output.write("@data\n")

        for (archivo, tweet_info_list) in dataset.items():
            for tweet_info in tweet_info_list:
                features = tweet_info[0]
                uppercase_tokens_count = features[1]
                reduced_length_tokens = features[2]
                pos_values = features[3]
                neg_values = features[4]
                obj_values = features[5]
                entity_mention = features[6]
                polarity = tweet_info[1]
                bigrams = features[0]
                bigramOccurrences = self.bigramOccurencesVector(bigrams)
                for found in bigramOccurrences:
                    features_output.write(str(found) + ",")
                features_output.write(str(pos_values) + ",")
                features_output.write(str(neg_values) + ",")
                features_output.write(str(obj_values) + ",")
                features_output.write(str(uppercase_tokens_count) + ",")
                features_output.write(str(reduced_length_tokens) + ",")
                features_output.write(str(entity_mention) + ",")
                features_output.write(polarity + "\n")

    def bigramOccurencesVector(self, bigrams):
        dicZeros = [0] * len(self.bigram_dic)
        for bigram in bigrams:
            if (bigram in self.bigram_dic):
                dicZeros[self.bigram_dic[bigram]] = 1

        return dicZeros
