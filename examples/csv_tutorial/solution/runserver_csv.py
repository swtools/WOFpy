import logging

import wof

from csv_dao import CsvDao

CSV_CONFIG_FILE = 'csv_config.cfg'
SITES_FILE = 'sites.csv'
VALUES_FILE = 'data.csv'

logging.basicConfig(level=logging.DEBUG)

def startServer(config=CSV_CONFIG_FILE,
                sites_file=SITES_FILE,
                values_file=VALUES_FILE):
    dao = CsvDao(sites_file, values_file)
    app = wof.create_wof_flask_app(dao, config)
    app.config['DEBUG'] = True
    site_map = wof.site_map(app)

    openPort = 8080
    url = "http://127.0.0.1:" + str(openPort)
    print "----------------------------------------------------------------"
    print "Acess Service endpoints at "
    for path in wof.site_map(app):
        print "%s%s" % (url,path)

    print "----------------------------------------------------------------"

    app.run(host='0.0.0.0', port=openPort, threaded=True)

if __name__ == '__main__':
    # This must be an available port on your computer.  
    # For example, if 8080 is already being used, try another port such as
    # 5000 or 8081.
    import argparse

    parser = argparse.ArgumentParser(description='start WOF for an ODM1 database.')
    parser.add_argument('config',
                       help='Configuration file', default=CSV_CONFIG_FILE)
    parser.add_argument('--sites_file',
                       help='csv file containing sites information',default=SITES_FILE)
    parser.add_argument('--values_file',
                       help='csv file containing values',default=VALUES_FILE)


    args = parser.parse_args()
    print(args)

    startServer(config=args.config,sites_file=args.sites_file,values_file=args.values_file)
