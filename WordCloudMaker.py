import numpy as np
from PIL import Image
import os
import matplotlib.pyplot as plt
import random

from wordcloud import WordCloud, STOPWORDS

basepath = os.getcwd() + '/WebCrawlers'
newsfolderpath = basepath + '/SortedNewsArticles'
imagesfolderpath = basepath + '/DefaultImages'

def grey_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return "hsl("+random.randint(0, 180)+", "+random.randint(0, 100)+"%%, "+random.randint(50, 100)+"%%)"

def getFilepaths(path):
    filepaths = {}
    for textfile in os.listdir(path):
        if(str(textfile)!='.DS_Store'):
            filepaths[str(textfile)] = path + '/' + str(textfile)
    return filepaths

def readFile(filepath):
    with io.open(filepath, "r+", encoding="utf-8") as myfile:
        text = myfile.read()
        text = text.encode('ascii', 'ignore')
    return text

FoldersPaths = getFilepaths(newsfolderpath)
ImagesPath = getFilepaths(imagesfolderpath)

for path in FoldersPaths:
    print(path + ' : ' + FoldersPaths[path])

mask = np.array(Image.open(path.join(d, "stormtrooper_mask.png")))

text = open(path.join(d, 'a_new_hope.txt')).read()

text = text.replace("HAN", "Han")
text = text.replace("LUKE'S", "Luke")

stopwords = set(STOPWORDS)
stopwords.add("int")
stopwords.add("ext")

wc = WordCloud(max_words=1000, mask=mask, stopwords=stopwords, margin=10,
               random_state=1).generate(text)

default_colors = wc.to_array()
plt.imshow(wc.recolor(color_func=grey_color_func, random_state=3),
           interpolation="bilinear")
wc.to_file("a_new_hope.png")
plt.axis("off")
plt.figure()
