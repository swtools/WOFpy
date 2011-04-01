from wof import *
from wof.code import *
import OdmSqlAlchDao

wof.config_from_file('lbr_config.cfg')
wof._dao = OdmSqlAlchDao.Dao()

print wof._network
print wof._mappings


print wof.code.create_get_site_response('')