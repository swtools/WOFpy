import cherrypy
import win32serviceutil
import win32service

import wof.config

from wof import app as flask_app

config_obj = wof.config.ProductionConfig

import private_config
config_obj.SQLALCHEMY_DATABASE_URI = private_config.database_connection_string

flask_app.config.from_object(config_obj)

from wofpy_soap.soap import WOFService
import soaplib #soaplib 2.0.0-beta

soap_application = soaplib.core.Application([WOFService], 'http://www.cuahsi.org/his/1.0/ws/')
soap_wsgi_application = wsgi.Application(soap_application)

class MyService(win32serviceutil.ServiceFramework):
    """NT Service."""
    
    _svc_name_ = "WOFPy_TWDB_Sondes_Server"
    _svc_display_name_ = "WOFPy_TWDB_Sondes_Server"

    def SvcDoRun(self):
        cherrypy.tree.graft(soap_wsgi_application, '/WOFPy/soap/TWDB_Sondes')
        cherrypy.tree.graft(flask_app, '/WOFPy/TWDB_Sondes')
        
        # in practice, you will want to specify a value for
        # log.error_file below or in your config file.  If you
        # use a config file, be sure to use an absolute path to
        # it, as you can't be assured what path your service
        # will run in.
        cherrypy.config.update({
            'global':{
                'log.screen': False,
                'engine.autoreload.on': False,
                'engine.SIGHUP': None,
                'engine.SIGTERM': None,
                'server.socket_port' : 80,
                'server.socket_host': 'crwr-hydroportal.austin.utexas.edu'
                }
            })
        
        cherrypy.engine.start()
        cherrypy.engine.block()
        
    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        cherrypy.engine.exit()
        
        self.ReportServiceStatus(win32service.SERVICE_STOPPED) 
        # very important for use with py2exe
        # otherwise the Service Controller never knows that it is stopped !
        
if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(MyService)
