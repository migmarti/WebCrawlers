# -*- coding: utf-8 -*-
import scrapy
import json

"""
scrapy crawl name
scrapy shell 'http://quotes.toscrape.com/page/1/'
"""


class TestSpider(scrapy.Spider):
    name = 'test'
    basePath = '/home/mig/WebCrawlers/WebCrawlers/'

    """
    Devuelve un iterable de Requests de la cual la Araña comenzará a rastrear. 
    Las solicitudes posteriores se generarán sucesivamente a partir de estas solicitudes iniciales.
    """

    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]
        print("Starting from: ")
        for url in urls:
            print(url)
            yield scrapy.Request(url=url, callback=self.parse)


    """
    Un método que se llamará para manejar la respuesta descargada para cada una de las solicitudes realizadas. 
    El parámetro de respuesta es una instancia de TextResponse que contiene el contenido de la página y tiene otros 
    métodos útiles para manejarlo.

    El método parse () normalmente analiza la respuesta, extrae los datos recortados como dicts y también encuentra 
    nuevas URL para seguir y crear nuevas solicitudes (Request) de ellos.
    """

    def parse(self, response):

        quoteObjects = []

        for quote in response.css('div.quote'):
            quoteObject = {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.css('small.author::text').extract_first(),
                'tags': quote.css('div.tags a.tag::text').extract(),
            }
            quoteObjects.append(quoteObject)

        self.saveObjectList(response, quoteObjects)
        self.savePage(response)
        print("")

        """
        Araña modificada para seguir recursivamente el enlace a la página siguiente, extrayendo datos de ella.
        """

        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            link = response.follow(next_page, callback=self.parse)
            print("Following: ", link)
            yield link

    def saveObjectList(self, response, objectList):
        page = response.url.split("/")[-2]
        path = self.basePath + 'SavedObjects/'
        filename = path + 'object-%s.txt' % page
        with open(filename, 'wb') as f:
            json.dump(objectList, f)
        self.log('Saved file %s' % filename)
        print("Saved Objects: ", filename)

    def savePage(self, response):
        page = response.url.split("/")[-2]
        path = self.basePath + 'ScrapedPages/'
        filename = path + 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
        print("Saved Page: ", filename)
