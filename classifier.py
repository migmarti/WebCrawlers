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

inputpath = '/home/mig/WebCrawlers/WebCrawlers/NewsArticles/'
outputpath = '/home/mig/WebCrawlers/WebCrawlers/SortedNewsArticles/'

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
    print("Success: Sorted article " + str(title) + "\n")


if __name__ == "__main__":
    if os.path.exists(outputpath):
        shutil.rmtree(outputpath)

    training = fetch_20newsgroups(subset='all')

    trial = Pipeline([
        ('vectorizer', TfidfVectorizer(stop_words=stopwords.words('english'))),
        ('classifier', MultinomialNB(alpha=0.05)),
    ])

    #print(training.target_names)
    # ['alt.atheism', 'comp.graphics', 'comp.os.ms-windows.misc', 'comp.sys.ibm.pc.hardware', 'comp.sys.mac.hardware', 'comp.windows.x', 'misc.forsale', 'rec.autos', 'rec.motorcycles', 'rec.sport.baseball', 'rec.sport.hockey', 'sci.crypt', 'sci.electronics', 'sci.med', 'sci.space', 'soc.religion.christian', 'talk.politics.guns', 'talk.politics.mideast', 'talk.politics.misc', 'talk.religion.misc']

    genres = ['Religion', 'Technology', 'Technology', 'Technology', 'Technology', 'Technology', 'Miscellaneous', 'Recreation', 'Recreation', 'Recreation', 'Recreation', 'Science', 'Technology', 'Biology', 'Science', 'Social Commentary', 'Politics', 'Politics', 'Politics', 'Religion']

    classifier = train(trial, training.data, training.target)
    categories = np.array(genres)

    filepaths = getFilepaths(inputpath)
    for filepath in filepaths:
        print("Processing: " + str(filepath))
        text = readFile(filepath)
        genreIndex = classifier.predict([text])
        genre = str(categories[genreIndex][0])
        print("Predicted genre: " + genre)
        path = str(outputpath + genre)
        if not os.path.exists(path):
            os.makedirs(path)
        title = os.path.basename(filepath)
        sort_article(title, text, path)


