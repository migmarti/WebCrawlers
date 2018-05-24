import numpy as np
from PIL import Image
import os
import io
import matplotlib.pyplot as plt
import random

from wordcloud import WordCloud, STOPWORDS

basepath = os.getcwd() + '/WebCrawlers'
newsfolderpath = basepath + '/SortedNewsArticles'
imagesfolderpath = basepath + '/DefaultImages'
outputpath = os.getcwd() + '/WordClouds/'

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

FoldersPaths = getFilepaths(newsfolderpath)
ImagesPath = getImageFilepaths(imagesfolderpath)

for category in FoldersPaths:
    fullText = ''
    imagePath = ImagesPath[category]
    newsFiles = getFilepaths(FoldersPaths[category])
    for news in newsFiles:
        fullText += str(readFile(newsFiles[news]))
    mask = np.array(Image.open(imagePath))
    stopwords = set(STOPWORDS)
    stopwords.add("int")
    stopwords.add("ext")
    wc = WordCloud(max_words=1000, mask=mask, stopwords=stopwords, margin=10,
                   random_state=1).generate(fullText)
    default_colors = wc.to_array()
    plt.imshow(default_colors, interpolation="bilinear")
    wc.to_file(outputpath+category+".png")
    plt.axis("off")
    plt.figure()
    fullText = ''

