import logging
import os
import tempfile

from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple
from werkzeug.exceptions import NotFound
import soaplib
from soaplib.core.server import wsgi

from wof import WOF
from wof.soap import create_wof_service_class
from wof.flask import config, create_app

from examples.swis.swis_dao import SwisDao
from examples.barebones.LCM_dao import LCMDao

logging.basicConfig(level=logging.DEBUG)

swis_dao = SwisDao('swis/swis_config.cfg',
                   database_uri='sqlite:///swis/swis2.db')
lcm_dao = LCMDao('sqlite:///barebones/LCM_Data/LCM.db',
                 'barebones/LCM_config.cfg')

swis_wof = WOF(swis_dao)
swis_wof.config_from_file('swis/swis_config.cfg')

lcm_wof = WOF(lcm_dao)
lcm_wof.config_from_file('barebones/LCM_config.cfg')
#Create the Flask applications
swis_flask_app = create_app(swis_wof)
lcm_flask_app = create_app(lcm_wof)

#Create the soaplib classes
SWISWOFService = create_wof_service_class(swis_wof)
LCMWOFService = create_wof_service_class(lcm_wof)

#Create the soaplib applications
swis_soap_app = soaplib.core.Application(services=[SWISWOFService],
    tns='http://www.cuahsi.org/his/1.0/ws/',
    name='WaterOneFlow')

lcm_soap_app = soaplib.core.Application(services=[LCMWOFService],
    tns='http://www.cuahsi.org/his/1.0/ws/',
    name='WaterOneFlow')

#Create WSGI apps from the soaplib applications
swis_soap_wsgi_app = soaplib.core.server.wsgi.Application(swis_soap_app)
lcm_soap_wsgi_app = soaplib.core.server.wsgi.Application(lcm_soap_app)

combined_app = DispatcherMiddleware(NotFound, {
    '/swis': swis_flask_app,
    '/lcm': lcm_flask_app,
    '/swis/soap/wateroneflow': swis_soap_wsgi_app,
    '/lcm/soap/wateroneflow': lcm_soap_wsgi_app
})

if __name__ == '__main__':
    print "------------------------------------------------------------"
    print "Access 'REST' endpoints at http://HOST:8080/<network>"
    print "Access SOAP WSDLs at http://HOST:8080/<network>/soap/wateroneflow.wsdl"
    print "Available <network>s are 'swis' and 'lcm'"
    print "------------------------------------------------------------"
   
    run_simple('0.0.0.0', 8080, combined_app, use_reloader=True,
               use_debugger=True, threaded=True)
