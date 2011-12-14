import soaplib
import logging

import wof

from csv_dao import CsvDao

CSV_CONFIG_FILE = 'csv_config.cfg'
SITES_FILE = 'sites.csv'
VALUES_FILE = 'data.csv'

logging.basicConfig(level=logging.DEBUG)

dao = CsvDao(SITES_FILE, VALUES_FILE)
app = wof.create_wof_app(dao, CSV_CONFIG_FILE)
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
