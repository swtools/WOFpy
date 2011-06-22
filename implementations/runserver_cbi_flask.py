import logging
import os
import tempfile

from werkzeug.wsgi import DispatcherMiddleware
import soaplib
from soaplib.core.server import wsgi
from wof import WOF
from wof.soap import create_wof_service_class
from wof.flask import config
from wof.flask import create_app

import private_config
from daos.cbi.cbi_dao import CbiDao


CBI_CACHE_DATABASE_URI = 'sqlite:////' + os.path.join(
    tempfile.gettempdir(), 'cbi_dao_cache.db')

logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    dao = CbiDao('config/cbi_config.cfg', CBI_CACHE_DATABASE_URI)
    cbi_wof = WOF(dao)
    cbi_wof.config_from_file('config/cbi_config.cfg')

    flask_app = create_app(cbi_wof)
    flask_app.config.from_object(config.DevConfig)

    CBIWOFService = create_wof_service_class(cbi_wof)

    soap_app = soaplib.core.Application(services=[CBIWOFService],
        tns='http://www.cuahsi.org/his/1.0/ws/',
        name='WaterOneFlow')

    soap_wsgi_app = soaplib.core.server.wsgi.Application(soap_app)

    flask_app.wsgi_app = DispatcherMiddleware(flask_app.wsgi_app, {
        '/soap/cbi': soap_wsgi_app
    })

    flask_app.run(host='0.0.0.0', port=8080, threaded=True)
