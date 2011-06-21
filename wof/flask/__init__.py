from flask import Flask, render_template

import config
from wof.flask.views.rest import rest
from wof.flask.views.wsdl import wsdl


#TODO: Error handlers (404, etc.)
def create_app(wof_inst):
    app = Flask(__name__)
    app.config.from_object(config.Config)

    app.wof_inst = wof_inst
    app.register_module(rest)
    app.register_module(wsdl)

    return app
