import ConfigParser
import wof

_network = 'NETWORK'
_vocabulary = 'VOCABULARY'
_menu_group_name = 'MENU_GROUP_NAME'
_service_wsdl = 'SERVICE_WSDL'

_dao = None

_mappings = None



def config_from_file(file_name):
    config = ConfigParser.RawConfigParser()
    config.read(file_name)
    
    wof._network = config.get('WOF', 'Network')
    wof._vocabulary = config.get('WOF', 'Vocabulary')
    wof._menu_group_name = config.get('WOF', 'Menu_Group_Name')
    wof._service_wsdl = config.get('WOF', 'Service_WSDL')

