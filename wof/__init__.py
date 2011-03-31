from flask import Flask
from flaskext.sqlalchemy import SQLAlchemy
import wof.config

app = Flask(__name__)
app.config.from_object(wof.config.Config) #default config loading

NSDEF = 'xmlns:gml="http://www.opengis.net/gml" xmlns:xlink="http://www.w3.org/1999/xlink" \
        xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" \
        xmlns:wtr="http://www.cuahsi.org/waterML/" xmlns="http://www.cuahsi.org/waterML/1.0/"'

import wof.views