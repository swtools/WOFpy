import ConfigParser
import wof


network = 'NETWORK'
vocabulary = 'VOCABULARY'
menu_group_name = 'MENU_GROUP_NAME'
service_wsdl = 'SERVICE_WSDL'

dao = None
mappings = None

def config_from_file(file_name):
    config = ConfigParser.RawConfigParser()
    config.read(file_name)
    
    wof.network = config.get('WOF', 'Network')
    wof.vocabulary = config.get('WOF', 'Vocabulary')
    wof.menu_group_name = config.get('WOF', 'Menu_Group_Name')
    wof.service_wsdl = config.get('WOF', 'Service_WSDL')

