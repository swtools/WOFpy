import logging
import os
import tempfile

from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple
from werkzeug.exceptions import NotFound
import soaplib
from soaplib.core.server import wsgi

import private_config

from wof import WOF
from wof.soap import create_wof_service_class
from wof.flask import config, create_app

from examples.swis.swis_dao import SwisDao
from examples.cbi.cbi_dao import CbiDao

logging.basicConfig(level=logging.DEBUG)


if __name__ == '__main__':
    #This one includes the SARA service from Ernest and was used
    # in the demonstration to Espey
        
    # change the deployment dir if you are going to deploy this in production
    CBI_CACHE_DIR = tempfile.gettempdir()
    CBI_CACHE_DATABASE_URI = 'sqlite:///' + os.path.join(
    CBI_CACHE_DIR, 'cbi_dao_cache.db')
    
    swis_dao = SwisDao(private_config.swis_connection_string,
                        'swis/swis_config.cfg')    
    cbi_dao = CbiDao('cbi/cbi_config.cfg', database_uri=CBI_CACHE_DATABASE_URI)

    swis_wof = WOF(swis_dao)    
    swis_wof.config_from_file('swis/swis_config.cfg')

    cbi_wof = WOF(cbi_dao)        
    cbi_wof.config_from_file('cbi/cbi_config.cfg')

    #Create the Flask applications
    swis_flask_app = create_app(swis_wof)
    cbi_flask_app = create_app(cbi_wof)

    #Create the soaplib classes
    SWISWOFService = create_wof_service_class(swis_wof)
    CBIWOFService = create_wof_service_class(cbi_wof)

    #Create the soaplib applications
    swis_soap_app = soaplib.core.Application(services=[SWISWOFService],
        tns='http://www.cuahsi.org/his/1.0/ws/',
        name='WaterOneFlow')

    cbi_soap_app = soaplib.core.Application(services=[CBIWOFService],
        tns='http://www.cuahsi.org/his/1.0/ws/',
        name='WaterOneFlow')
    
    #Create WSGI apps from the soaplib applications
    swis_soap_wsgi_app = soaplib.core.server.wsgi.Application(swis_soap_app)
    cbi_soap_wsgi_app = soaplib.core.server.wsgi.Application(cbi_soap_app)

    combined_app = DispatcherMiddleware(NotFound, {
        '/swis': swis_flask_app,
        '/cbi': cbi_flask_app,
        '/swis/soap/wateroneflow': swis_soap_wsgi_app,
        '/cbi/soap/wateroneflow': cbi_soap_wsgi_app
    })
    
    print "------------------------------------------------------------"
    print "Access 'REST' endpoints at http://HOST:8080/<network>"
    print "Access SOAP WSDLs at http://HOST:8080/<network>/soap/wateroneflow.wsdl"
    print "Available <network>s are 'swis' and 'cbi'"
    print "------------------------------------------------------------"
   
    run_simple('0.0.0.0', 8080, combined_app, use_reloader=True,
               use_debugger=True, threaded=True)
