from wof import app as flask_app
from wof.soap import *


import wof.config

import soaplib #soaplib 2.0.0-beta

from werkzeug.wsgi import DispatcherMiddleware

if __name__ == '__main__':
	soap_application = soaplib.core.Application([WOFService], 'http://www.cuahsi.org/his/1.0/ws/')
	soap_wsgi_application = wsgi.Application(soap_application)
	
	flask_app.wsgi_app = DispatcherMiddleware(flask_app.wsgi_app, {
		'/soap': soap_wsgi_application
		})

	#CHANGE THIS TO LOAD DIFFERENT CONFIGURATION PARAMETERS
	config_obj = wof.config.LBRConfig()
	
	#Must specify a valid db connection string here
	import private_config
	config_obj.SQLALCHEMY_DATABASE_URI = private_config.database_connection_string
	
	
	flask_app.config.from_object(config_obj)	

	flask_app.run(host='0.0.0.0', port=8080)