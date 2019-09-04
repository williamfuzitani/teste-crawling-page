# response.css('div.brand-listing-container-frontpage a').getall()

import scrapy

class BrickSetSpider(scrapy.Spider):
     name = "brickset_spider"
     start_urls = ['https://www.evspecifications.com/']

     def parse(self, response):
          SET_SELECTOR = 'div.brand-listing-container-frontpage a'

          for brickset in response.css(SET_SELECTOR):
               NAME_SELECTOR = 'a ::text'
               PAGE_SELECTOR = 'a ::attr(href)'
               yield {
                    'name': brickset.css(NAME_SELECTOR).extract_first(),
                    'page': brickset.css(PAGE_SELECTOR).extract_first(),
               }