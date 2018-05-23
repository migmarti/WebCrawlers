import nltk
import os
import io

basepath = '/home/mig/WebCrawlers/WebCrawlers/NewsArticles/'

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


def main():
    totaltext = ""
    filepaths = getFilepaths(basepath)
    for filepath in filepaths:
        print("Processing: " + str(filepath))
        text = readFile(filepath)
        tokens = tokenizeText(text)
        fdist = getNounFreqDist(tokens)
        words = fdist.most_common()
        word = words[:1][0][0]
        print("Main noun: " + str(word))
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




if __name__ == "__main__":
    main()