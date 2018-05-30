import numpy as np
from PIL import Image
import os
import io
import matplotlib.pyplot as plt
import random
import nltk

from wordcloud import WordCloud, STOPWORDS

basepath = os.getcwd() + '/WebCrawlers'
newsfolderpath = basepath + '/SortedNewsArticles'
imagesfolderpath = basepath + '/DefaultImages'
outputpath = basepath + '/WordClouds/'

def grey_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return "hsl("+random.randint(0, 180)+", "+random.randint(0, 100)+"%%, "+random.randint(50, 100)+"%%)"

def getFilepaths(path):
    filepaths = {}
    for textfile in os.listdir(path):
        if(str(textfile)!='.DS_Store'):
            filepaths[str(textfile)] = path + '/' + str(textfile)
    return filepaths

def getImageFilepaths(path):
    filepaths = {}
    for textfile in os.listdir(path):
        if(str(textfile)!='.DS_Store'):
            filepaths[str(textfile[:-4])] = path + '/' + str(textfile)
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

def getNouns(text):
    tokens = tokenizeText(text)
    tagged = nltk.pos_tag(tokens)
    nouns = [word for word, pos in tagged
             if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS')]
    return ' '.join(nouns)

FoldersPaths = getFilepaths(newsfolderpath)
ImagesPath = getImageFilepaths(imagesfolderpath)

for category in FoldersPaths:
    print("Processing category: " + str(category))
    fullText = ''
    imagePath = ImagesPath[category]
    newsFiles = getFilepaths(FoldersPaths[category])
    for news in newsFiles:
        fullText += str(readFile(newsFiles[news]))
    fullText = getNouns(fullText)
    mask = np.array(Image.open(imagePath))
    #stopwords = set(STOPWORDS)
    #stopwords.add("int")
    #stopwords.add("ext")
    print("Creating wordcloud...")
    wc = WordCloud(max_words=1000, mask=mask,
                   #stopwords=stopwords,
                   margin=10,
                   random_state=1).generate(fullText)
    default_colors = wc.to_array()
    plt.imshow(default_colors, interpolation="bilinear")
    filename = outputpath + category + ".png"
    wc.to_file(filename)
    print("Saved Wordcloud: " + str(filename))
    plt.axis("off")
    plt.figure()

