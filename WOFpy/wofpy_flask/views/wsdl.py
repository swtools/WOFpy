

from flask import (Flask, request, Markup, Response, render_template,
                   make_response, Module, current_app)

wsdl = Module(__name__)

@wsdl.route('/soap/wateroneflow.wsdl')
def get_wsdl():
#TODO: The WSDL should be served separately from the Flask application.
# Come up with a better way to do this.
    network = current_app.wof_inst.network.lower()
    if (network == 'lbr' or network == 'swis' or network == 'cbi'):

        serv_loc = 'http://%s/soap/%s/WOFService' %\
            (request.environ['HTTP_HOST'], network)
        
        response = make_response(render_template('wsdl_temp.wsdl',
                                                 serv_loc=serv_loc,
                                                 network=network))
        
        response.headers['Content-Type'] = 'text/xml'
        
        return response
    else:
        return "Network '"+network+"' not registered."