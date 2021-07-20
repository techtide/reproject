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
        RM_PROPIDS = []
        SEARCH_URL = base_search_url

        html = requests.get(SEARCH_URL)
        doc = lxml.html.fromstring(html.content)

        NUM_SCRAPED = 0
        TOTAL_RESULTS = int(doc.xpath("//div[@id='searchHeader']/span/text()")[0].replace(",", ""))
        print(TOTAL_RESULTS, "properties to scrape...")

        prev_idcol_count = 1    # The number of IDs collected in the previous iteration.

        # TODO: This solution is not very elegant. Refactor later whenever I have energy. View previous Git commits.
        # TODO: This solution does not scrape all the properties. Needs to be fixed.
        while prev_idcol_count > 0:
            html = requests.get(SEARCH_URL)
            doc = lxml.html.fromstring(html.content)
            sel = CSSSelector(".propertyCard-anchor")
            ids = [e.get("id")[4:] for e in sel(doc)]   # Slice starting from index 4 onwards to avoid the "prop" prefix.
            prev_idcol_count = len(ids)
            
            RM_PROPIDS += ids

            print(NUM_SCRAPED)
            NUM_SCRAPED += len(ids) - 1
            SEARCH_URL = base_search_url + "&index=" + str(NUM_SCRAPED)
        
        assert len(RM_PROPIDS) > 0

        print(len(RM_PROPIDS), "properties successfully scraped. Poggers!")

        return list(set(RM_PROPIDS))    # Shorthand to quickly remove duplicate RM property IDs from the list.
