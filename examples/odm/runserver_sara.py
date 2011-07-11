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
    app.run(host='0.0.0.0', port=8080, threaded=True)
