#!/usr/bin/env python

class Property:
    """
    The Property object is a container which holds all the information points about a particular property.
    :param headline: The headline, human-readable description of where the property is located.
    :type headline: str
    :param lonlat: Tuple containing the geographic location of the property in terms of (Longitude, Latitude).  
    :type lonlat: tup
    :param descr: The written description provided by the property site.
    :type descr: str
    :param rent: The rental price. 
    :type rent: int
    :param rooms: Tuple in the format (No. of Bedrooms, No. of Bathrooms).
    :type rooms: tup
    :param fp_url: The URL to the floorplan image.
    :type fp_url: str
    :param gallery: A list containing the URLs to all of the gallery images.
    :type gallery: list
    """
    def __init__(self, headline, lonlat, descr, rent, rooms, fp_url, gallery):
        self.headline = headline
        self.lonlat = lonlat
        self.descr = descr
        self.rent = rent
        self.bedrooms = rooms[0]
        self.bathrooms = rooms[1]
        self.gallery = gallery

    def __str__(self):
        '''Returns the human-readable location headline of the property.'''
        return self.headline 

    def download(self):
        '''Downloads and archives the images to an archive/database.'''
        raise RuntimeError("The function to download and archive all images to a database has not been implemented.")
