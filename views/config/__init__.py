
class Config(object):
	DEBUG = False
	TESTING = False
	NETWORK = 'NETWORK'
	VOCABULARY = 'VOCABULARY'
	NSDEF = 'xmlns:gml="http://www.opengis.net/gml" \
	 xmlns:xlink="http://www.w3.org/1999/xlink" \
	 xmlns:xsd="http://www.w3.org/2001/XMLSchema" \
	 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" \
	 xmlns:wtr="http://www.cuahsi.org/waterML/" \
	 xmlns="http://www.cuahsi.org/waterML/1.0/"'
	MENU_GROUP_NAME = ''
	SERVICE_WSDL = ''
	SQLALCHEMY_DATABASE_URI = ''

class TWDBSondesConfig(Config):
	NETWORK = 'TWDB_Sondes'
	VOCABULARY = 'TWDB'
	MENU_GROUP_NAME = 'TWDB Sondes Observations'
	
class LBRConfig(Config):
	NETWORK = 'LBR'
	VOCABULARY = 'LBR'
	MENU_GROUP_NAME = 'Little Bear River Observations'

class TCEQConfig(Config):
	NETWORK = 'TCEQ'
	VOCABULARY = 'TCEQ'
	MENU_GROUP_NAME = 'TCEQ TRACS Observations'

class ProductionConfig(TWDBSondesConfig):
    SERVICE_WSDL = 'http://crwr-hydroportal.austin.utexas.edu/WOFPy/soap/TWDB_Sondes/WOFService.wsdl'