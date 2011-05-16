
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
from daos.swis.swis_dao import SwisDao

logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    
    dao = SwisDao(private_config.swis_connection_string,
                  'config/swis_config.cfg')
    
    swis_wof = WOF(dao)
    swis_wof.config_from_file('config/swis_config.cfg')

    flask_app = create_app(swis_wof)
    flask_app.config.from_object(config.DevConfig)

    SWISWOFService = create_wof_service_class(swis_wof)
    
    soap_app = soaplib.core.Application(services=[SWISWOFService],
        tns='http://www.cuahsi.org/his/1.0/ws/',
        name='WaterOneFlow')

    soap_wsgi_app = soaplib.core.server.wsgi.Application(soap_app)

    flask_app.wsgi_app = DispatcherMiddleware(flask_app.wsgi_app, {
        '/soap': soap_wsgi_app
    })

    flask_app.run(host='0.0.0.0', port=8080, threaded=True)
