
import logging
import ConfigParser

import wof
from wof.core import WOFConfig

from odm_dao import OdmDao
#import private_config

"""
    python runserver_odm11.py
    --config=lbr_config.cfg
    --connection=mssql+pyodbc://webservice:webservice@localhost/LittleBear11?driver=SQL+Server+Native+Client+10.0

"""
logging.basicConfig(level=logging.DEBUG)

def startServer(config='lbr_config.cfg',connection=None,openPort=8080):

    dao = OdmDao(connection)
    app = wof.create_wof_flask_app(dao, config)
    app.config['DEBUG'] = True

    configFile = WOFConfig(config)

    url = "http://127.0.0.1:" + str(openPort)
    print "----------------------------------------------------------------"
    print "Acess Service endpoints at "
    for path in wof.site_map(app):
        print "%s%s" % (url,path)

    print "----------------------------------------------------------------"

    app.run(host='0.0.0.0', port=openPort, threaded=True)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='start WOF for an ODM1 database.')
    parser.add_argument('--config',
                       help='Configuration file')
    parser.add_argument('--connection',
                       help='Connection String eg: "mssql+pyodbc://username:password@localhost/LittleBear11?driver=SQL+Server+Native+Client+10.0"')

    parser.add_argument('--port',
                       help='Open port for server."', default=8080)
    args = parser.parse_args()
    print(args)

    startServer(config=args.config,connection=args.connection,openPort=args.port)
