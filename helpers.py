#!/usr/bin/env python

import requests

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
