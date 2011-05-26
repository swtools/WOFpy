import suds
import soaplib
import unittest

from werkzeug.wsgi import DispatcherMiddleware
from soaplib.core.server import wsgi

from daos.odm.odm_dao import OdmDao

from wofpy_soap import create_wof_service_class
from wofpy_flask import config
from wofpy_flask import create_app

#TODO
class TestWofpySoap(unittest.TestCase):
    
    def setUp(self):
        #just assume that the server is already running
        self.wsdl_address = None
        #setup the suds client here
        
    def tearDown(self):
        pass
        
    def test_get_sites(self):
        pass