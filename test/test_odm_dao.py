import unittest
import odm_dao
import private_config

class TestOdmDao(unittest.TestCase):
    def setUp(self):
        self.dao = odm_dao.OdmDao(
            private_config.lbr_connection_string)
        self.network_prefix = 'LBR'
        self.known_site_codes = (
            'USU-LBR-Mendon',
            'USU-LBR-Paradise',
            'USU-LBR-ExpFarm',
            'USU-LBR-SFLower',
            'USU-LBR-EFLower',
            'USU-LBR-EFWeather',
            'USU-LBR-SFUpper',
            'USU-LBR-ParadiseRepeater',
            'USU-LBR-EFRepeater',
            'USU-LBR-Wellsville',
            'USU-LBR-Confluence',
            '10105900'
        )
        
        self.fake_codes = (
            'junk',
            'trash',
            'fake'
        )
        
        self.known_var_codes = (
            'USU3',
            'USU4',
            'USU5',
            'USU6',
            'USU7',
            'USU8',
            'USU9',
            'USU10',
            'USU11',
            'USU12',
            'USU13',
            'USU14',
            'USU15',
            'USU16',
            'USU17',
            'USU18',
            'USU19',
            'USU20',
            'USU21',
            'USU22',
            'USU23',
            'USU24',
            'USU25',
            'USU26',
            'USU27',
            'USU28',
            'USU29',
            'USU30',
            'USU31',
            'USU32',
            'USU33',
            'USU34',
            'USU35',
            'USU36',
            'USU37',
            'USU38',
            'USU39',
            'USU40',
            'USU41',
            'USU42',
            'USU43'
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
    