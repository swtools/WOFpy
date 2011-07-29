import soaplib
import logging

from werkzeug.wsgi import DispatcherMiddleware
from soaplib.core.server import wsgi

from wof import WOF
from wof.soap import create_wof_service_class
from wof.flask import config
from wof.flask import create_app
from LCM_dao import LCMDao

logging.basicConfig(level=logging.DEBUG)

'''
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

swis_connection_string = 'sqlite:///C:\PythonSandbox\WOFpy_Sandbox\WOFpy\examples\swis\swis2.db'

You can use relative paths too, e.g. if you are calling the above database from the same directory, 
the connection string can just be:

swis_connection_string = 'sqlite:///swis2.db' 
'''

LCM_connection_string = 'sqlite:///LCM_Data\LCM.db'

dao = LCMDao(LCM_connection_string,'LCM_config.cfg')
LCM_wof = WOF(dao)
LCM_wof.config_from_file('LCM_config.cfg')

app = create_app(LCM_wof)
app.config.from_object(config.DevConfig)

ODMWOFService = create_wof_service_class(LCM_wof)

soap_app = soaplib.core.Application(services=[ODMWOFService],
                                    tns='http://www.cuahsi.org/his/1.0/ws/',
                                    name='WaterOneFlow')

soap_wsgi_app = soaplib.core.server.wsgi.Application(soap_app)

app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
     '/soap/wateroneflow': soap_wsgi_app,   
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True)
