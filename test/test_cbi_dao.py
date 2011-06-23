import unittest
import os
import sys
import tempfile

sys.path.append('../implementations/')
from cbi.cbi_dao import CbiDao


CBI_CACHE_DATABASE_URI = 'sqlite:////' + os.path.join(
    tempfile.gettempdir(), 'cbi_dao_cache.db')
TEST_CONFIG_PATH = os.path.join(os.path.dirname(__file__),
                                'test_cbi_config.cfg')


class TestCbiDao(unittest.TestCase):
    def setUp(self):
        self.dao = CbiDao(TEST_CONFIG_PATH, CBI_CACHE_DATABASE_URI)

        self.known_sites = {
            '001': 'Naval Air Station (87754211)',
            '002': 'Lawrence St. T-Head (87753511)',
            '003': 'Rincon del San Jose (87778121)',
            '004': 'Yarborough Pass (87766871)',
            '005': 'Packery Channel (87757921)',
            '006': 'Ingleside (87752831)',
            '007': 'El Toro Island (87775623)',
            '008': 'Texas State Aquarium (87752961)',
            '009': 'Port Aransas (87752371)',
            '010': 'Williamson Boat Works (87766391)',
            '011': 'White Point (87751881)',
            '012': 'Offshore (CBI90012)',
            '013': 'S. Bird Island (87761391)',
            '014': 'Bob Hall Pier (87758701)',
            '015': 'Rockport (87747701)',
            '016': 'Sabine Pass (87705701)',
            '017': 'Port Mansfield (87784901)',
            '018': 'Port Isabel (87797701)',
            '021': 'Galveston Pleasure Pier (87715101)',
            '022': 'Galveston Pier 21 (87714501)',
            '023': 'N. Matagorda Island (87739631)',
            '024': 'South Bay (87797681)',
            '025': 'CBI Christmas Bay (CBI90025)',
            '026': 'CBI Clear Lake (CBI90026)',
            '028': 'Flower Garden (CBI90028)',
            '029': 'Delta Rincon (87752751)',
            '030': 'Bayside (87746521)',
            '031': 'Seadrift (87730371)',
            '032': 'East Matagorda Bay (87730011)',
            '033': 'Port Lavaca (87732591)',
            '034': 'Palacios (87731561)',
            '035': 'Goose Island (87745221)',
            '036': 'Copano Bay (87745131)',
            '037': 'Indian Head Point (CBI90037)',
            '038': 'False Live Oak (CBI90038)',
            '039': 'Shamrock Island (CBI90039)',
            '041': 'Nueces Delta 1',
            '042': 'Nueces Delta 2',
            '043': 'Nueces Delta 3',
            '047': 'Arroyo Colorado (87790381)',
            '048': 'Colorado River (CBI90048)',
            '049': 'San Bernard Rivers End (87726891)',
            '050': 'Churchill - San Bernard (CBI90050)',
            '051': 'S. Padre Island Coast Guard Sta. (87797481)',
            '054': 'Rawlings (87733041)',
            '056': 'Freeport (87724401)',
            '057': 'Port O\'Connor (87737011)',
            '058': 'Lavaca Bay (87733261)',
            '059': 'Freeport RTNS Dolphin',
            '060': 'East Matagorda, Old Gulf Cut (87731181)',
            '061': 'SWEmatagorda (CBI90061)',
            '065': 'Freeport Flowinfo RTNS (FREFLO)',
            '068': 'Baffin Bay (87766041)',
            '069': 'Nueces Delta Weather Station',
            '072': 'SALT01',
            '074': 'SALT03',
            '075': 'SALT04',
            '076': 'SALT05',
            '077': 'SALT06',
            '078': 'SALT07',
            '079': 'SALT08',
            '080': 'DO0',
            '082': 'DO2',
            '083': 'DO3',
            '084': 'DO4',
            '085': 'DO5',
            '086': 'DO6',
            '087': 'ndmp1',
            '088': 'ndmp2',
            '089': 'ndmp3',
            '090': 'ndmp4',
            '094': 'San Jacinto River Project (sanjac)',
            '095': 'SERF Weather Station (CBI90095)',
            '098': 'NWS Weather Station 1',
            '100': 'RTNS Offshore',
            '106': 'RTNS Ingleside',
            '108': 'CC Bay Platform (ccbay)',
            '109': 'RTNS Port Aransas',
            '110': 'DO10',
            '111': 'DO11',
            '113': 'DO13',
            '114': 'TWDB Current Meter at Turkey Bend',
            '115': 'TWDB Current Meter at Chinquapin',
            '116': 'TWDB Current Meter at Gulf Cut',
            '117': 'TWDB Current Meter at Old Gulf',
            '118': 'Port of Brownsville, Brownsville Ship Channel (87799771)',
            '119': 'Port Lavaca Causeway Current Meter',
            '121': 'Eastern Arm Current Meter',
            '122': 'Pass Cavallo Current Meter',
            '123': 'Marker 20 Current Meter',
            '124': 'SALT09',
            '125': 'Magnolia Beach Current Meter',
            '126': 'Texas Point (87708221)',
            '127': 'GBRA Station #1',
            '128': 'Tampico Mexico (95009661)',
            '129': 'Mezquital Mexico (95002021)',
            '130': 'GBRA Station #2',
            '131': 'Bahia Grande Meteorological Station (87798611)',
            '132': 'Bahia Grande Water Quality Station #1',
            '133': 'Bahia Grande Water Quality Station #2',
            '134': 'Bahia Grande Water Quality Station #3',
            '135': 'Corpus Christi Marina Weather Station (DNR00135)',
            '136': 'Live Oak Point',
            '137': 'Packery Current Meter #1',
            '138': 'Packery Current Meter #2',
            '139': 'La Pesca (95004081)',
            '146': 'MANERR Station #2 (Copano East)',
            '147': 'MANERR Station #3 (Copano West)',
            '148': 'MANERR Station #4 (Aransas Bay)',
            '149': 'MANERR Station #5 (Port Aransas)',
            '150': 'JFK Bridge Current Meter #1',
            '151': 'Bob Hall Wave Gauge',
            '152': 'USCG Freeport (87724471)',
            '153': 'Viola Turning Basin (87752221)',
            '170': 'National Park Service - Baffin Bay',
            '171': 'National Park Service - Bird Island',
            '181': 'Realitos Peninsula (87792801)',
            '185': 'Nueces Bay (87752441)',
            '501': 'Christmas Bay (87721321)',
            '502': 'Clear Lake (87709331)',
            '503': 'Morgans Point (87706131)',
            '504': 'Rainbow Bridge (87705201)',
            '505': 'Round Point (87705591)',
            '506': 'Mesquite Point (87705391)',
            '507': 'Eagle Point (87710131)',
            '508': 'Alligator Point (87718011)',
            '509': 'High Island (87709231)',
            '513': 'Manchester Houston (87707771)',
            '514': 'Beaumont (87705951)',
            '515': 'Orange (87705971)',
            '517': 'Lynchburg (87707331)',
            '518': 'Rollover Pass (87709711)',
            '519': 'Chocolate Bayou (87717081)',
            '520': 'Bastrop Bayou (87719841)',
            '521': 'Port Bolivar (87713281)',
            '522': 'Galveston Entrance Channel, South Jetty (87714161)',
            '523': 'Sabine Offshore (87710811)',
            '524': 'Port Arthur (87704751)',
            '525': 'Galveston Offshore (87719041)',
            '526': 'San Luis Pass (87719721)',
            '527': 'Sabine Jetty (87707011)',
            '528': 'Point Barrow (87705571)',
            '529': 'Galveston Entrance Channel, North Jetty (87713411)',
            '532': 'West Bay (87718541)',
            '533': 'Battleship Texas State Park (87707431)'
        }

        self.known_var_codes = (
            'vertical_current',
            'eastward_current',
            'significant_wave_period',
            'specific_conductance',
            'wind_speed',
            'wind_from_direction',
            'voltage',
            'turbidity',
            'chl_concentration',
            'air_pressure',
            'relative_humidity',
            'air_temperature',
            'oxygen_saturation',
            'depth',
            'northward_current',
            'current_speed',
            'wind_gust',
            'photosynthetically_available_radiation',
            'signifcant_wave_to_direction',
            'sea_surface_elevation',
            'water_pressure',
            'salinity',
            'conductivity',
            'signifcant_wave_height',
            'oxygen_concentration',
            'water_temperature'
        )

    def test_get_all_sites(self):
        siteResultList = self.dao.get_all_sites()
        resultSiteCodes = [s.SiteCode for s in siteResultList]
        for known_code in self.known_sites:
            self.assertTrue(known_code in resultSiteCodes)

    def test_get_site_by_code(self):
        for known_code in self.known_sites:
            siteResult = self.dao.get_site_by_code(known_code)
            self.assertEqual(known_code, siteResult.SiteCode)

    def test_get_sites_by_codes(self):
        siteResultList = self.dao.get_sites_by_codes(self.known_sites)
        resultSiteCodes = [s.SiteCode for s in siteResultList]
        for known_code in self.known_sites:
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

    #TODO: Test other DAO Methods

    def test_get_series_by_sitecode(self):
        for known_code in self.known_sites:
            seriesResultArr = self.dao.get_series_by_sitecode(known_code)
            self.assertNotEqual(seriesResultArr, None)
            self.assertNotEqual(len(seriesResultArr), 0)
