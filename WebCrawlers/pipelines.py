# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import re
import os
from scrapy.exceptions import DropItem
import html2text
import sys
from goose import Goose


class WebcrawlersPipeline(object):
    def process_item(self, item, spider):
        return item

"""
Un filtro para las "publicaciones propias", publicaciones que son solo preguntas de alguien en lugar de vincularse a algo.
"""

class DropSelfPostsPipeline(object):
    def process_item(self, item, spider):
        match = re.match("item\?id=[0-9]+", item["url"])
        if match:
            print("Excluded self-post: " + str(item["url"]))
            raise DropItem("Excluded self-post: " + str(item["url"]))
        return item

class DropInvalidArticlePipeline(object):
    def process_item(self, item, spider):
        item['link_title'] = item['link_title'].encode("utf-8")
        title = item['link_title']
        if ("[" in title.lower() and "]" in title.lower()) or "github" in item["url"]:
            print("Excluded invalid article: " + str(item["link_title"]))
            raise DropItem("Excluded invalid article: " + str(item["link_title"]))
        return item

"""
Metodo para extraer el texto del artículo del enlace y guardarlo en el campo de texto del elemento.
"""

class ExtractArticlePipeline(object):
    def __init__(self):
        self.savePath = os.getcwd() + '/WebCrawlers'
        self.h = html2text.HTML2Text()
        self.h.ignore_links = True
        self.h.ignore_images = True
        self.g = Goose()

    def process_item(self, item, spider):
        try:
            article = self.g.extract(url=item["url"])
            text = article.cleaned_text.encode("utf-8")
            item["text"] = text
            self.save_article(item["link_title"], item["text"])
        except Exception as e:
            print("\n" + str(e))
            print("Line: " + str(sys.exc_info()[-1].tb_lineno) + "\n")
        return item

    """
    def process_item(self, item, spider):
        response = requests.get(item["url"])
        if (response.status_code != 403):
            item["text"] = self.h.handle(response.content)
            self.saveArticle(item["link_title"], item["text"])
        else:
            print("Access is denied for: ", item["link_title"])
        return item
    """

    def save_article(self, title, text):
        if len(text.split()) > 250:
            name = re.sub('[^A-Za-z0-9 ]+', ' ', title)
            path = self.savePath + '/NewsArticles/'
            filename = path + '%s.txt' % name
            with open(filename, 'w') as f:
                f.write(text)
            print("Success: Saved article " + str(name))
        else:
            print("Insufficient text from: " + str(title) + ". Text is empty, too short or prohibited.")