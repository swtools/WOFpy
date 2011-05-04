import urllib2


from StringIO import StringIO
from lxml import etree
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from daos.base_dao import BaseDao

import wof
import cbi_site_cache_models as site_cache_model
import cbi_models as model
import cbi_sos_client


namespaces = {
        'xsi': "http://www.w3.org/2001/XMLSchema-instance",
        'xlink': "http://www.w3.org/1999/xlink",
        'om': "http://www.opengis.net/om/1.0",
        'gml': "http://www.opengis.net/gml",
        'swe': "http://www.opengis.net/swe/1.0.1"
    }

def nspath(path, ns):
    return '{%s}%s' % (ns, path) 

class CbiDao(BaseDao):
    
    def __init__(self, db_connection_string):
        self.engine = create_engine(db_connection_string, convert_unicode=True)
        self.db_session = scoped_session(sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine))
        site_cache_model.init_model(self.db_session)
        
        self.cbi_sos_client = cbi_sos_client.CbiSosClient(
            'http://lighthouse.tamucc.edu/sos')
    
    def get_all_sites(self):
        """
        Returns a list of all the Sites in the CBI site cache.
        """
        return site_cache_model.Site.query.all()

    def get_site_by_code(self, site_code):
        """
        Returns a single Site identified by its code.
        """        
        return site_cache_model.Site.query.filter(
            site_cache_model.Site.SiteCode==site_code).first()


    def get_sites_by_codes(self, site_codes_arr):
        """
        Returns a list of Sites identified by the given site code list.
        """
        return site_cache_model.Site.query.filter(
            site_cache_model.Site.SiteCode.in_(site_codes_arr)).all()

    def get_all_variables(self):
        """
        Returns a list of all Variables in the data source.
        """
        
        #TODO: Not sure where to get all the variable info
        pass

    def get_variable_by_code(self, var_code):
        """
        Returns a single Variable identified by its code.
        """
        #TODO: Not sure where to get all the variable info
        pass

    def get_variables_by_codes(self, var_codes_arr):
        """
        Returns a list of Variables identified by the given variable code list.
        """
        #TODO: Not sure where to get all the variable info
        pass

    def get_series_by_sitecode(self, site_code):
        """
        Returns a list of SeriesCatalogs for the given site code.
        """
        pass

    def get_series_by_sitecode_and_varcode(self, site_code, var_code):
        """
        Returns a list of SeriesCatalogs for the given site code and variable
        code combination.
        """
        pass

    def get_datavalues(self, site_code, var_code, begin_date_time=None,
                       end_date_time=None):
        """
        Returns a list of DataValues for the given site code and variable code,
        filtered by the optional begin and end datetimes.
        """
        
        #Call GetObservation
        response = self.cbi_sos_client.get_observation(site_code, var_code,
                                            begin_date_time, end_date_time)
        
        tree = etree.parse(StringIO(response.read()))
        
        #The data values from the response xml are organized into 'blocks'
        # with each block containing several fields (PlatformName, time,
        # latitude, longitude, depth, observedProperty1).
        # These fields are described in swe:field elements
        
        fields = tree.findall('.//'+nspath('field', namespaces['swe']))
        field_names = [f.attrib['name'] for f in fields]
        
        #Now that we have the fields, we can parse the values appropriately
        
        text_block = tree.find('.//'+nspath('encoding', namespaces['swe'])
                        +'/'+nspath('TextBlock', namespaces['swe']))
        block_sep = text_block.attrib['blockSeparator']
        token_sep = text_block.attrib['tokenSeparator']
        
        values_blocks = tree.findtext('.//'+nspath('values',
                                                   namespaces['swe']))
   
        datavalue_list = []
        val_lines_arr = [block.split(token_sep)
                         for block in values_blocks.split(block_sep)]
        
        for val_line in val_lines_arr:
            field_val_dict = dict(zip(field_names, val_line))
            
            dv = model.DataValue(field_val_dict['observedProperty1'], #TODO: Is it always observedProperty1 ?
                                 field_val_dict['time'],
                                 field_val_dict['depth'],
                                 site_code,
                                 var_code) #TODO: SITEID and VARID (instead of code)
            
            datavalue_list.append(dv)
    
        return datavalue_list
        
        #Parse swe:values from the response
        
        
    def get_method_by_id(self, method_id):
        """
        Returns a single Method identified by the given id.
        """
        pass

    def get_methods_by_ids(self, method_id_arr):
        """
        Returns a list of Methods identified by the given id list.
        """
        pass

    def get_source_by_id(self, source_id):
        """
        Returns a single Source identified by the given id.
        """
        pass

    def get_sources_by_ids(self, source_id_arr):
        """
        Returns a list of Sources identified by the given id list.
        """
        pass

    def get_qualifier_by_id(self, qualifier_id):
        """
        Returns a single Qualifier identified by the given id.
        """
        pass

    def get_qualifiers_by_ids(self, qualifier_id_arr):
        """
        Returns a list of Qualifiers identified by the given id list.
        """
        pass

    def get_qualcontrollvl_by_id(self, qual_control_lvl_id):
        """
        Returns a single QualityControlLevel identified by the given id.
        """
        pass

    def get_qualcontrollvls_by_ids(self, qual_control_lvl_id_arr):
        """
        Returns a list of QualityControlLevels identified by the given id list.
        """
        pass

    def get_offsettype_by_id(self, offset_type_id):
        """
        Returns a single OffsetType identified by the given id.
        """
        pass

    def get_offsettypes_by_ids(self, offset_type_id_arr):
        """
        Returns a list of OffsetTypes identified by the given id list.
        """
        pass
