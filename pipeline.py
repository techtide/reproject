#!/usr/bin/env python

from rightmove import RightmoveHelper
from property import Property

class RightmovePipeline:
    def __init__(self, loc):
        self.loc = loc
        helper = RightmoveHelper()
        rmid = helper.loc_to_rmid(loc)[0]["locationId"]

if __name__ == "__main__":
    
