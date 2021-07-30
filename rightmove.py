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
        print("Requesting the following endpoint:", REQ_URL)
        assert res.status_code == 200, "The request to the Rightmove RMID endpoint was unsuccessful."

        data = res.json()
        locations = data["typeAheadLocations"]

        return locations

    def scrape_property(self, rm_property_id):
        """
        Scrapes all details of a property page and returns a Property object.

        Parameters:
        rm_property_id (str):The string representing the Rightmove property ID, retrieved, for example, from the get_property_ids function.

        Returns:
        prop (Property):An object of type Property containing the property details.
        """
        RM_URL = "https://www.rightmove.co.uk/properties/" + str(rm_property_id) + "#/"
        
        html = requests.get(RM_URL)
        doc = lxml.html.fromstring(html.content)

       DISPLAYADDRESS_XPATH = "//h1[@itemprop='streetAddress']"
       PRICE_XPATH = "//html/body/div[2]/div/div[3]/main/div[2]/div/div/div/span"
       PROPERTYTYPE_XPATH = "//div[@data-test='infoReel']/div[1]/div[2]" 
       BEDROOMS_XPATH = "//div[@data-test='infoReel']/div[2]/div[2]"
       BATHROOMS_XPATH = "//div[@data-test='infoReel']/div[3]/div[2]"
       PROPERTYDESCRIPTION_XPATH = "//html/body/div[2]/div/div[3]/main/div[10]/div/div"
       MAPIMGSRC_XPATH =  "//html/body/div[2]/div/div[3]/main/div[16]/div/a/img/@src"
       LATITUDE_REGEX = re.compile(r"(latitude=)(.*)&l")
       LONGITUDE_REGEX = re.compile(r"(longitude=)(.*)&" )
       NUM_FLOORPLANS_XPATH= "//html/body/div[2]/div/div[3]/main/div[8]/div[1]/a/span"

       PRICEAMOUNT = str(doc.xpath(PRICE_XPATH)[0])
       DISPLAYADDRESS = str(doc.xpath(DISPLAYADDRESS_XPATH)[0])
       PROPERTYTYPE = str(doc.xpath(PROPERTYTYPE_XPATH)[0])
       BEDROOMS = str(doc.xpath(BEDROOMS_XPATH)[0])
       PROEPRTYDESCRIPTION = str(doc.xpath(PROPERTYDESCRIPTION_XPATH)[0])
       BATHROOMS = str(doc.xpath(BATHROOMS_XPATH)[0])
       MAPIMGSRC = str(doc.xpath(IMGSRC_XPATH)[0])
       LONGITUDE = int(LONGITUDE_REGEX.match(MAPIMGSRC)[2])
       LATITUDE = int(LATITUDE_REGEX.match(MAPIMGSRC)[2])
       NUMFLOORPLANS = int(doc.xpath(NUM_FLOORPLANS_XPATH)[0])
       
       fp_urls = []

       FLOORPLAN_IMAGE_XPATH = "//html/body/div[2]/div/div[2]/div[2]/div/div/div/div[2]/div/img/@src"

       if NUMFLOORPLANS > 0:
           for fpi in range(NUMFLOORPLANS):
               d = lxml.html.fromstring(requests.get("https://www.rightmove.co.uk/properties/" + str(rm_property_id) + "#/floorplan?activePlan=1"))  
               fp_src = str(d.xpath(FLOORPLAN_IMAGE_XPATH)[0])
               fp_urls.append(fp_src)

       NUM_IMAGES_XPATH = "//html/body/div[2]/div/div[3]/main/div[8]/div[2]/a[7]"
       NUMIMGS = int(str(doc.xpath(NUM_IMAGES_XPATH)[0]).replace("+",""))
       
       img_urls = []

       if NUMIMGS > 0:
           for nimg in range(NUMIMGS):
               d = lxml.html.fromstring(requests.get("https://www.rightmove.co.uk/properties/" + str(rm_property_id) + "#/media?id=media" + str(nimg)))
               IMG_XPATH = "//html/body/div[2]/div/div[2]/div[2]/div/div/div[4]/div/div/img/@src"
               img_src = str(d.xpath(IMG_XPATH)[0])
               img_urls.append(img_src)

        return Property(headline=DISPLAYADDRESS, lonlat=(LONGITUDE, LATITUDE), descr=PROPERTYDESCRIPTION, rent=PRICEAMOUNT, rooms=(BEDROOMS, BATHROOMS), fp_url=fp_urls, gallery=img_urls)
    
    def gen_property_urls(self, rmids):
        """
        Returns a generator function which provides an output sequence of property rental URLs.
        
        Parameters:
        rmids (list):The array representning all the RMIDs which neeed to be scraped into accessible rental URLs.

        Returns:
        links (list):The generated array containing the rental URLs.
        """
        BASE_URL = "https://www.rightmove.co.uk/property-to-rent/find.html?searchType=RENT&locationIdentifier="
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
