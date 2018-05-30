import nltk
import os
import io
from matplotlib import pylab
from nltk.corpus import wordnet as wn
import tkinter as tk
from datetime import datetime

directory = os.getcwd() + '/WebCrawlers'
basepath = directory + '/NewsArticles/'
imagepath = directory + '/Frequencies/'

def getFilepaths(path):
    filepaths = []
    for textfile in os.listdir(path):
        url = path + str(textfile)
        filepaths.append(url)
    return filepaths


def readFile(filepath):
    with io.open(filepath, "r+", encoding="utf-8") as myfile:
        text = myfile.read()
        text = text.encode('ascii', 'ignore')
    return text


def filterWords(tokens):
    stopwords = nltk.corpus.stopwords
    stops = set(stopwords.words("english"))
    filteredtokens = [word for word in tokens if word.lower() not in stops and word.isalpha()]
    #print(filteredtokens)
    return filteredtokens


def tokenizeText(text):
    tokens = nltk.tokenize.word_tokenize(text.lower())
    tokens = filterWords(tokens)
    return tokens


def getTotalFreqDist(tokens):
    fdist = nltk.probability.FreqDist(tokens)
    return fdist


def getNounFreqDist(tokens):
    tagged = nltk.pos_tag(tokens)
    nouns = [word for word, pos in tagged
             if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS')]
    fdist = nltk.probability.FreqDist(nouns)
    return fdist

def filename_generator():
    date = str(datetime.now().date())
    to_return = imagepath + '{0}.png'.format(date)
    return to_return

def my_show():
    return pylab.savefig(filename_generator())


def saveGraph(fdist):
    pylab_orig_show = pylab.show
    pylab.show = my_show
    fdist.plot(10, title=str(datetime.now().date()))
    pylab.show = pylab_orig_show


def main():
    totaltext = ""
    filepaths = getFilepaths(basepath)
    for filepath in filepaths:
        print("\nProcessing: " + str(filepath))
        text = readFile(filepath)
        tokens = tokenizeText(text)
        fdist = getNounFreqDist(tokens)
        words = fdist.most_common(3)
        word = str(words[0][0])
        word2 = str(words[1][0])
        word3 = str(words[2][0])
        print("Most common nouns: " + word + ", " + word2 + ", " + word3)
        """
        try:
            s1 = word + '.n.1'
            s2 = word2 + '.n.1'
            synset = wn.synset(s1).lowest_common_hypernyms(wn.synset(s2))[0]
            print("Lowest common hypernym: " + str(synset))
        except:
            print("Could not get lowest common hypernym.")
        """
        totaltext += text
    tokens = tokenizeText(totaltext)
    fdist1 = getTotalFreqDist(tokens)
    fdist2 = getNounFreqDist(tokens)
    words = fdist1.most_common()
    nouns = fdist2.most_common()
    print("\nTotal Word Frequency\n")
    print(words[:100])
    print("\nTotal Noun Frequency\n")
    print(nouns[:100])
    print("\nFile Quantity: " + str(len(filepaths)))
    saveGraph(fdist2)




if __name__ == "__main__":
    main()