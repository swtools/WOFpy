
import logging

import wof

from odm_dao import OdmDao
import private_config

""" Before running this script, create a private_config.py file with the 
    connection string to your ODM database in SQL Server.  For example:
    
    lbr_connection_string = \
    'mssql+pyodbc://username:password@(local)/LittleBear11'
"""

logging.basicConfig(level=logging.DEBUG)

dao = OdmDao(private_config.lbr_connection_string)
app = wof.create_wof_flask_app(dao, 'lbr_config.cfg')
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
