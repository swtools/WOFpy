import soaplib
import logging

from werkzeug.wsgi import DispatcherMiddleware
from soaplib.core.server import wsgi

from wof import WOF
from wof.soap import create_wof_service_class
from wof.flask import create_app, config
from swis_dao import SwisDao

logging.basicConfig(level=logging.DEBUG)


SWIS_DATABASE_URI = 'sqlite:///swis2.db'

dao = SwisDao(SWIS_DATABASE_URI,
              'swis_config.cfg')

swis_wof = WOF(dao)
swis_wof.config_from_file('swis_config.cfg')

app = create_app(swis_wof)
app.config.from_object(config.DevConfig)

SWISWOFService = create_wof_service_class(swis_wof)

soap_app = soaplib.core.Application(services=[SWISWOFService],
                                    tns='http://www.cuahsi.org/his/1.0/ws/',
                                    name='WaterOneFlow')

soap_wsgi_app = soaplib.core.server.wsgi.Application(soap_app)

app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/soap/swis': soap_wsgi_app
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True)
