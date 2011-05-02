

from flask import (Flask, request, Markup, Response, render_template,
                   make_response, Module)

wsdl = Module(__name__)

@wsdl.route('/<network>.wsdl')
def get_wsdl(network):
#TODO: The WSDL should be served separately from the Flask application
    if network == 'lbr' or network == 'swis':
        #TODO: should have different serv_loc based on network
        serv_loc = 'http://crwr-little.austin.utexas.edu:8080/soap/WOFService'
        response = make_response(render_template('wsdl_temp.wsdl',
                                                 serv_loc=serv_loc,
                                                 network=network))
        
        response.headers['Content-Type'] = 'text/xml'
        
        return response
    else:
        return "Network '"+network+"' not registered."