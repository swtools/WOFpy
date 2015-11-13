
import logging

import wof

from swis_dao import SwisDao

SWIS_DATABASE_URI = 'sqlite:///swis2.db'
SWIS_CONFIG_FILE = 'swis_config.cfg'

logging.basicConfig(level=logging.DEBUG)

# swis_dao = SwisDao(SWIS_CONFIG_FILE, database_uri=SWIS_DATABASE_URI)
# app = wof.create_wof_flask_app(swis_dao, SWIS_CONFIG_FILE)
# app.config['DEBUG'] = True

def startServer(config=SWIS_CONFIG_FILE,connection=SWIS_DATABASE_URI, openPort=8080):

    swis_dao = SwisDao(SWIS_CONFIG_FILE, database_uri=connection)
    app = wof.create_wof_flask_app(swis_dao, config)
    app.config['DEBUG'] = True


    url = "http://127.0.0.1:" + str(openPort)
    print "----------------------------------------------------------------"
    print "Acess Service endpoints at "
    for path in wof.site_map(app):
        print "%s%s" % (url,path)

    print "----------------------------------------------------------------"

    app.run(host='0.0.0.0', port=openPort, threaded=True)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='start WOF for an LCM Example.')
    parser.add_argument('--config',
                       help='Configuration file', default=SWIS_CONFIG_FILE)
    parser.add_argument('--connection',
                       help='Connection String eg: "sqlite:///LCM_Data/LCM.db"', default=SWIS_DATABASE_URI)

    parser.add_argument('--port',
                       help='Open port for server."', default=8080)
    args = parser.parse_args()
    print(args)

    startServer(config=args.config,connection=args.connection, openPort=args.port)
