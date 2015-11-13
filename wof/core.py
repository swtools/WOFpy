import datetime
import ConfigParser
import os

import werkzeug
import wof.flask
import wof.core_1_1 as wof_1_1
import wof.core_1_0 as wof_1_0

from spyne.server.wsgi import WsgiApplication
from spyne.application import Application
from spyne.model.primitive import Unicode, AnyXml
from spyne.protocol.soap import Soap11
from spyne.protocol.http import HttpRpc
from spyne.protocol.xml import XmlDocument

from wof.apps.spyned_1_0 import TWOFService as wml10
from wof.apps.spyned_1_1 import TWOFService as wml11
from wof.apps.waterml2 import TWOFService as wml2
from  wof.WofWsdls import WofWSDL_1_0, WofWSDL_1_1


import urllib

import logging
#logging.basicConfig(level=logging.INFO)
logging.getLogger('spyne.model.complex').setLevel(logging.ERROR)
logging.getLogger('spyne.interface._base').setLevel(logging.ERROR)
logging.getLogger('spyne.util.appreg').setLevel(logging.ERROR)
logging.getLogger('spyne.interface.xml_schema').setLevel(logging.ERROR)
logging.getLogger('spyne.protocol.dictdoc.simple').setLevel(logging.ERROR)

_SERVICE_PARAMS = {
    "r_type" : "rest",
    "s_type" : "soap",
    "wml10_tns" : "http://www.cuahsi.org/his/1.0/ws/",
    "wml11_tns" : "http://www.cuahsi.org/his/1.1/ws/",
    "wml10_rest_name" : "WaterOneFlow_rest_1_0",
    "wml10_soap_name" : "WaterOneFlow_soap_1_0",
    "wml11_rest_name" : "WaterOneFlow_rest_1_1",
    "wml11_soap_name" : "WaterOneFlow_soap_1_1",
}

def site_map(app):
    output = []
    for rule in app.url_map.iter_rules():
        methods = ','.join(rule.methods)
        #line = urllib.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, rule))
        line = urllib.unquote("{}".format(rule))
        if '/static/' in line or '/rest/' in line:
            continue
        output.append(line)

    #print "Acess Service Path at "
    #for line in sorted(output):
    #    print(line)
    return sorted(output)

def site_map_flask_wsgi_mount(app):
    output = []
    for mount in app.wsgi_app.mounts:
        method = app.wsgi_app.mounts[mount].app.name
        #methods = ','.join(mounts[.app.name)
        #path = mount.key
        #line = urllib.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, rule))
        line = urllib.unquote("{}".format(mount))
        if '/static/' in line:
            #or '/rest/' in line:
            continue
        output.append(line)

    #print "Acess Service Path at "
    #for line in sorted(output):
    #    print(line)
    return sorted(output)

class WOFConfig(object):
        network = 'NETWORK'
        vocabulary = 'VOCABULARY'
        menu_group_name = 'MENU_GROUP_NAME'
        service_wsdl = 'SERVICE_WSDL'
        timezone = None
        timezone_abbr = None

        default_site = None
        default_variable = None
        default_start_date = None
        default_end_date = None
        default_unitid = None
        default_samplemedium = None

        default_west = None
        default_south = None
        default_north = None
        default_east = None

        TEMPLATES = '../../wof/apps/templates'

        def __init__(self, file_name,templates=None):
            config = ConfigParser.RawConfigParser()
            config.read(file_name)

            if config.has_option('WOF_1_1','Network'):
                self.network = config.get('WOF_1_1', 'Network')
            else:
                self.network = config.get('WOF', 'Network')
            if config.has_option('WOF_1_1','Vocabulary'):
                self.vocabulary = config.get('WOF_1_1', 'Vocabulary')
            else:
                self.vocabulary = config.get('WOF', 'Vocabulary')
            if config.has_option('WOF_1_1','Menu_Group_Name'):
                self.menu_group_name = config.get('WOF_1_1', 'Menu_Group_Name')
            else:
                self.menu_group_name = config.get('WOF', 'Menu_Group_Name')
            if config.has_option('WOF_1_1','Service_WSDL'):
                self.service_wsdl = config.get('WOF_1_1', 'Service_WSDL')
            else:
                self.service_wsdl = config.get('WOF', 'Service_WSDL')
            if config.has_option('WOF_1_1','Timezone'):
                self.timezone = config.get('WOF_1_1', 'Timezone')
            else:
                self.timezone = config.get('WOF', 'Timezone')
            if config.has_option('WOF_1_1','TimezoneAbbreviation'):
                self.timezone_abbr = config.get('WOF_1_1', 'TimezoneAbbreviation')
            else:
                self.timezone_abbr = config.get('WOF', 'TimezoneAbbreviation')

            if config.has_section('Default_Params'):
                if config.has_option('Default_Params','UnitID'):
                    self.default_unitid = config.get('Default_Params','UnitID')
                if config.has_option('Default_Params','SampleMedium'):
                    self.default_samplemedium = config.get('Default_Params','SampleMedium')

                if config.has_option('Default_Params_1_1','Site'):
                    self.default_site = config.get('Default_Params_1_1', 'Site')
                else:
                    self.default_site = config.get('Default_Params', 'Site')
                if config.has_option('Default_Params_1_1','Variable'):
                    self.default_variable = config.get('Default_Params_1_1', 'Variable')
                else:
                    self.default_variable = config.get('Default_Params', 'Variable')
                if config.has_option('Default_Params_1_1','StartDate'):
                    self.default_start_date = config.get('Default_Params_1_1', 'StartDate')
                else:
                    self.default_start_date = config.get('Default_Params', 'StartDate')
                if config.has_option('Default_Params_1_1','EndDate'):
                    self.default_end_date = config.get('Default_Params_1_1', 'EndDate')
                else:
                    self.default_end_date = config.get('Default_Params', 'EndDate')
                if config.has_option('Default_Params_1_1','East'):
                    self.default_east = config.get('Default_Params_1_1', 'East')
                else:
                    if config.has_option('Default_Params','East'):
                        self.default_east = config.get('Default_Params', 'East')
                    else:
                        self.default_east = 180
                if config.has_option('Default_Params_1_1','North'):
                    self.default_north = config.get('Default_Params_1_1','North')
                else:
                    if config.has_option('Default_Params','North'):
                        self.default_north = config.get('Default_Params', 'North')
                    else:
                        self.default_north = 90
                if config.has_option('Default_Params_1_1','South'):
                    self.default_south = config.get('Default_Params_1_1', 'South')
                else:
                    if config.has_option('Default_Params','South'):
                        self.default_south= config.get('Default_Params', 'South')
                    else:
                        self.default_south = -90
                if config.has_option('Default_Params_1_1','West'):
                    self.default_west = config.get('Default_Params_1_1', 'West')
                else:
                    if config.has_option('Default_Params','West'):
                        self.default_west = config.get('Default_Params', 'West')
                    else:
                        self.default_west = -180

            if templates is not None:
                self.TEMPLATES = templates
            elif config.has_option('WOFPY','Templates'):
                self.TEMPLATES = config.get('WOFPY', 'Templates')
            else:
                self.TEMPLATES = '../../wof/apps/templates'

