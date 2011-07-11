import soaplib
import logging

import wof

from swis_dao import SwisDao

SWIS_DATABASE_URI = 'sqlite:///swis2.db'
SWIS_CONFIG_FILE = 'swis_config.cfg'

logging.basicConfig(level=logging.DEBUG)

swis_dao = SwisDao(SWIS_CONFIG_FILE, database_uri=SWIS_DATABASE_URI)
app = wof.create_wof_app(swis_dao, SWIS_CONFIG_FILE)
app.config['DEBUG'] = True

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True)
