
import wof


wof.config_from_file('lbr_config.cfg')
wof._mappings = 'sqlalch_odm_mappings'

print wof._network
print wof._mappings


import wof.code
print wof.code.create_get_site_response('')