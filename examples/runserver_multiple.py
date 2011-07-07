import logging
import os

from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple
from werkzeug.exceptions import NotFound
import soaplib
from soaplib.core.server import wsgi

import private_config

from wof import WOF
from wof.soap import create_wof_service_class
from wof.flask import config, create_app

from examples.odm.odm_dao import OdmDao
from examples.swis.swis_dao import SwisDao
from examples.cbi.cbi_dao import CbiDao

logging.basicConfig(level=logging.DEBUG)

CBI_CACHE_DIR = tempfile.gettempdir()


if __name__ == '__main__':
    #This one includes the SARA service from Ernest and was used
    # in the demonstration to Espey

    cbi_cache_connection_string = 'sqlite:////' + os.path.join(
        CBI_CACHE_DIR, 'cbi_cache.db')

    lbr_dao = OdmDao(private_config.lbr_connection_string)
    swis_dao = SwisDao(private_config.swis_connection_string,
                  'config/swis_config.cfg')
    cbi_dao = CbiDao(cbi_cache_connection_string, 'config/cbi_config.cfg')
    sara_dao = OdmDao(private_config.sara_connection_string)

    lbr_wof = WOF(lbr_dao)
    lbr_wof.config_from_file('config/lbr_config.cfg')

    swis_wof = WOF(swis_dao)
    swis_wof.config_from_file('config/swis_config.cfg')

    cbi_wof = WOF(cbi_dao)
    cbi_wof.config_from_file('config/cbi_config.cfg')

    sara_wof = WOF(sara_dao)
    sara_wof.config_from_file('config/sara_config.cfg')

    #Create the Flask applications
    lbr_flask_app = create_app(lbr_wof)
    swis_flask_app = create_app(swis_wof)
    cbi_flask_app = create_app(cbi_wof)
    sara_flask_app = create_app(sara_wof)

    #Create the soaplib classes
    LBRWOFService = create_wof_service_class(lbr_wof)
    SWISWOFService = create_wof_service_class(swis_wof)
    CBIWOFService = create_wof_service_class(cbi_wof)
    SARAWOFService = create_wof_service_class(sara_wof)

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

    sara_soap_app = soaplib.core.Application(services=[SARAWOFService],
        tns='http://www.cuahsi.org/his/1.0/ws/',
        name='WaterOneFlow')

    #Create WSGI apps from the soaplib applications
    lbr_soap_wsgi_app = soaplib.core.server.wsgi.Application(lbr_soap_app)
    swis_soap_wsgi_app = soaplib.core.server.wsgi.Application(swis_soap_app)
    cbi_soap_wsgi_app = soaplib.core.server.wsgi.Application(cbi_soap_app)
    sara_soap_wsgi_app = soaplib.core.server.wsgi.Application(sara_soap_app)

    combined_app = DispatcherMiddleware(NotFound, {
        '/lbr': lbr_flask_app,
        '/swis': swis_flask_app,
        '/cbi': cbi_flask_app,
        '/sara': sara_flask_app,
        '/soap/lbr': lbr_soap_wsgi_app,
        '/soap/swis': swis_soap_wsgi_app,
        '/soap/cbi': cbi_soap_wsgi_app,
        '/soap/sara': sara_soap_wsgi_app
    })

    print "------------------------------------------------------------"
    print "Access 'REST' endpoints at http://HOST:8080/<network>"
    print "Access SOAP WSDLs at http://HOST:8080/<network>/soap/wateroneflow.wsdl"
    print "Available <network>s are 'sara', 'lbr', 'swis' and 'cbi'"
    print "------------------------------------------------------------"

    run_simple('0.0.0.0', 8080, combined_app, use_reloader=True,
               use_debugger=True, threaded=True)
