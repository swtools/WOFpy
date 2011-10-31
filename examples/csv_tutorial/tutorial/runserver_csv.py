import soaplib
import logging

import wof

from csv_dao import CsvDao

PORT = 5000 # Use a port that is available on your computer, e.g., 8080, 5000
CSV_CONFIG_FILE = 'csv_config.cfg'
SITES_FILE = 'sites.csv'
VALUES_FILE = 'data.csv'

logging.basicConfig(level=logging.DEBUG)

#dao = CsvDao(SITES_FILE, VALUES_FILE)
dao = CsvDao(SITES_FILE)
app = wof.create_wof_app(dao, CSV_CONFIG_FILE)
app.config['DEBUG'] = True

if __name__ == '__main__':
    soapEndpoint = "/soap/wateroneflow.wsdl"
    print "----------------------------------------------------------------"
    print "Access 'REST' endpoints at http://127.0.0.1:" + str(PORT) + "/"
    print "Access SOAP WSDL at http://127.0.0.1:" + str(PORT) + soapEndpoint
    print "----------------------------------------------------------------"

    app.run(host='0.0.0.0', port=PORT, threaded=True)
