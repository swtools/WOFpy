import logging
import os
import tempfile

import wof

from cbi_dao import CbiDao

""" Before running this script, run build_cbi_cache.py to build a cache of
    sites and variables available from CBI.
"""

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
    # This must be an available port on your computer.  
    # For example, if 8080 is already being used, try another port such as
    # 5000 or 8081.
    openPort = 8080 

    url = "http://127.0.0.1:" + str(openPort) + "/"

    print "----------------------------------------------------------------"
    print "Access 'REST' endpoints at " + url
    print "Access SOAP WSDL at " + url + "soap/wateroneflow.wsdl"
    print "----------------------------------------------------------------"

    app.run(host='0.0.0.0', port=openPort, threaded=True)

    print CBI_CACHE_DATABASE_URI

