import suds
import soaplib
import unittest

from werkzeug.wsgi import DispatcherMiddleware
from soaplib.core.server import wsgi

from daos.odm.odm_dao import OdmDao

from wofpy_soap.soap import WOFService
from wofpy_flask import config
from wofpy_flask import create_app

class TestWofpySoap(unittest.TestCase):
    
    def setUp(self):
        self.wsdlurl = 'http://127.0.0.1:8080/soap/WOFService.wsdl'
        '''
        flask_app.config.from_object(config.DevConfig)
        wof.config_from_file('config/lbr_config.cfg')
        wof.dao = odm_dao.OdmDao()
        
        soap_app = soaplib.core.Application([WOFService],
            'http://www.cuahsi.org/his/1.0/ws/')
        
        soap_wsgi_app = soaplib.core.server.wsgi.Application(soap_app)
        
        flask_app.wsgi_app = DispatcherMiddleware(flask_app.wsgi_app, {
            '/soap': soap_wsgi_app
        })
        
        flask_app.run(host='0.0.0.0', port=8080, threaded=True,
                      debug=False)
        '''
        
    def tearDown(self):
        pass
        
    def test_get_sites(self):
        pass