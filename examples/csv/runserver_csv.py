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
    print "----------------------------------------------------------------"
    print "Access 'REST' endpoints at http://127.0.0.1:8080/"
    print "Access SOAP WSDL at http://127.0.0.1:8080/soap/wateroneflow.wsdl"
    print "----------------------------------------------------------------"

    app.run(host='0.0.0.0', port=8080, threaded=True)
