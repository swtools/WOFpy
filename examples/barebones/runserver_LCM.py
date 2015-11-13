
import logging

from werkzeug.wsgi import DispatcherMiddleware

import wof

from wof.flask import config
from wof.flask import create_app
from LCM_dao import LCMDao

logging.basicConfig(level=logging.DEBUG)

'''
Be sure to assign an available port to the openPort variable below!

The standard syntax for connection string is a URL in the form:
dialect://user:password@host/dbname[?key=value..],
where dialect is a name such as mysql, oracle, sqlite postgres,etc. 

1.  Example for MSSQL

database_connection_string = 'mssql+pyodbc://odm_user2:water123@JAMTAY-PC\SQLEXPRESS/LittleBear11'
"odm_user2" is a user with (at least) read privileges on the database,
"water123" is the password,
"JAMTAY-PC\SQLEXPRESS" is the name of my MSSQL server (you can see what yours is called when you
connect with SQL Server Management Studio).
"LittleBear11" is the name of the database.
database_connection_string = 'mssql+pyodbc://odm_user2:water123@JAMTAY-PC\SQLEXPRESS/LittleBear11'

2.  Example for SQLite

swis_connection_string = 'sqlite:///C:/PythonSandbox/WOFpy_Sandbox/WOFpy/examples/swis/swis2.db'

You can use relative paths too, e.g. if you are calling the above database from the same directory, 
the connection string can just be:

swis_connection_string = 'sqlite:///swis2.db' 
'''

LCM_connection_string = 'sqlite:///LCM_Data/LCM.db'
CONFIG='LCM_config.cfg'
#
# dao = LCMDao(LCM_connection_string,'LCM_config.cfg')
# LCM_wof = WOF(dao)
# LCM_wof.config_from_file('LCM_config.cfg')
#
# app = create_app(LCM_wof)
# app.config.from_object(config.DevConfig)
#
# ODMWOFService = wof.create_wof_service_class(LCM_wof)
#
# soap_app = soaplib.core.Application(services=[ODMWOFService],
#                                     tns='http://www.cuahsi.org/his/1.0/ws/',
#                                     name='WaterOneFlow')
#
# soap_wsgi_app = soaplib.core.server.wsgi.Application(soap_app)
#
# app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
#      '/soap/wateroneflow': soap_wsgi_app,
#     })

def startServer(config='LCM_config.cfg',connection='sqlite:///LCM_Data/LCM.db', openPort=8080):

    dao = LCMDao(connection,config)
    app = wof.create_wof_flask_app(dao, config)
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
                       help='Configuration file', default=CONFIG)
    parser.add_argument('--connection',
                       help='Connection String eg: "sqlite:///LCM_Data/LCM.db"', default=LCM_connection_string)
    parser.add_argument('--port',
                       help='Open port for server."', default=8080)
    args = parser.parse_args()
    print(args)

    startServer(config=args.config,connection=args.connection, openPort=args.port)
