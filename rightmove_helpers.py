#!/usr/bin/env python

import requests
import lxml.html
from lxml.cssselect import CSSSelector

class RightmoveHelper:
    """
    Helper tools for scraping the Rightmove property website.
    """
    BASE_RMID_ENDPOINT = "https://www.rightmove.co.uk/typeAhead/uknostreet/"

    def __init__(self):
        pass

    def loc_to_rmid(self, loc):
        """
        Injective map between London property location (either city or postcode) to proprietary Rightmove location IDs.

        Parameters:
            loc (str):The string representing either UK postcode or city.

        Returns:
            rmid (str):The proprietary Rightmove location ID, a string comprised of integers and special characters.
        """
        req_url = self.BASE_RMID_ENDPOINT
        iterator = 0
        for char in loc:
            if iterator == 2:
                req_url += "/"
                iterator = 0

            req_url += char
            iterator += 1

        res = requests.get(req_url)
        assert res.status_code == 200, "The request to the Rightmove RMID endpoint was unsuccessful."

        data = res.json()
        locations = data["typeAheadLocations"]

        return locations

    def get_property_ids(self, base_search_url):
        """
        Extracts all the property page ids (https://rightmove.co.uk/property/<ID>) for a given Rightmove search page.

        Parameters:
        base_search_url (str):The string representing the Rightmove search URL showing all the rental listings. Note that this should be a URL without the "index" in the URL. This means that the &index=<value> parameter should not be in the URL, but the location identifier (RMID) should be in the URL along with other parameters like property types, keywords, and furnish types. 

        Returns:
            prop_id (list):A list where each element corresponds to a property page ID from the search page.
        """
        NUM_PAGES = 1
        RM_PROPIDS = []
        SEARCH_URL = base_search_url
        for pg in range(NUM_PAGES):
            html = requests.get(SEARCH_URL)
            doc = lxml.html.fromstring(html.content)
            sel = CSSSelector(".propertyCard-anchor")
            ids = [e.get("id") for e in sel(h)]
         
        # use scrapy, filter by xpath, do what ever is needed to get all the links. the index changes page in multiples of 24

        # https://www.rightmove.co.uk/sitemap.xml this sitemap lists all links for all the post codes
        #LIST_ITEM_SELECTOR = "div[id*='property'].l-searchResult"
#        HEADLINE_SELECTOR = "//div/div/div[4]/div[1]/div[2]/a/address/text()"
 #       RENT_SELECTOR = "//div/div/div[3]/div/a/div"
  #      print(response.text)
