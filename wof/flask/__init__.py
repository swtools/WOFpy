from flask import Flask, render_template

import config
from wof.flask.views.rest import rest
from wof.flask.views.wsdl import wsdl

try:
    from flask import Blueprint
    USE_BLUEPRINTS = True
except ImportError:
    USE_BLUEPRINTS = False


#TODO: Error handlers (404, etc.)
def create_app(wof_inst, soap_service_url=None):
    app = Flask(__name__)

    app.config.from_object(config.Config)
    app.wof_inst = wof_inst
    if not 'SOAP_SERVICE_URL' in app.config and soap_service_url:
        app.config['SOAP_SERVICE_URL'] = soap_service_url

    if USE_BLUEPRINTS:
        app.register_blueprint(rest)
        app.register_blueprint(wsdl)
    else:
        app.register_module(rest)
        app.register_module(wsdl)

    return app
