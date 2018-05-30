from sklearn.datasets import fetch_20newsgroups
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import numpy as np
import scipy
import os
import io
import shutil
import re

directory = os.getcwd() + '/WebCrawlers'
inputpath = directory + '/NewsArticles/'
inputpath2 = directory + '/NewsArticles(Dates)/'
outputpath = directory + '/SortedNewsArticles/'
outputpath2 = directory + '/SortedNewsArticles(Dates)/'

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
    return text.decode('utf-8')


def train(classifier, X, y):
    print("Training classifier...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=33)
    classifier.fit(X_train, y_train)
    print("Training has finished. Accuracy: %s" % classifier.score(X_test, y_test))
    return classifier


def sort_article(title, text, path):
    filename = path + '/%s' % title
    with open(filename, 'w') as f:
        f.write(text)
    print("Success: Sorted article " + str(title))


def predict_genre(classifier, text):
    if len(re.findall('(\$ *\d+|currency|bank|money|econom)', text)) > 5:
        genre = 'Economics'
    elif len(re.findall('game|movie', text)) > 5:
        genre = 'Recreational'
    elif len(re.findall('government|law', text)) > 3:
        genre = 'Politics'
    else:
        genreIndex = classifier.predict([text])
        genre = str(categories[genreIndex][0])
    print("Predicted genre: " + genre)
    return genre


if __name__ == "__main__":
    if os.path.exists(outputpath):
        shutil.rmtree(outputpath)
    if os.path.exists(outputpath2):
        shutil.rmtree(outputpath2)

    training = fetch_20newsgroups(subset='all',
                                  remove=('headers', 'footers', 'quotes'))

    trial = Pipeline([
        ('vectorizer', TfidfVectorizer(stop_words=stopwords.words('english'))),
        ('classifier', MultinomialNB(alpha=0.05)),
    ])

    #print(training.target_names)
    # ['alt.atheism', 'comp.graphics', 'comp.os.ms-windows.misc', 'comp.sys.ibm.pc.hardware', 'comp.sys.mac.hardware', 'comp.windows.x', 'misc.forsale', 'rec.autos', 'rec.motorcycles', 'rec.sport.baseball', 'rec.sport.hockey', 'sci.crypt', 'sci.electronics', 'sci.med', 'sci.space', 'soc.religion.christian', 'talk.politics.guns', 'talk.politics.mideast', 'talk.politics.misc', 'talk.religion.misc']

    genres = ['Religion', 'Computer Engineering', 'Computer Engineering', 'Computer Engineering', 'Computer Engineering', 'Computer Engineering', 'Recreational', 'Recreational', 'Recreational', 'Recreational', 'Recreational', 'Technology', 'Technology', 'Science', 'Science', 'Recreational', 'Politics', 'Politics', 'Politics', 'Religion']

    classifier = train(trial, training.data, training.target)
    categories = np.array(genres)
    dist = {}

    filepaths = getFilepaths(inputpath)
    for filepath in filepaths:
        print("\nProcessing: " + str(filepath))
        text = readFile(filepath)
        genre = predict_genre(classifier, text)
        path = str(outputpath + genre)
        if not os.path.exists(path):
            os.makedirs(path)
            dist[genre] = 1
        title = os.path.basename(filepath)
        sort_article(title, text, path)
        dist[genre] += 1

    dirs = getFilepaths(inputpath2)
    for dir in dirs:
        date = dir[-10:]
        filepaths = getFilepaths(dir + "/")
        for filepath in filepaths:
            print(filepath)
            text = readFile(filepath)
            genre = predict_genre(classifier, text)
            path = str(outputpath2 + date + "/" + genre)
            if not os.path.exists(path):
                os.makedirs(path)
            title = os.path.basename(filepath)
            sort_article(title, text, path)



    print("Results: ")
    print(str(dist))


