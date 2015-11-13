import logging
import os
import tempfile
import sys

from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple
from werkzeug.exceptions import NotFound

import wof
from measurement.odm2_measurement_dao import Odm2Dao as measurement
from timeseries.odm2_timeseries_dao import Odm2Dao as timeseries
#from measurement.private_config import odm2_connection_string

logging.basicConfig(level=logging.DEBUG)

M_CONFIG_FILE = './measurement/odm2_config_measurement.cfg'
T_CONFIG_FILE = './timeseries/odm2_config_timeseries.cfg'

def startServer(m_config=M_CONFIG_FILE,
                t_config=T_CONFIG_FILE,
                m_connection=None,
                t_connection=None,
                openPort=8080):
    if m_connection is None and t_connection is None:
        sys.exit("connection string must be provided")
    m_dao = measurement(m_connection)
    t_dao = timeseries(t_connection)

    m_conf = wof.core.wofConfig(m_dao, m_config)
    t_conf = wof.core.wofConfig(t_dao, t_config)

    app= wof.core.create_wof_flask_multiple({m_conf,t_conf},templates='../../wof/apps/templates')

    url = "http://127.0.0.1:" + str(openPort)
    print "----------------------------------------------------------------"
    print "Service endpoints"
    for path in wof.core.site_map_flask_wsgi_mount(app):
        print "%s%s" % (url,path)

    print "----------------------------------------------------------------"
    print "----------------------------------------------------------------"
    print "Acess HTML descriptions of endpoints at "
    for path in wof.site_map(app):
        print "%s%s" % (url,path)

    print "----------------------------------------------------------------"

    app.run(host='0.0.0.0', port=openPort, threaded=True)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='start WOF for an ODM2 database.')
    parser.add_argument('--timeseries',
                       help='Timeseries Configuration file', default=M_CONFIG_FILE)
    parser.add_argument('--measurement',
                       help='Measurement Configuration file', default=T_CONFIG_FILE)
    parser.add_argument('--timeseries_connection',
                       help='Connection String eg: "mysql+mysqldb://username:password/db_name"')
    parser.add_argument('--measurement_connection',
                       help='Connection String eg: "postgresql+psycopg2://username:password/db_name"')
    parser.add_argument('--port',
                       help='Open port for server."', default=8080)
    args = parser.parse_args()
    print(args)

    startServer( m_config=args.timeseries,
                 t_config=args.measurement,
                 m_connection=args.measurement_connection,
                 t_connection=args.timeseries_connection,
                 openPort=args.port )


