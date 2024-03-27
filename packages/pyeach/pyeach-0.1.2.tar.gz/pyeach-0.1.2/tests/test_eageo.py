"""
Test the functions in eageo.py
"""

import unittest
import warnings
from pyeach.eageo import *


class TestEAGeo(unittest.TestCase):
    def setUp(self):
        warnings.simplefilter("ignore", category=UserWarning)

    ## Need to figure out why locations() does not work on DS2
    # def test_locations(self):
    #     educ = locations("ed_uc")
    #     hosp = locations("hospitals")
    #     comc = locations("comm_care")
    #     cnps = locations("cnp")
    #     pcps = locations("pcp")
    #     comf = locations("comm_food")
    #     aggh = locations("agg_housing")

    #     self.assertEqual(educ.shape, (7, 4))
    #     self.assertEqual(hosp.shape, (9, 3))
    #     self.assertEqual(comc.shape, (14,11))
    #     self.assertEqual(cnps.shape, (66, 3))
    #     self.assertEqual(pcps.shape, (150, 3))
    #     self.assertEqual(comf.shape, (151, 4))
    #     self.assertEqual(aggh.shape, (2580, 9))

    def test_nc_va_geos(self):
        tracts = nc_va_geos("tract")
        blocks = nc_va_geos("block")
        blockg = nc_va_geos("block_groups")
        zipcds = nc_va_geos("zipcode")
        county = nc_va_geos("county")
        
        self.assertEqual(str(type(county["geometry"])), "<class 'geopandas.geoseries.GeoSeries'>")
        self.assertEqual(str(type(zipcds["geometry"])), "<class 'geopandas.geoseries.GeoSeries'>")
        self.assertEqual(str(type(tracts["geometry"])), "<class 'geopandas.geoseries.GeoSeries'>")
        self.assertEqual(str(type(blockg["geometry"])), "<class 'geopandas.geoseries.GeoSeries'>")
        self.assertEqual(str(type(blocks["geometry"])), "<class 'geopandas.geoseries.GeoSeries'>")

if __name__ == '__main__':
    unittest.main()
