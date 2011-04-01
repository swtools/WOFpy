import ConfigParser
import wof

wof._network = 'NETWORK'
wof._vocabulary = 'VOCABULARY'
wof._menu_group_name = 'MENU_GROUP_NAME'
wof._service_wsdl = 'SERVICE_WSDL'

wof._mappings = None


def config_from_file(file_name):
    config = ConfigParser.RawConfigParser()
    config.read(file_name)
    
    wof._network = config.get('WOF', 'Network')
    wof._vocabulary = config.get('WOF', 'Vocabulary')
    wof._menu_group_name = config.get('WOF', 'Menu_Group_Name')
    wof._service_wsdl = config.get('WOF', 'Service_WSDL')

