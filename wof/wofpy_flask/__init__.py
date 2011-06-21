from flask import Flask, render_template

import config

#TODO: Error handlers (404, etc.)

def create_app(wof_inst):
    app = Flask(__name__)
    app.config.from_object(config.Config)

    app.wof_inst = wof_inst

    from wofpy_flask.views.rest import rest
    app.register_module(rest)
    
    from wofpy_flask.views.wsdl import wsdl
    app.register_module(wsdl)
    
    return app
