import ConfigParser
import wof

network = 'NETWORK'
vocabulary = 'VOCABULARY'
menu_group_name = 'MENU_GROUP_NAME'
service_wsdl = 'SERVICE_WSDL'
contact_info = None
dao = None

def config_from_file(file_name):
    config = ConfigParser.RawConfigParser()
    config.read(file_name)
    
    wof.network = config.get('WOF', 'Network')
    wof.vocabulary = config.get('WOF', 'Vocabulary')
    wof.menu_group_name = config.get('WOF', 'Menu_Group_Name')
    wof.service_wsdl = config.get('WOF', 'Service_WSDL')

    if config.has_section('Contact'):
        wof.contact_info = dict()
        wof.contact_info['name'] = config.get('Contact', 'Name')
        wof.contact_info['phone'] = config.get('Contact', 'Phone')
        wof.contact_info['email'] = config.get('Contact', 'Email')
        wof.contact_info['organization'] = config.get('Contact', 'Organization')
        wof.contact_info['link'] = config.get('Contact', 'Link')
        wof.contact_info['description'] = config.get('Contact', 'Description')
        wof.contact_info['address'] = config.get('Contact', 'Address')
        wof.contact_info['city'] = config.get('Contact', 'City')
        wof.contact_info['state'] = config.get('Contact', 'State')
        wof.contact_info['zipcode'] = config.get('Contact', 'ZipCode')
        
