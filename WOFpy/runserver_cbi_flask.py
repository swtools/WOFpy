import os
import soaplib
import logging

from werkzeug.wsgi import DispatcherMiddleware
from soaplib.core.server import wsgi

import wof
import private_config

from wofpy_soap.soap import WOFService
from wofpy_flask import config
from wofpy_flask import create_app
from daos.cbi.cbi_dao import CbiDao

logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':

    wof.config_from_file('config/cbi_config.cfg')
    
    cbi_cache_connection_string = 'sqlite:///' + os.path.join(
        os.path.dirname(__file__), 'daos', 'cbi', 'cbi_cache.db')
    
    
    wof.dao = CbiDao(cbi_cache_connection_string)

    flask_app = create_app()
    flask_app.config.from_object(config.DevConfig)

    soap_app = soaplib.core.Application(services=[WOFService],
        tns='http://www.cuahsi.org/his/1.0/ws/',
        name='WaterOneFlow')

    soap_wsgi_app = soaplib.core.server.wsgi.Application(soap_app)

    flask_app.wsgi_app = DispatcherMiddleware(flask_app.wsgi_app, {
        '/soap': soap_wsgi_app
    })

    flask_app.run(host='0.0.0.0', port=8080, threaded=True)