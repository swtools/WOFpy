import wof.config
import soaplib #soaplib 2.0.0-beta

from wof import WofPyApplication
from wof.soap import *
from werkzeug.wsgi import DispatcherMiddleware

if __name__ == '__main__':
	
	wofpy_app = WofPyApplication()
	
	soap_application = soaplib.core.Application([WOFService], 'http://www.cuahsi.org/his/1.0/ws/')
	soap_wsgi_application = wsgi.Application(soap_application)
	
	wofpy_app.app.wsgi_app = DispatcherMiddleware(wofpy_app.app.wsgi_app, {
		'/soap': soap_wsgi_application
		})

	#CHANGE THIS TO LOAD DIFFERENT CONFIGURATION PARAMETERS
	config_obj = wof.config.LBRConfig()
	
	#Must specify a valid db connection string here
	import private_config
	config_obj.SQLALCHEMY_DATABASE_URI = private_config.database_connection_string
	
	
	wofpy_app.app.config.from_object(config_obj)	

	wofpy_app.app.run(host='0.0.0.0', port=8080)