import logging
import os
import tempfile

import wof

from cbi_dao import CbiDao

# change the cache dir if you are going to deploy this in production
CBI_CACHE_DIR = tempfile.gettempdir()

CBI_CONFIG_FILE = 'cbi_config.cfg'
CBI_CACHE_DATABASE_URI = 'sqlite:///' + os.path.join(
    CBI_CACHE_DIR, 'cbi_dao_cache.db')

logging.basicConfig(level=logging.DEBUG)

cbi_dao = CbiDao(CBI_CONFIG_FILE, database_uri=CBI_CACHE_DATABASE_URI)
app = wof.create_wof_app(cbi_dao, CBI_CONFIG_FILE)
app.config['DEBUG'] = True

if __name__ == '__main__':
    print "-----------------------------------------------------------------"
    print "Access 'REST' endpoints at http://127.0.0.1:8080/"
    print "Access SOAP WSDLs at http://127.0.0.1:8080/soap/wateroneflow.wsdl"
    print "-----------------------------------------------------------------"
    print CBI_CACHE_DATABASE_URI
    app.run(host='0.0.0.0', port=8080, threaded=True)
