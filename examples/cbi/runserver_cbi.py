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

from cbi_dao import CbiDao


# change the deployment dir if you are going to deploy this in production
CBI_DEPLOYMENT_DIR = tempfile.gettempdir()
CBI_CACHE_DIR = os.path.join(CBI_DEPLOYMENT_DIR,
                             'cache/')
CBI_CONFIG_FILE = os.path.join(CBI_DEPLOYMENT_DIR,
                               'cbi_config.cfg')
CBI_CACHE_DATABASE_URI = 'sqlite:////' + os.path.join(
    CBI_CACHE_DIR, 'cbi_dao_cache.db')

logging.basicConfig(level=logging.DEBUG)


dao = CbiDao(CBI_CONFIG_FILE, database_uri=CBI_CACHE_DATABASE_URI)
cbi_wof = WOF(dao)
cbi_wof.config_from_file(CBI_CONFIG_FILE)

app = create_app(cbi_wof)
app.config.from_object(config.DevConfig)

CBIWOFService = create_wof_service_class(cbi_wof)

soap_app = soaplib.core.Application(services=[CBIWOFService],
                                    tns='http://www.cuahsi.org/his/1.0/ws/',
                                    name='WaterOneFlow')

soap_wsgi_app = soaplib.core.server.wsgi.Application(soap_app)

app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/soap/wateroneflow': soap_wsgi_app
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True)
