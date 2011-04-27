import ConfigParser
import wof

network = 'NETWORK'
vocabulary = 'VOCABULARY'
menu_group_name = 'MENU_GROUP_NAME'
service_wsdl = 'SERVICE_WSDL'
timezone = None
timezone_abbr = None

contact_info = dict(
    name = 'NAME',
    phone = 'PHONE',
    email = 'EMAIL',
    organization = 'ORGANIZATION',
    link = 'LINK',
    description = 'DESCRIPTION',
    address = 'ADDRESS',
    city = 'CITY',
    state = 'STATE',
    zipcode = 'ZIP'
)

dao = None

def config_from_file(file_name):
    config = ConfigParser.RawConfigParser()
    config.read(file_name)
    
    wof.network = config.get('WOF', 'Network')
    wof.vocabulary = config.get('WOF', 'Vocabulary')
    wof.menu_group_name = config.get('WOF', 'Menu_Group_Name')
    wof.service_wsdl = config.get('WOF', 'Service_WSDL')
    wof.timezone = config.get('WOF', 'Timezone')
    wof.timezone_abbr = config.get('WOF', 'TimezoneAbbreviation')

    if config.has_section('Contact'):
        wof.contact_info = dict(
            name = config.get('Contact', 'Name'),
            phone = config.get('Contact', 'Phone'),
            email = config.get('Contact', 'Email'),
            organization = config.get('Contact', 'Organization'),
            link = config.get('Contact', 'Link'),
            description = config.get('Contact', 'Description'),
            address = config.get('Contact', 'Address'),
            city = config.get('Contact', 'City'),
            state = config.get('Contact', 'State'),
            zipcode = config.get('Contact', 'ZipCode')
        )
        
