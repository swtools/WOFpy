import os
import soaplib
import logging

from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple
from werkzeug.exceptions import NotFound
from soaplib.core.server import wsgi

import wofpy_soap
import private_config

from wof import WOF
from wofpy_soap import create_wof_service_class
from wofpy_flask import config
from wofpy_flask import create_app

from daos.odm.odm_dao import OdmDao
from daos.swis.swis_dao import SwisDao
from daos.cbi.cbi_dao import CbiDao

logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':

    cbi_cache_connection_string = 'sqlite:///' + os.path.join(
        os.path.dirname(__file__), 'daos', 'cbi', 'cbi_cache.db')

    lbr_dao = OdmDao(private_config.lbr_connection_string)
    swis_dao = SwisDao(private_config.swis_connection_string,
                  'config/swis_config.cfg')
    cbi_dao = CbiDao(cbi_cache_connection_string, 'config/cbi_config.cfg')
    
    lbr_wof = WOF(lbr_dao)
    lbr_wof.config_from_file('config/lbr_config.cfg')
    
    swis_wof = WOF(swis_dao)
    swis_wof.config_from_file('config/swis_config.cfg')
    
    cbi_wof = WOF(cbi_dao)
    cbi_wof.config_from_file('config/cbi_config.cfg')
    
    #Create the Flask applications
    lbr_flask_app = create_app(lbr_wof)
    lbr_flask_app.config.from_object(config.DevConfig)
    
    swis_flask_app = create_app(swis_wof)
    swis_flask_app.config.from_object(config.DevConfig)

    cbi_flask_app = create_app(cbi_wof)
    cbi_flask_app.config.from_object(config.DevConfig)
    
    #Create the soaplib classes
    LBRWOFService = create_wof_service_class(lbr_wof)
    SWISWOFService = create_wof_service_class(swis_wof)
    CBIWOFService = create_wof_service_class(cbi_wof)
    
    #Create the soaplib applications
    lbr_soap_app = soaplib.core.Application(services=[LBRWOFService],
        tns='http://www.cuahsi.org/his/1.0/ws/',
        name='WaterOneFlow')

    swis_soap_app = soaplib.core.Application(services=[SWISWOFService],
        tns='http://www.cuahsi.org/his/1.0/ws/',
        name='WaterOneFlow')
    
    cbi_soap_app = soaplib.core.Application(services=[CBIWOFService],
        tns='http://www.cuahsi.org/his/1.0/ws/',
        name='WaterOneFlow')

    #Create WSGI apps from the soaplib applications
    lbr_soap_wsgi_app = soaplib.core.server.wsgi.Application(lbr_soap_app)
    swis_soap_wsgi_app = soaplib.core.server.wsgi.Application(swis_soap_app)
    cbi_soap_wsgi_app = soaplib.core.server.wsgi.Application(cbi_soap_app)


    combined_app = DispatcherMiddleware(NotFound,{
        '/lbr' : lbr_flask_app,
        '/swis' : swis_flask_app,
        '/cbi' : cbi_flask_app,
        '/soap/lbr' : lbr_soap_wsgi_app,
        '/soap/swis' : swis_soap_wsgi_app,
        '/soap/cbi' : cbi_soap_wsgi_app
    })

    print "------------------------------------------------------------"
    print "Access 'REST' endpoints at http://HOST:PORT/<network>"
    print "Access SOAP WSDLs at http://HOST:PORT/soap/<network>.wsdl"
    print "Available <network>s are 'lbr', 'swis' and 'cbi'"
    print "------------------------------------------------------------"
    
    run_simple('0.0.0.0', 8080, combined_app, use_reloader=True,
               use_debugger=True, threaded=True)
    
    
    