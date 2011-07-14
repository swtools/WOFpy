import soaplib
import logging

import wof

from test_dao import TestDao

logging.basicConfig(level=logging.DEBUG)


def create_app():
    test_dao = TestDao()
    app = wof.create_wof_app(test_dao, 'test_config.cfg')
    app.config['DEBUG'] = True

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8080, threaded=True)
