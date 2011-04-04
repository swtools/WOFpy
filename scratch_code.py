from wof import *
from wof.code import *
import OdmSqlAlchDao

wof.config_from_file('lbr_config.cfg')
wof.dao = OdmSqlAlchDao.OdmSqlAlchDao()

print wof.network
print wof.mappings


print wof.code.create_get_site_response('')