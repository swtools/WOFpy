
class Config(object):
	DEBUG = False
	TESTING = False
	NETWORK = 'NETWORK'
	VOCABULARY = 'VOCABULARY'
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