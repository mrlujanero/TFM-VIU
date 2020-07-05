# coding: utf8

from os import listdir

from src.main.com.example.viu.tfm.utils.Preprocessor import Preprocessor


class FileReader:

    def __init__(self, senti_dir, stop_words):
        self.tweets = {}
        self.normalizer = Preprocessor(senti_dir)
        self.stop_words = stop_words

    def createSetEtiquetas(self, label_dir, opinionated=(['"true"', '"false"'])):
        for archivo_training in listdir(label_dir):
            if ".dat" in archivo_training:
                self.leerEtiquetasTweets(label_dir + "\\" + archivo_training, opinionated)
            else:
                self.createSetEtiquetas(label_dir + "\\" + archivo_training, opinionated)

    def createSetTexts(self, texts_dir):
        for archivo_training in listdir(texts_dir):
            if ".dat" in archivo_training:
                self.leerTextosTweets(texts_dir + "\\" + archivo_training)
            else:
                self.createSetTexts(texts_dir + "\\" + archivo_training)

    def leerTextosTweets(self, nombre_fichero):

        archivo = open(nombre_fichero, mode='r', encoding="utf-8")
        name = nombre_fichero.split("\\")[-1]
        self.tweets[name] = []
        first = True
        for line in archivo:
            if first:
                first = False
                continue
            elif len(line.strip()) > 0 and len(line.split("\t")) == 4:
                self.tweets[name].append([line.split("\t")[3]])
        archivo.close()

    def leerEtiquetasTweets(self, nombre_fichero, opinionated):

        archivo = open(nombre_fichero, mode='r', encoding="utf-8")
        name = nombre_fichero.split("\\")[-1]

        i = 0
        first = True
        for line in archivo:
            if (first):
                first = False
                continue
            if len(line.strip()) > 0 and len(line.split("\t")) >= 7:
                info = line.split("\t")
                "Polarity"
                if info[3] == "\"neutral\"" or info[6] not in opinionated:
                    del self.tweets[name][i]
                    i -= 1
                else:
                    self.tweets[name][i].append(info[3])
                    self.tweets[name][i][0] = self.normalizer.preprocess(self.tweets[name][i][0], self.stop_words, name)
                i += 1
