import logging

import wof

from csv_dao import CsvDao
from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.exceptions import NotFound
CSV_CONFIG_FILE = 'csv_config.cfg'
CSV_CONFIG_FILE2 = 'csv_config_multi.cfg'
SITES_FILE = 'sites.csv'
VALUES_FILE = 'data.csv'

logging.basicConfig(level=logging.DEBUG)

def startServer(config=CSV_CONFIG_FILE,config2=CSV_CONFIG_FILE2,
                sites_file=SITES_FILE,
                values_file=VALUES_FILE):

    dao = CsvDao(sites_file, values_file)

    conf1 = wof.core.wofConfig(dao, config)
    conf2 = wof.core.wofConfig(dao, config2)

    app= wof.core.create_wof_flask_multiple({conf1,conf2})

    openPort = 8080
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
    # This must be an available port on your computer.  
    # For example, if 8080 is already being used, try another port such as
    # 5000 or 8081.


    startServer()