""" returns an array of the applications """
def getSpyneApplications(wof_obj_1_0, wof_obj_1_1, templates=None):

    # wof_obj_1_0 = wof_1_0.WOF(dao, config_file)
    # wof_obj_1_1 = wof_1_1.WOF_1_1(dao,config_file)

    sensorNetwork=wof_obj_1_0.network.replace('/','')

    soap_app_1_0 = Application(
        [wml10(wof_obj_1_0,Unicode,_SERVICE_PARAMS["s_type"])],
        tns=_SERVICE_PARAMS["wml10_tns"],
        name=sensorNetwork+'_svc_'+ _SERVICE_PARAMS["wml10_soap_name"],
        in_protocol=Soap11(validator='lxml'),
        out_protocol=Soap11(),
    )

    rest_app_1_0 = Application(
        [wml10(wof_obj_1_0,AnyXml,_SERVICE_PARAMS["r_type"])],
        tns=_SERVICE_PARAMS["wml10_tns"],
        name=sensorNetwork+'_svc_'+  _SERVICE_PARAMS["wml10_rest_name"],
        in_protocol=HttpRpc(validator='soft'),
        out_protocol=XmlDocument(),
    )

    soap_app_1_1 = Application(
        [wml11(wof_obj_1_1,Unicode,_SERVICE_PARAMS["s_type"])],
        tns=_SERVICE_PARAMS["wml11_tns"],
        name=sensorNetwork+'_svc_'+  _SERVICE_PARAMS["wml11_soap_name"],
        in_protocol=Soap11(validator='lxml'),
        out_protocol=Soap11(),
    )

    rest_app_1_1 = Application(
        [wml11(wof_obj_1_1,AnyXml,_SERVICE_PARAMS["r_type"])],
        tns=_SERVICE_PARAMS["wml11_tns"],
        name=sensorNetwork+'_svc_'+  _SERVICE_PARAMS["wml11_rest_name"],
        in_protocol=HttpRpc(validator='soft'),
        out_protocol=XmlDocument(),
    )
    # need to update template to 1_1 object.
    # <gml:Definition gml:id="methodCode-{{ method_result.MethodID  }}">
    #   File "C:\Users\valentin\venv_odm\lib\site-packages\jinja2\environment.py", line 408, in getattr
    #     return getattr(obj, attribute)
    # UndefinedError: 'method_result' is undefined
    rest_app_2 = Application(
        [wml2(wof_obj_1_0,Unicode,_SERVICE_PARAMS["r_type"])],
        tns=_SERVICE_PARAMS["wml11_tns"],
        name=sensorNetwork+'_svc_'+ _SERVICE_PARAMS["wml11_rest_name"],
        in_protocol=HttpRpc(validator='soft'),
        #out_protocol=XmlDocument(),
        out_protocol=HttpRpc(mime_type='text/xml'),

    )

    rest_wsgi_wrapper_1_0 = WsgiApplication(rest_app_1_0)
    soap_wsgi_wrapper_1_0 = WsgiApplication(soap_app_1_0)
    rest_wsgi_wrapper_1_1 = WsgiApplication(rest_app_1_1)
    soap_wsgi_wrapper_1_1 = WsgiApplication(soap_app_1_1)
    rest_wsgi_wrapper_2_0 = WsgiApplication(rest_app_2)

    spyneApps =  {
       '/'+ sensorNetwork+'/rest/1_0': rest_wsgi_wrapper_1_0,
       '/'+ sensorNetwork+'/rest/1_1' : rest_wsgi_wrapper_1_1,
       '/'+ sensorNetwork+'/soap/wateroneflow': soap_wsgi_wrapper_1_0,
       '/'+ sensorNetwork+'/soap/wateroneflow_1_1': soap_wsgi_wrapper_1_1,
        '/'+ sensorNetwork+'/rest/2' : rest_wsgi_wrapper_2_0,
        }
    if templates is None:
        templatesPath = os.path.abspath(wof_obj_1_1._config.TEMPLATES)
    else:
        templatesPath = os.path.abspath(templates)
        #  path: /{sensorNetwork}/soap/wateroneflow/.wsdl returns the WSDL.
    # needs to be service_baseURL. in config wof_obj_1_0.service_wsdl
    wsdl10= WofWSDL_1_0(soap_wsgi_wrapper_1_0.doc.wsdl11.interface, templates=templatesPath)

    #soap_wsgi_wrapper_1_0._wsdl = wsdl10.build_interface_document('/'+ sensorNetwork+'/soap/wateroneflow',templatesPath) #.get_wsdl_1_0('/'+ sensorNetwork+'/soap/wateroneflow')
    soap_wsgi_wrapper_1_0.event_manager.add_listener('wsdl', wsdl10.on_get_wsdl_1_0_)
    #  path: /{sensorNetwork}/soap/wateroneflow_1_1/.wsdl returns the WSDL.
    wsdl11= WofWSDL_1_1(soap_wsgi_wrapper_1_1.doc.wsdl11.interface, templates=templatesPath)
    #soap_wsgi_wrapper_1_1._wsdl = wsdl11.build_interface_document('/'+ sensorNetwork+'/soap/wateroneflow_1_1',templatesPath) #.get_wsdl_1_0('/'+ sensorNetwork+'/soap/wateroneflow')
    soap_wsgi_wrapper_1_1.event_manager.add_listener('wsdl', wsdl11.on_get_wsdl_1_1_)

    return spyneApps


