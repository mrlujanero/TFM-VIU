# coding: utf8

class FeaturesCalculator:

    def __init__(self, bigrams_path):
        self.bigram_dic = {}
        self.bigram_occurrences = {}
        self.bigram_names = []
        self.read_bigrams(bigrams_path)

    def read_bigrams(self, bigrams_path):
        archivo = open(bigrams_path, mode='r', encoding="utf-8")
        for line in archivo:
            if len(line.strip()) > 0:
                ngram = line.replace("\n", "").split(";")
                ngram_tuple = (ngram[0], ngram[1])
                self.bigram_names.append(ngram_tuple)
                self.bigram_dic[ngram_tuple] = 0

    def calculateFeatures(self, tweet_info, arff_file, polarity):
        f = open(arff_file, 'w', encoding="utf-8")

        f.write("@relation pol" + "\n")
        f.write("\n")
        for bigram_name in self.bigram_names:
            str1 = bigram_name[0]
            str2 = bigram_name[1]
            if ("\\" in str1):
                str1 = str1.replace("\\", "\\\\")
            if ("\\" in str2):
                str2 = str2.replace("\\", "\\\\")
            f.write("@attribute \"" + str1 + "_" + str2 + "\" numeric" + "\n")

        f.write("@attribute posvalues numeric" + "\n")
        f.write("@attribute negvalues numeric" + "\n")
        f.write("@attribute objvalues numeric" + "\n")
        f.write("@attribute upperwords numeric" + "\n")
        f.write("@attribute repetitions numeric" + "\n")
        f.write("@attribute entitymention {True,False}" + "\n")
        f.write("@attribute polarity {\"positive\",\"negative\"}" + "\n")  # ,\"neutral\"
        f.write("\n")
        f.write("@data\n")

        uppercase_tokens_count = tweet_info[1]
        reduced_length_tokens = tweet_info[2]
        pos_values = tweet_info[3]
        neg_values = tweet_info[4]
        obj_values = tweet_info[5]
        entity_mention = tweet_info[6]
        bigrams = tweet_info[0]
        bigram_occurrences = self.bigramOccurencesVector(bigrams)
        for found in bigram_occurrences:
            f.write(str(found) + ",")
        f.write(str(pos_values) + ",")
        f.write(str(neg_values) + ",")
        f.write(str(obj_values) + ",")
        f.write(str(uppercase_tokens_count) + ",")
        f.write(str(reduced_length_tokens) + ",")
        f.write(str(entity_mention) + ",")
        f.write(polarity + "\n")

    def bigramOccurencesVector(self, bigrams):
        dicZeros = [0] * len(self.bigram_dic)
        for bigram in bigrams:
            if (bigram in self.bigram_dic):
                dicZeros[self.bigram_dic[bigram]] = 1

        return dicZeros
