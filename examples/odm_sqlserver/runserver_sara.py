import soaplib
import logging

import wof

from odm_dao import OdmDao
import private_config

logging.basicConfig(level=logging.DEBUG)


dao = OdmDao(private_config.sara_connection_string)
app = wof.create_wof_app(swis_dao, 'sara_config.cfg')
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
