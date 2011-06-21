import unittest
import os
import sys

from lxml import etree

sys.path.append('../implementations/')

from daos.cbi.cbi_sos_parser import parse_datavalues_from_get_observation


class TestCbiParser(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_parse_datavalues_from_get_observation(self):
        
        path = os.path.join(os.path.dirname(__file__), 'cbi_sos_examples',
                     'cbi_get_observations.xml')
        
        f = open(path)
        tree = etree.parse(f)
        
        dataval_list = \
            parse_datavalues_from_get_observation(tree, '014',
                                                  'water_temperature')

        self.assertTrue(dataval_list)
        self.assertTrue(len(dataval_list) == 2)
        
        for datavalue in dataval_list:
            self.assertTrue(datavalue.DataValue)
