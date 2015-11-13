from flask import Flask, render_template, current_app, make_response, request

import config
import datetime

def create_simple_app():
    app = Flask(__name__)

    app.config.from_object(config.Config)
    return app

#TODO: Error handlers (404, etc.)
def create_app(wof_inst, wof_inst_1_1, soap_service_url=None, soap_service_1_1_url=None):
    # app = Flask(__name__)
    #
    # app.config.from_object(config.Config)
    app = create_simple_app()
    path = wof_inst.network
    servicesPath =  '/'+wof_inst.network
    add_flask_routes(app,path,servicesPath,wof_inst,
                     wof_inst_1_1,soap_service_url=soap_service_url, soap_service_1_1_url=soap_service_1_1_url )
    return app

def add_flask_routes(app,path, servicesPath,
                     wof_inst,
                     wof_inst_1_1,
                     soap_service_url=None,
                     soap_service_1_1_url=None):

    # app.wof_inst = wof_inst
    # app.wof_inst_1_1 = wof_inst_1_1
    # path = wof_inst.network
    # servicesPath =  '/'+wof_inst.network

    #@app.route( '/')
    def index():
        return render_template('index.html',
                               rest10=path+'/rest_1_0/',
                               rest11=path+'/rest_1_1/',
                               rest2=path+'/rest_2/',
                               soap10=path+'/soap/wateroneflow/.wsdl',
                               soap11=path+'/soap/wateroneflow_1_1/.wsdl',
                               p=wof_inst.network)

    app.add_url_rule(servicesPath+'/', wof_inst.network+'index', index)

    def index_2_0():
        return render_template('index_2.html',
                       path= path + '/rest/2/',
                       p=wof_inst.network,
                       s=wof_inst.default_site,
                       v=wof_inst.default_variable,
                       sd=wof_inst.default_start_date,
                       ed=wof_inst.default_end_date,
                       u=wof_inst.default_unitid,
                       sm=wof_inst.default_samplemedium)
    app.add_url_rule(servicesPath+'/rest_2/', wof_inst.network+'index_2_0', index_2_0)

    if wof_inst is not None:
        if not 'SOAP_SERVICE_URL' in app.config and soap_service_url:
            app.config['SOAP_SERVICE_URL'] = soap_service_url

        #@app.route('/rest_1_0/')
        def index_1_0():
            return render_template('index_1_0.html',
                           path= path + '/rest/1_0/',
                           p=wof_inst.network,
                           s=wof_inst.default_site,
                           v=wof_inst.default_variable,
                           sd=wof_inst.default_start_date,
                           ed=wof_inst.default_end_date,
                           u=wof_inst.default_unitid,
                           sm=wof_inst.default_samplemedium)
        app.add_url_rule(servicesPath+'/rest_1_0/',wof_inst.network+ 'index_1_0', index_1_0)



        # #@app.route('/soap/wateroneflow.wsdl')
        # def get_wsdl():
        # #TODO: The WSDL should be served separately from the Flask application.
        # # Come up with a better way to do this.
        #     network = wof_inst.network.lower()
        #
        #     try:
        #         serv_loc = app.config['SOAP_SERVICE_URL']
        #     except KeyError:
        #         serv_loc = app.config.get(
        #             'SOAP_SERVICE_URL',
        #             '%s/wateroneflow/' % request.url.rsplit('/', 1)[0])
        #
        #     response = make_response(render_template('wsdl_temp.wsdl',
        #                                      serv_loc=serv_loc,
        #                                      network=network))
        #
        #     response.headers['Content-Type'] = 'text/xml'
        #     return response
        # app.add_url_rule(servicesPath+'/soap/wateroneflow.wsdl', wof_inst.network+'get_wsdl', get_wsdl)

    if wof_inst_1_1 is not None:
        if not 'SOAP_SERVICE_URL_1_1' in app.config and soap_service_1_1_url:
            app.config['SOAP_SERVICE_URL_1_1'] = soap_service_1_1_url

        #@app.route('/rest_1_1/')
        def index_1_1():
            return render_template('index_1_1.html',
                           path=path+'/rest/1_1/',
                           p=wof_inst_1_1.network,
                           s=wof_inst_1_1.default_site,
                           v=wof_inst_1_1.default_variable,
                           sd=wof_inst_1_1.default_start_date,
                           ed=wof_inst_1_1.default_end_date,
                           w=wof_inst_1_1.default_west,
                           so=wof_inst_1_1.default_south,
                           n=wof_inst_1_1.default_north,
                           e=wof_inst_1_1.default_east)
        app.add_url_rule(servicesPath+'/rest_1_1/', wof_inst.network+'index_1_1', index_1_1)

        #@app.route('/soap/wateroneflow_1_1.wsdl')
        # def get_wsdl_1_1():
        # #TODO: The WSDL should be served separately from the Flask application.
        # # Come up with a better way to do this.
        #     network = wof_inst_1_1.network.lower()
        #
        #     try:
        #         serv_loc = app.config['SOAP_SERVICE_URL_1_1']
        #     except KeyError:
        #         serv_loc = app.config.get(
        #             'SOAP_SERVICE_URL_1_1',
        #             '%s/wateroneflow_1_1/' % request.url.rsplit('/', 1)[0])
        #
        #     response = make_response(render_template('wsdl_1_1_template.wsdl',
        #                                      serv_loc=serv_loc,
        #                                      network=network))
        #
        #     response.headers['Content-Type'] = 'text/xml'
        #     return response
        # app.add_url_rule(servicesPath+'/soap/wateroneflow_1_1.wsdl', wof_inst.network+'get_wsdl_1_1', get_wsdl_1_1)


    return app
