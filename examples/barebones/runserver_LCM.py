import soaplib
import logging

import wof

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

dao = LCMDao('sqlite:///LCM_Data/LCM.db', 'LCM_config.cfg')
app = wof.create_wof_app(dao, 'LCM_config.cfg')
app.config['DEBUG'] = True

if __name__ == '__main__':
    print "-----------------------------------------------------------------"
    print "Access 'REST' endpoints at http://127.0.0.1:8080/"
    print "Access SOAP WSDLs at http://127.0.0.1:8080/soap/wateroneflow.wsdl"
    print "-----------------------------------------------------------------"

    app.run(host='0.0.0.0', port=8080, threaded=True)
