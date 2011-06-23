import soaplib
import logging

from werkzeug.wsgi import DispatcherMiddleware
from soaplib.core.server import wsgi

from wof import WOF
from wof.soap import create_wof_service_class
from wof.flask import config
from wof.flask import create_app
from odm_dao import OdmDao

import private_config

logging.basicConfig(level=logging.DEBUG)


dao = OdmDao(private_config.sara_connection_string)
odm_wof = WOF(dao)
odm_wof.config_from_file('config/sara_config.cfg')

app = create_app(odm_wof)
app.config.from_object(config.DevConfig)

ODMWOFService = create_wof_service_class(odm_wof)

soap_app = soaplib.core.Application(services=[ODMWOFService],
                                    tns='http://www.cuahsi.org/his/1.0/ws/',
                                    name='WaterOneFlow')

soap_wsgi_app = soaplib.core.server.wsgi.Application(soap_app)

app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/soap/sara': soap_wsgi_app,
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True)
