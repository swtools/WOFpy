import unittest
import SwisSqlAlchDao
import private_config

class Test_SwisSqlAlchDao(unittest.TestCase):
    def setUp(self):
        self.dao = SwisSqlAlchDao.SwisSqlAlchDao(
            private_config.swis_test_connection_string)
        
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
        
        self.fake_codes = (
            'junk',
            'trash',
            'fake'
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
        
    def test_get_all_sites(self):
        siteResultList = self.dao.get_all_sites()
        resultSiteCodes = [s.SiteCode for s in siteResultList]
        for known_code in self.known_site_codes:
            self.assertTrue(known_code in resultSiteCodes)
          
    def test_get_site_by_code(self):
        for known_code in self.known_site_codes:
            siteResult = self.dao.get_site_by_code(known_code)
            self.assertEqual(known_code, siteResult.SiteCode)
        
    def test_get_sites_by_codes(self):
        siteResultList = self.dao.get_sites_by_codes(self.known_site_codes)
        resultSiteCodes = [s.SiteCode for s in siteResultList]
        for known_code in self.known_site_codes:
            self.assertTrue(known_code in resultSiteCodes)
    
    def test_get_all_variables(self):
        varResultList = self.dao.get_all_variables()
        resultVarCodes = [v.VariableCode for v in varResultList]
        for known_code in self.known_var_codes:
            self.assertTrue(known_code in resultVarCodes)
    
    def test_get_var_by_code(self):
        for known_code in self.known_var_codes:
            varResult = self.dao.get_variable_by_code(known_code)
            self.assertEqual(known_code, varResult.VariableCode)
            
    def test_get_vars_by_codes(self):
        varResultList = self.dao.get_variables_by_codes(self.known_var_codes)
        resultVarCodes = [v.VariableCode for v in varResultList]
        for known_code in self.known_var_codes:
            self.assertTrue(known_code in resultVarCodes)
            
   
    #TODO
    def test_get_series_by_sitecode(self):
        seriesResult = self.dao.get_series_by_sitecode('BAYT')
        #print len(seriesResult)
        
    #TODO
    def test_get_series_by_sitecode_and_varcode(self):
        pass
    
    #TODO
    def test_get_datavalues(self):
        pass
    
    #TODO
    def test_get_method_by_id(self):
        pass
    
    #TODO
    def test_get_methods_by_ids(self):
        pass
    
    #TODO
    def test_get_source_by_id(self):
        pass
    
    #TODO
    def test_get_sources_by_ids(self):
        pass
    
    #TODO
    def test_get_qualifier_by_id(self):
        pass
    
    #TODO
    def test_get_qualifiers_by_ids(self):
        pass
    
    #TODO
    def test_get_qualcontrol_by_id(self):
        pass
    
    #TODO
    def test_get_qualcontrols_by_ids(self):
        pass
    
    #TODO
    def test_get_offsettype_by_id(self):
        pass
    
    #TODO
    def test_get_offsettypes_by_ids(self):
        pass
        