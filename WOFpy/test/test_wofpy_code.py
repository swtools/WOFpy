from lxml import etree
import unittest
import os
import StringIO

import wof
import wof.code
import private_config

from daos.swis.swis_dao import SwisDao

NSDEF = 'xmlns:gml="http://www.opengis.net/gml" \
    xmlns:xlink="http://www.w3.org/1999/xlink" \
    xmlns:xsd="http://www.w3.org/2001/XMLSchema" \
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" \
    xmlns:wtr="http://www.cuahsi.org/waterML/" \
    xmlns="http://www.cuahsi.org/waterML/1.0/"'

class TestWofpyCode(unittest.TestCase):
    
    def setUp(self):
        test_db_path = os.path.join(os.path.dirname(__file__),
                                        'test_swis2.db')
        
        test_config_path = os.path.join(os.path.dirname(__file__),
                                        'test_swis_config.cfg')
        
        wof.dao = SwisDao('sqlite:///'+test_db_path)
        wof.config_from_file(test_config_path)
        
        waterml_schema_path = os.path.join(os.path.dirname(__file__),
                                        'cuahsiTimeSeries_v1_0.xsd')
        
        waterml_schema_doc = etree.parse(waterml_schema_path)
        self.waterml_schema = etree.XMLSchema(waterml_schema_doc)
        
    def test_create_get_site_response(self):
        get_site_response = wof.code.create_get_site_response()
        
        out_file_path = os.path.join(os.path.dirname(__file__),
                                     'GetSitesResponse.xml')
        
        out_file = open(out_file_path,'w')
        
        get_site_response.export(out_file, 0, name_="sitesResponse",
                                 namespacedef_= NSDEF)
         
        out_file.close() 
         
        doc = etree.parse(out_file_path)
        self.assertTrue(self.waterml_schema.validate(doc))
    
    def test_create_get_site_info_response(self):
        get_site_response = wof.code.create_get_site_info_response('BAYT')
        
        out_file_path = os.path.join(os.path.dirname(__file__),
                                     'GetSiteInfoResponse.xml')
        
        out_file = open(out_file_path,'w')
        
        get_site_response.export(out_file, 0, name_="sitesResponse",
                                 namespacedef_= NSDEF)
         
        out_file.close() 
         
        doc = etree.parse(out_file_path)
        self.assertTrue(self.waterml_schema.validate(doc))
    
    def test_create_get_variable_info_response(self):
        get_site_response = wof.code.create_get_variable_info_response()
        
        out_file_path = os.path.join(os.path.dirname(__file__),
                                     'GetVariableInfoResponse.xml')
        
        out_file = open(out_file_path,'w')
        
        get_site_response.export(out_file, 0, name_="variablesResponse",
                                 namespacedef_= NSDEF)
         
        out_file.close() 
         
        doc = etree.parse(out_file_path)
        self.assertTrue(self.waterml_schema.validate(doc))
    
    def test_create_get_values_response(self):
        get_site_response = wof.code.create_get_values_response(
            'BAYT','seawater_salinity')
        
        out_file_path = os.path.join(os.path.dirname(__file__),
                                     'GetValuesResponse.xml')
        
        out_file = open(out_file_path,'w')
        
        get_site_response.export(out_file, 0, name_="timeSeriesResponse",
                                 namespacedef_= NSDEF)
         
        out_file.close() 
         
        doc = etree.parse(out_file_path)
        self.assertTrue(self.waterml_schema.validate(doc))
