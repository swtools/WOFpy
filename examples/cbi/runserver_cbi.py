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

# cbi_dao = CbiDao(CBI_CONFIG_FILE, database_uri=CBI_CACHE_DATABASE_URI)
# app = wof.create_wof_flask_app(cbi_dao, CBI_CONFIG_FILE)
# app.config['DEBUG'] = True

def startServer(config=CBI_CONFIG_FILE,connection=CBI_CACHE_DATABASE_URI):

    cbi_dao = CbiDao(CBI_CONFIG_FILE, database_uri=CBI_CACHE_DATABASE_URI)
    app = wof.create_wof_flask_app(cbi_dao, config)
    app.config['DEBUG'] = True


    openPort = 8080
    url = "http://127.0.0.1:" + str(openPort)
    print "----------------------------------------------------------------"
    print "Acess Service endpoints at "
    for path in wof.site_map(app):
        print "%s%s" % (url,path)

    print "----------------------------------------------------------------"

    app.run(host='0.0.0.0', port=openPort, threaded=True)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='start WOF for an CBI Example. Cache and database creation must be run befroe this example')
    parser.add_argument('--config',
                       help='Configuration file', default=CBI_CONFIG_FILE)
    parser.add_argument('--connection',
                       help='Connection String eg: "sqlite:///LCM_Data/LCM.db"', default=CBI_CACHE_DATABASE_URI)

    args = parser.parse_args()
    print(args)

    startServer(config=args.config,connection=args.connection)

    print CBI_CACHE_DATABASE_URI

