import soaplib
import logging

import wof

from odm_dao import OdmDao
import private_config

logging.basicConfig(level=logging.DEBUG)

dao = OdmDao(private_config.lbr_connection_string)
app = wof.create_wof_app(dao, 'lbr_config.cfg')
app.config['DEBUG'] = True

if __name__ == '__main__':
    print "-----------------------------------------------------------------"
    print "Access 'REST' endpoints at http://127.0.0.1:8080/"
    print "Access SOAP WSDLs at http://127.0.0.1:8080/soap/wateroneflow.wsdl"
    print "-----------------------------------------------------------------"

    app.run(host='0.0.0.0', port=8080, threaded=True)