class wofConfig(object):
    dao=None
    config=None
    def __init__(self, dao=None,wofConfig=None):
        self.config = wofConfig
        self.dao = dao

def create_wof_flask_app(dao, config_file):
    """
    Returns a fully instantiated WOF wsgi app (flask + apps)
    """

    # wof_obj_1_0 = wof_1_0.WOF(dao, config_file)
    # wof_obj_1_1 = wof_1_1.WOF_1_1(dao,config_file)
    #
    # # static URL's need to be deprecriated.
    # app = wof.flask.create_app(wof_obj_1_0,wof_obj_1_1)
    #
    # spyneapps = getSpyneApplications(wof_obj_1_0,wof_obj_1_1)
    # app.wsgi_app = werkzeug.wsgi.DispatcherMiddleware(app.wsgi_app, spyneapps)
    wConf = wofConfig(dao=dao,  wofConfig=config_file)
    app = create_wof_flask_multiple({wConf})
    return app



def create_wof_flask_multiple(wofConfig=[], templates=None):
    """
    Returns a fully instantiated WOF wsgi app (flask + apps)
    """
    app = wof.flask.create_simple_app()
    spyneapps = {}
    for wConf in wofConfig:
        wof_obj_1_0 = wof_1_0.WOF(wConf.dao, wConf.config, templates)
        wof_obj_1_1 = wof_1_1.WOF_1_1(wConf.dao,wConf.config,templates)

        spyneapps.update(getSpyneApplications(wof_obj_1_0,wof_obj_1_1,templates) )
        path = wof_obj_1_0.network
        servicesPath =  '/'+wof_obj_1_0.network

        wof.flask.add_flask_routes(app,path, servicesPath,
                     wof_obj_1_0,
                     wof_obj_1_1,
                     soap_service_url=None,
                     soap_service_1_1_url=None)

    app.wsgi_app = werkzeug.wsgi.DispatcherMiddleware(app.wsgi_app, spyneapps)
    return app

def _get_iso8061_datetime_string(object, local_datetime_attr,
                                 utc_datetime_attr):
    """
    Returns a datetime string given an object and the names of the
    attributes for local time and utc date time
    """
    local_datetime = getattr(object, local_datetime_attr, None)
    if local_datetime:
        if type(local_datetime) == datetime.datetime:
            if not local_datetime.tzinfo:
                raise ValueError("local times must be timezone-aware")
            return local_datetime.isoformat()
        else:
            return local_datetime
    else:
        utc_datetime = getattr(object, utc_datetime_attr)
        if type(utc_datetime) == datetime.datetime:
            return utc_datetime.replace(tzinfo=None).isoformat() + 'Z'
        else:
            return utc_datetime
