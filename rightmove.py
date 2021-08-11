#!/usr/bin/env python

import requests
import lxml.html
from lxml.cssselect import CSSSelector
import re
import pandas as pd
from property import Property

class RightmoveHelper:
    """
    Helper tools for scraping the Rightmove property website.
    """

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
        REQ_URL = "https://www.rightmove.co.uk/typeAhead/uknostreet/"
        iterator = 0
        loc = loc.upper()
        for char in loc:
            if iterator == 2:
                REQ_URL += "/"
                iterator = 0

            REQ_URL += char
            iterator += 1

        res = requests.get(REQ_URL)
#        print("Requesting the following endpoint:", REQ_URL)
        assert res.status_code == 200, "The request to the Rightmove RMID endpoint was unsuccessful."

        data = res.json()
        locations = data["typeAheadLocations"]

        return locations

    def scrape_property(self, prop_url):
        """
        Scrapes all details of a property page and returns a Property object.

        Parameters:
        rm_property_id (str):The string representing the Rightmove property ID, retrieved, for example, from the get_property_ids function.

        Returns:
        prop (Property):An object of type Property containing the property details.
        """
        html = requests.get(prop_url)
        doc = lxml.html.fromstring(html.content)

        price = doc.xpath("/html/body/div[@id='root']/div[@class='_38rRoDgM898XoMhNRXSWGq']/div[@class='WJG_W7faYk84nW-6sCBVi']/main[@class='_2cXkMZ35RNYeRkIc77z-4p']/div[@class='_2fFy6nQs_hX4a6WEDR-B-6']/div[@class='_5KANqpn5yboC4UXVUxwjZ']/div[@class='_3Kl5bSUaVKx1bidl6IHGj7']/div[@class='_1gfnqJ3Vtd1z40MlC0MzXu']/span/text()")[0]
        descr = doc.xpath("/html/body/div[@id='root']/div[@class='_38rRoDgM898XoMhNRXSWGq']/div[@class='WJG_W7faYk84nW-6sCBVi']/main[@class='_2cXkMZ35RNYeRkIc77z-4p']/div[@class='OD0O7FWw1TjbTD4sdRi1_']/div[@class='STw8udCxUaBUMfOOZu0iL _3nPVwR0HZYQah5tkVJHFh5']/div/text()")[0]
        bedrooms = doc.xpath("/html/body/div[@id='root']/div[@class='_38rRoDgM898XoMhNRXSWGq']/div[@class='WJG_W7faYk84nW-6sCBVi']/main[@class='_2cXkMZ35RNYeRkIc77z-4p']/div[@class='_4hBezflLdgDMdFtURKTWh']/div[@class='_1u12RxIYGx3c84eaGxI6_b'][2]/div[@class='_3mqo4prndvEDFoh4cDJw_n']/div[@class='_2Pr4092dZUG6t1_MyGPRoL']/div[@class='_1fcftXUEbWfJOJzIUeIHKt']/text()")[0]
        bathrooms = doc.xpath("/html/body/div[@id='root']/div[@class='_38rRoDgM898XoMhNRXSWGq']/div[@class='WJG_W7faYk84nW-6sCBVi']/main[@class='_2cXkMZ35RNYeRkIc77z-4p']/div[@class='_4hBezflLdgDMdFtURKTWh']/div[@class='_1u12RxIYGx3c84eaGxI6_b'][3]/div[@class='_3mqo4prndvEDFoh4cDJw_n']/div[@class='_2Pr4092dZUG6t1_MyGPRoL']/div[@class='_1fcftXUEbWfJOJzIUeIHKt']/text()")[0]
        let_date = doc.xpath("/html/body/div[@id='root']/div[@class='_38rRoDgM898XoMhNRXSWGq']/div[@class='WJG_W7faYk84nW-6sCBVi']/main[@class='_2cXkMZ35RNYeRkIc77z-4p']/div[@class='_21Dc_JVLfbrsoEkZYykXK5']/dl[@class='_2E1qBJkWUYMJYHfYJzUb_r']/div[@class='_2RnXSVJcWbWv4IpBC1Sng6'][1]/dd/text()")[0]
        let_type = doc.xpath("/html/body/div[@id='root']/div[@class='_38rRoDgM898XoMhNRXSWGq']/div[@class='WJG_W7faYk84nW-6sCBVi']/main[@class='_2cXkMZ35RNYeRkIc77z-4p']/div[@class='_21Dc_JVLfbrsoEkZYykXK5']/dl[@class='_2E1qBJkWUYMJYHfYJzUb_r']/div[@class='_2RnXSVJcWbWv4IpBC1Sng6'][2]/dd/text()")[0]
        furnish_type = doc.xpath("/html/body/div[@id='root']/div[@class='_38rRoDgM898XoMhNRXSWGq']/div[@class='WJG_W7faYk84nW-6sCBVi']/main[@class='_2cXkMZ35RNYeRkIc77z-4p']/div[@class='_21Dc_JVLfbrsoEkZYykXK5']/dl[@class='_2E1qBJkWUYMJYHfYJzUb_r']/div[@class='_2RnXSVJcWbWv4IpBC1Sng6'][3]/dd")[0]

        print(RM_URL)

        pass

    def gen_property_urls(self, rmids):
        """
        Returns a generator function which provides an output sequence of property rental URLs.
        
        Parameters:
        rmids (list):The array representning all the RMIDs which neeed to be scraped into accessible rental URLs.

        Returns:
        links (list):The generated array containing the rental URLs.
        """
        BASE_URL = "https://www.rightmove.co.uk/property/"
        for rmid in rmids:
            yield BASE_URL + str(rmid)

    def get_property_ids(self, base_search_url):
        """
        Extracts all the property page ids (https://rightmove.co.uk/property/<ID>) for a given Rightmove search page.

        Parameters:
        base_search_url (str):The string representing the Rightmove search URL showing all the rental listings. Note that this should be a URL without the "index" in the URL. This means that the &index=<value> parameter should not be in the URL, but the location identifier (RMID) should be in the URL along with other parameters like property types, keywords, and furnish types. 

        Returns:
        prop_id (list):A list where each element corresponds to a property page ID from the search page.
        """
        assert type(base_search_url) == str

        RM_PROPIDS = []
        SEARCH_URL = base_search_url

        html = requests.get(SEARCH_URL)
        doc = lxml.html.fromstring(html.content)

        NUM_SCRAPED = 0
        TOTAL_RESULTS = int(doc.xpath("//div[@id='searchHeader']/span/text()")[0].replace(",", ""))
#        print(TOTAL_RESULTS, "properties to scrape...")

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

 #           print(NUM_SCRAPED)
            NUM_SCRAPED += len(ids) - 1
            SEARCH_URL = base_search_url + "&index=" + str(NUM_SCRAPED)
        
        assert len(RM_PROPIDS) > 0

        print(len(RM_PROPIDS), "properties successfully scraped. Poggers!")

        return list(set(RM_PROPIDS))    # Shorthand to quickly remove duplicate RM property IDs from the list.
