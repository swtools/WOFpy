
from frontends.wofpy_flask import app as flask_app
import frontends.wofpy_flask.config
from wof import *
from wof.code import *
import OdmSqlAlchDao



if __name__ == '__main__':
	
	flask_app.config.from_object(frontends.wofpy_flask.config.DevConfig)
	
	wof.config_from_file('config/lbr_config.cfg')
	wof.dao = OdmSqlAlchDao.OdmSqlAlchDao()
	
	flask_app.run(host='0.0.0.0', port=8080, threaded=True)