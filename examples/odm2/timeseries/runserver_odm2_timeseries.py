import logging

import wof

from odm2_timeseries_dao import Odm2Dao
#import private_config

"""
    python runserver_odm2_timeseries.py
    --config=odm2_config_timeseries.cfg
    --connection=mysql+mysqldb://username:password/db_name

"""
logging.basicConfig(level=logging.DEBUG)

def startServer(config='odm2_config_timeseries.cfg',connection=None):
    dao = Odm2Dao(connection)
    app = wof.create_wof_flask_app(dao, config)
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

    parser = argparse.ArgumentParser(description='start WOF for an ODM2 database.')
    parser.add_argument('--config',
                       help='Configuration file', default='odm2_config_timeseries.cfg')
    parser.add_argument('--connection',
                       help='Connection String eg: "mysql+mysqldb://username:password/db_name"')

    args = parser.parse_args()
    print(args)

    startServer(config=args.config,connection=args.connection)
