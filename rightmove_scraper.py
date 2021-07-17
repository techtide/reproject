#!/usr/bin/env python

import scrapy

class RMFindPropertySpider(scrapy.Spider):
    """
    The RMFindPropertySpider inherits Scrapy's Spider class and is intended to crawl the property search results page.
    :param start_urls:The list of starting pages to crawl. These should be search result pages.
    :type start_urls:list
    """
    name = "rightmove_find_property_spider"
    def __init__(self, **kwargs):
#        self.start_urls = [start_url]
        self.start_urls = ["https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=POSTCODE%5E913161&radius=15.0&propertyTypes=&includeSSTC=false&mustHave=&dontShow=&furnishTypes=&keywords="]
        super().__init__(**kwargs)
    
    def parse(self, response):
        '''Continuously parses each list item from the real estate search engine.''' 
        LIST_ITEM_SELECTOR = "div[id*='property'].l-searchResult"
        HEADLINE_SELECTOR = "//div/div/div[4]/div[1]/div[2]/a/address/text()"
        RENT_SELECTOR = "//div/div/div[3]/div/a/div"
        print(response.text)
