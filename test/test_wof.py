import itertools
import os
import StringIO
import unittest

from lxml import etree
from wof import WOF

from test_dao import TestDao

TEST_CONFIG_FILE = 'test_config.cfg'
TEST_XML_DIR = 'test_xml'

NSDEF = 'xmlns:gml="http://www.opengis.net/gml" \
    xmlns:xlink="http://www.w3.org/1999/xlink" \
    xmlns:xsd="http://www.w3.org/2001/XMLSchema" \
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" \
    xmlns:wtr="http://www.cuahsi.org/waterML/" \
    xmlns="http://www.cuahsi.org/waterML/1.0/"'


class TestWOF(unittest.TestCase):
    """
    Tests wof response generation methods for validation against
    the WaterML 1.0 schema.
    """

    def setUp(self):
        dao = TestDao()
        self.wof_inst = WOF(dao, TEST_CONFIG_FILE)
        waterml_schema_path = os.path.join(os.path.dirname(__file__),
                                        'cuahsiTimeSeries_v1_0.xsd')
        waterml_schema_doc = etree.parse(waterml_schema_path)
        self.waterml_schema = etree.XMLSchema(waterml_schema_doc)

    def compare_output_to_known_xml(self, response, filename):
        """
        Make sure response output is as expected. This tests that a
        response contains the same text as the filename.
        """
        out_file_path = os.path.join(os.path.dirname(__file__),
                                     TEST_XML_DIR, filename)
        response_output = StringIO.StringIO()
        response.export(response_output, 0, name_="sitesResponse",
                        namespacedef_=NSDEF)
        response_output.seek(0)
        # test each line in the response text equals each line in the file
        with open(out_file_path, 'rb') as valid_file:
            for response_line, valid_line in itertools.izip(response_output, valid_file):
                assert response_line == valid_line


    def test_get_all_sites(self):
        get_site_response = self.wof_inst.create_get_site_response()
        self.compare_output_to_known_xml(get_site_response,
                                         'get_all_sites.xml')

    def test_get_one_site(self):
        get_site_response = self.wof_inst.create_get_site_response(
            'TEST:SITE_A')
        self.compare_output_to_known_xml(get_site_response,
                                         'get_one_site.xml')

    def test_get_multiple_sites(self):
        get_site_response = self.wof_inst.create_get_site_response(
            'TEST:SITE_A,TEST:SITE_B')
        self.compare_output_to_known_xml(get_site_response,
                                         'get_multiple_sites.xml')

