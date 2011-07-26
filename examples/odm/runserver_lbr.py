import soaplib
import logging

import wof

from odm_dao import OdmDao
import private_config

logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    dao = OdmDao(private_config.lbr_connection_string)
    app = wof.create_wof_app(dao, 'lbr_config.cfg')
    app.config['DEBUG'] = True

    app.run(host='0.0.0.0', port=8080, threaded=True)
