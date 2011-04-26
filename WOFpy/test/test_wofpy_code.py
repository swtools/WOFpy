from lxml import etree
import unittest
import os
import StringIO

import wof
import wof.code
import private_config

import swis_dao

class TestSwisDao(unittest.TestCase):
    def setUp(self):
        test_db_path = os.path.join(os.path.dirname(__file__),
                                        'test_swis2.db')
        
        test_config_path = os.path.join(os.path.dirname(__file__),
                                        'test_swis_config.cfg')
        
        wof.dao = swis_dao.SwisDao('sqlite:///'+test_db_path)
        wof.config_from_file(test_config_path)
        
        waterml_schema_path = os.path.join(os.path.dirname(__file__),
                                        'cuahsiTimeSeries_v1_0.xsd')
        
        self.waterml_schema_doc = etree.parse(waterml_schema_path)
        self.waterml_schema = etree.XMLSchema(self.waterml_schema_doc)
        
        
        self.known_site_codes = (
            'ARA', 'ARROYD', 'ARROYS', 'BAFF', 'BAYT', 'BIRD', 'BLB', 'BOBH',
            'BOLI', 'BRAZOSD', 'BRAZOSS', 'BZ1U', 'BZ1UX', 'BZ2L', 'BZ2U',
            'BZ3L', 'BZ3U', 'BZ4L', 'BZ4U', 'BZ5L', 'BZ5U', 'BZ6U', 'CANEY',
            'CED1', 'CED2', 'CHKN', 'CONT', 'COP', 'COWT', 'DELT', 'DOLLAR',
            'EAST', 'EEMAT', 'ELTORO', 'EMATC', 'EMATH', 'EMATT', 'FISH',
            'FRES', 'FRPT', 'GIW1',  'GWSB1', 'GWSB2', 'HANN', 'ICFR', 'INGL',
            'ISABEL', 'JARD', 'JDM1', 'JDM2', 'JDM3', 'JDM4', 'JFK', 'JOB',
            'LAVC', 'LM-ARR', 'MANS', 'MATA', 'MCF1', 'MCF2', 'MES', 'MIDG',
            'MIDSAB', 'MOSQ', 'NUE', 'NUECWN', 'NUECWS', 'NUELOW', 'NUEPP',
            'NUERIV', 'NUEUP', 'OLDR', 'OSO', 'RED', 'RIOA', 'RIOF', 'SAB1',
            'SAB2', 'SANT', 'SB1S', 'SB1W', 'SB2S', 'SB2W', 'SB3S', 'SB3W',
            'SB5S', 'SB5W', 'SB6W', 'SBBP', 'SBR1', 'SBR2', 'SBR3', 'SBR4',
            'SBR5', 'SBWS', 'SLNDCUT', 'SWBR', 'TRIN', 'UPBAFF', 'USAB'
        )

        
        self.known_var_codes = (
           'air_pressure', 'instrument_battery_voltage',
           'water_specific_conductance', 'water_electrical_conductivity',
           'water_dissolved_oxygen_concentration',
           'water_dissolved_oxygen_percent_saturation',
           'water_ph', 'seawater_salinity', 'water_temperature',
           'air_temperature', 'water_total_dissolved_salts',
           'water_turbidity', 'water_depth_non_vented', 'water_depth_vented',
           'northward_water_velocity', 'eastward_water_velocity',
           'upward_water_velocity', 'water_x_velocity', 'water_y_velocity'
        )
        
    def test_create_get_site_response(self):
        for site_code in self.known_site_codes:
            get_site_respose = wof.code.create_get_site_response(site_code)
    
    def test_create_get_site_info_response(self):
        pass
    
    def test_create_variable_info_response(self):
        pass
    
    def test_create_get_values_response(self):
        pass