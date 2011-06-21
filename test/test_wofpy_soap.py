import suds
import unittest

#TODO finish this unittest
# should definitely test for bad inputs (non-existent site and var codes, bad dates for getvalues, etc.)

class TestWofpySoap(unittest.TestCase):
    """
    UnitTest to test the WOF SOAP methods using a Suds client.
    
    Assumes a server using the SWIS DAO is already up and running at the
    specified WSDL Address.
    """
    
    def setUp(self):
        #Change this to your currently-running WSDL
        wsdl_address = "http://127.0.0.1:8080/soap/wateroneflow.wsdl"
        self.network = 'SWIS'
        
        self.client = suds.client.Client(wsdl_address)
        
        #Assuming use of LBR ODM database
        #TODO: Maybe should test against SWIS instead.  SQLite seems faster.
        self.known_site_codes = [
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
        ]
        
        self.known_var_codes = [
           'air_pressure', 'instrument_battery_voltage',
           'water_specific_conductance', 'water_electrical_conductivity',
           'water_dissolved_oxygen_concentration',
           'water_dissolved_oxygen_percent_saturation',
           'water_ph', 'seawater_salinity', 'water_temperature',
           'air_temperature', 'water_total_dissolved_salts',
           'water_turbidity', 'water_depth_non_vented', 'water_depth_vented',
           'northward_water_velocity', 'eastward_water_velocity',
           'upward_water_velocity', 'water_x_velocity', 'water_y_velocity'
        ]
        
        #Need more test data, only JOB and BAYT have datavalues associated with them
        self.known_series = dict(
            BAYT = ['instrument_battery_voltage',
                    'water_electrical_conductivity',
                    'water_dissolved_oxygen_percent_saturation',
                    'seawater_salinity',
                    'water_temperature',
                    'water_depth_non_vented']
        )
        
    def test_getsitesxml(self):
        result = self.client.service.GetSitesXml('')
        self.assertNotEqual(result, None)
    
    def test_getsites(self):
        result = self.client.service.GetSites('')
        self.assertNotEqual(result, None)
    
    def test_getvariableinfo(self):
        result = self.client.service.GetVariableInfo('')
        self.assertNotEqual(result, None)
        
        for var_code in self.known_var_codes:
            result = self.client.service.GetVariableInfo(
                self.network+':'+var_code)
            self.assertNotEqual(result, None)
            #TODO: test that the var code matches the given var code
    
    def test_getvariableinfoobject(self):
        result = self.client.service.GetVariableInfoObject('')
        self.assertNotEqual(result, None)
        
        for var_code in self.known_var_codes:
            result = self.client.service.GetVariableInfoObject(
                self.network+':'+var_code)
            self.assertNotEqual(result, None)
            #TODO: test that the var code matches the given var code
    
    def test_getsiteinfo(self):
        for site_code in self.known_series: #TODO: every site should have siteinfo, but the swis db is not complete
            result = self.client.service.GetSiteInfo(
                self.network+':'+site_code)
            self.assertNotEqual(result, None)
            #TODO: test that the site code in the result matches the given site code
    
    def test_getsiteinfoobject(self):
        for site_code in self.known_series: #TODO: every site should have siteinfo, but the swis db is not complete
            result = self.client.service.GetSiteInfoObject(
                self.network+':'+site_code)
            self.assertNotEqual(result, None)
            #TODO: test that the site code in the result matches the given site code

    def test_getvalues(self):
        for site_code, var_code_list in self.known_series.items():
            for var_code in var_code_list:
                result = self.client.service.GetValues(self.network+':'+site_code, self.network+':'+var_code)
            
    def test_getvaluesobject(self):
        for site_code, var_code_list in self.known_series.items():
            for var_code in var_code_list:
                result = self.client.service.GetValuesObject(
                    site_code, var_code)