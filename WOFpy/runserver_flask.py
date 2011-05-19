
import soaplib
import logging

from werkzeug.wsgi import DispatcherMiddleware
from soaplib.core.server import wsgi

import wofpy_soap
import private_config

from wof import WOF
from wofpy_soap import create_wof_service_class
from wofpy_flask import config
from wofpy_flask import create_app
from daos.odm.odm_dao import OdmDao

logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':

    
    dao = OdmDao(private_config.lbr_connection_string)
    odm_wof = WOF(dao)
    odm_wof.config_from_file('config/lbr_config.cfg')
    
    flask_app = create_app(odm_wof)
    flask_app.config.from_object(config.DevConfig)

    ODMWOFService = create_wof_service_class(odm_wof)

    soap_app = soaplib.core.Application(services=[ODMWOFService],
        tns='http://www.cuahsi.org/his/1.0/ws/',
        name='WaterOneFlow')

    soap_wsgi_app = soaplib.core.server.wsgi.Application(soap_app)

    flask_app.wsgi_app = DispatcherMiddleware(flask_app.wsgi_app, {
        '/soap/lbr': soap_wsgi_app,        
    })

    flask_app.run(host='0.0.0.0', port=8080, threaded=True)
