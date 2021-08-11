#!/usr/bin/env python

from rightmove import RightmoveHelper
from property import Property
import argparse 

parser = argparse.ArgumentParser("pipeline")
parser.add_argument("location", help="the location from which properties should be scraped from (in plain text)", type=str)
args = parser.parse_args()

class RightmovePipeline:
    def __init__(self, loc):
        self.loc = loc
        helper = RightmoveHelper()
        rmid = helper.loc_to_rmid(loc)[0]["locationIdentifier"]
        # keep in mind radius=
        radius = 1
        search_url = "https://www.rightmove.co.uk/property-to-rent/find.html?searchType=RENT&insId=1&radius=" + str(radius) + "&_includeLetAgreed=on&locationIdentifier=" + str(rmid)
#        print(search_url)
        propids = helper.get_property_ids(search_url)
        url_gen = helper.gen_property_urls(propids)
        for prop_url in url_gen:
            # scrape and save to mongodb
            print(prop_url)
#            property_details = helper.scrape_property(prop_url)
            pass

if __name__ == "__main__":
    pipeline = RightmovePipeline(args.location) 
