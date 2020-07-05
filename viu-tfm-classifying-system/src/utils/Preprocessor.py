# coding: utf8

import re
import string

import nltk
from nltk.tag import pos_tag
from nltk.tokenize import TweetTokenizer

from constants.Config import entities


class Preprocessor:

    def __init__(self, sentiwordnet):
        self.possmileys = re.compile(':\)|:-\)|: \)|:D|=\)|;\)|; \)|\(:')
        self.negsmileys = re.compile(':\(|:-\(|: \(|\):|\) :')
        self.numbers = re.compile('\\b\\d+(\\.(\\d)+)?\\b')
        self.question = re.compile('\\?|¿')
        self.exclamation = re.compile('!|¡')
        self.uppercase = re.compile('\\b[A-Z]+\\b')
        self.punctuation = re.compile('[\"#$%&()*+,.\/:;<=>\\^{}~]')
        self.nonWords = re.compile("[\W]+")  # [\W]+ [^\\p{L}\\p{Nd}]+
        self.apostrophe1 = re.compile('^\'+')
        self.apostrophe2 = re.compile('\'+$')
        self.spaces = re.compile(' +')
        self.token_inicial = "<s>"
        self.token_final = "</s>"
        self.sentiwordset = {}
        self.leerSentiWord(sentiwordnet)
        self.twtok = TweetTokenizer()

    def preprocess(self, tweet, stop_words=(), archivo=''):
        cleaned_tokens = []
        [lowercase_tweet, uppercase_tokens_count] = self.toLowerCase(tweet)
        reduced_length_tokens = 0
        pos_tokens = 0
        neg_tokens = 0
        obj_tokens = 0
        entity_mention = self.entityMention(tweet, archivo)
        tweet_tokens = self.twtok.tokenize(lowercase_tweet)

        for token, tag in pos_tag(tweet_tokens):
            pos_tokens += self.posValue(token)
            neg_tokens += self.negValue(token)
            obj_tokens += self.objValue(token)
            [tokenstemmed, reduced_length_tokens] = self.normalizeToken(tag, token)
            reduced_length_tokens += reduced_length_tokens
            if len(
                    tokenstemmed) > 0 and tokenstemmed not in string.punctuation and tokenstemmed.lower() not in stop_words:
                cleaned_tokens.append(tokenstemmed.lower())
        tokens_preprocessed = self.anadirTokenIF(cleaned_tokens)
        ngrams = self.calculateBigrams(tokens_preprocessed)
        return (
        ngrams, uppercase_tokens_count, reduced_length_tokens, pos_tokens, neg_tokens, obj_tokens, entity_mention)

    def normalizeToken(self, tag, token):
        tweetnousers = self.changeUsers(token)
        tweetnourls = self.changeURLS(tweetnousers)
        tweetnosmileys = self.detectSmileys(tweetnourls)
        tweetnoqe = self.detectQandE(tweetnosmileys)
        [tokennolength, count] = self.reduceLength(tweetnoqe)
        tweetNoPunct = self.removePunctuation(tokennolength)
        tweetnonumbers = self.detectNumbers(tweetNoPunct)
        porter_stemmer = nltk.PorterStemmer()
        tokenstemmed = porter_stemmer.stem(tweetnonumbers)
        return [tokenstemmed, count]

    def processPosTag(self, tag):
        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'
        return pos

    def changeUsers(self, token):
        if ("@" == token[0]):
            return "USUARIO0"
        return token

    def changeURLS(self, token):
        if ("http" in token):
            return "URL"
        return token

    def detectSmileys(self, token):
        return self.negsmileys.sub("NEGSMILEY",
                                   self.possmileys.sub("POSSMILEY", token)
                                   )

    def detectNumbers(self, token):
        return self.numbers.sub("NUMBER", token)

    def detectQandE(self, tweet):
        return self.exclamation.sub("EXCLAMATIONMARK",
                                    self.question.sub("QUESTIONMARK", tweet)
                                    )

    def toLowerCase(self, tweet):
        upperWords = self.uppercase.findall(tweet)
        return [tweet.lower(), len(upperWords)]

    def anadirTokenIF(self, tweet):
        tweet.append(self.token_final)
        tweet.reverse()
        tweet.append(self.token_inicial)
        tweet.reverse()

        return tweet

    def posValue(self, token):
        if token in self.sentiwordset:
            (pos, neg) = self.sentiwordset[token]
            return pos
        return 0

    def negValue(self, token):
        if token in self.sentiwordset:
            (pos, neg) = self.sentiwordset[token]
            return neg
        return 0

    def objValue(self, token):
        if token in self.sentiwordset:
            (pos, neg) = self.sentiwordset[token]
            return 1 - (pos + neg)
        return 0

    def removePunctuation(self, token):
        token = self.punctuation.sub(" ", token)
        outputtoken = ""

        newtoken = self.apostrophe1.sub("", token)
        newtoken = self.apostrophe2.sub("", newtoken)
        outputtoken += " " + newtoken

        outputtoken = outputtoken.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú",
                                                                                                                  "u")
        outputtoken = outputtoken.replace("à", "a").replace("è", "e").replace("ì", "i").replace("ò", "o").replace("ù",
                                                                                                                  "u")
        outputtoken = self.nonWords.sub(" ", outputtoken)
        outputtoken = self.spaces.sub(" ", outputtoken)

        return outputtoken.strip()

    def reduceLength(self, token):

        numberofwords = 0

        actualchar = ''
        counter = 0
        newword = ''
        new = True
        for char in token:
            if actualchar == char:
                counter += 1
            else:
                actualchar = char
                counter = 1
            if counter <= 3:
                newword += char
            elif new:
                new = False
                numberofwords += 1

        return [newword, numberofwords]

    def leerSentiWord(self, path):
        archivo = open(path, 'r')
        for line in archivo:
            words = line.split("\t")[4].split()
            for word in words:
                key = word.split("#")[0]
                self.sentiwordset[key] = (int(line[2]), int(line[3]))

    def entityMention(self, tweet, archivo):
        if (archivo in entities):
            entity = entities[archivo]
            for word in entity:
                if (word in tweet):
                    return True
        return False

    def calculateBigrams(self, tweetIF):
        ngrams = nltk.bigrams(tweetIF)
        return [bigram for bigram in ngrams]

    def turnFeaturesIntoDict(self, features):
        return dict([feature, True] for feature in features)
