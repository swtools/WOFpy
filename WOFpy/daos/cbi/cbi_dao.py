import urllib2
import time

from lxml import etree
from StringIO import StringIO
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from daos.base_dao import BaseDao

import cbi_cache_models as cache
import cbi_models as model
import cbi_sos_client
import cbi_sos_parser

class CbiDao(BaseDao):
    
    def __init__(self, db_connection_string):
        self.engine = create_engine(db_connection_string, convert_unicode=True)
        self.db_session = scoped_session(sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine))
        cache.init_model(self.db_session)
        
        self.cbi_sos_client = cbi_sos_client.CbiSosClient(
            'http://lighthouse.tamucc.edu/sos')
    
    def get_all_sites(self):
        """
        Returns a list of all the Sites in the CBI site cache.
        """
        return cache.Site.query.all()

    def get_site_by_code(self, site_code):
        """
        Returns a single Site identified by its code.
        """        
        return cache.Site.query.filter(
            cache.Site.SiteCode==site_code).first()


    def get_sites_by_codes(self, site_codes_arr):
        """
        Returns a list of Sites identified by the given site code list.
        """
        return cache.Site.query.filter(
            cache.Site.SiteCode.in_(site_codes_arr)).all()

    def get_all_variables(self):
        """
        Returns a list of all Variables in the data source.
        """
        return cache.Variable.query.all()
        

    def get_variable_by_code(self, var_code):
        """
        Returns a single Variable identified by its code.
        """
        return cache.Variable.query.filter(
            cache.Variable.VariableCode == var_code).first()

    def get_variables_by_codes(self, var_codes_arr):
        """
        Returns a list of Variables identified by the given variable code list.
        """
        return cache.Variable.query.filter(
            cache.Variable.VariableCode.in_(var_codes_arr)).all()

    def get_series_by_sitecode(self, site_code):
        """
        Returns a list of SeriesCatalogs for the given site code.
        """
        seriesResultArr = cache.SeriesCatalog.query.filter(
            cache.SeriesCatalog.SiteCode==site_code).all()
        
        
        for sr in seriesResultArr:
            if sr.IsCurrent: #TODO: Get current time in GMT
                et = time.gmtime(time.time())
                sr.EndDateTimeUTC = time.strftime("%Y-%m-%dT%H:%M:%SZ", et)
                
            #TODO: Source
        
        return seriesResultArr
        
    def get_series_by_sitecode_and_varcode(self, site_code, var_code):
        """
        Returns a list of SeriesCatalogs for the given site code and variable
        code combination.
        """
        #TODO: I think I can get all this information from the Capabilities doc
        pass

    def get_datavalues(self, site_code, var_code, begin_date_time=None,
                       end_date_time=None):
        """
        Returns a list of DataValues for the given site code and variable code,
        filtered by the optional begin and end datetimes.
        """
        
        #TODO: if begin and end date time are not specified, then need to
        #check series catalog to get full time extent and use those values
        #in the getobservation request.  The expected behavior of WOF:GetValues
        #is to return all data values for the full period of record, but
        #the GetObservation method only returns the last 10 or something.
        
        #Call GetObservation
        response = self.cbi_sos_client.get_observation(site_code, var_code,
                                            begin_date_time, end_date_time)
        
        if not response:
            return None
        
        tree = etree.parse(StringIO(response.read()))
        
        datavalue_list = \
            cbi_sos_parser.parse_datavalues_from_get_observation(tree,
                                                                site_code,
                                                                var_code)
    
        return datavalue_list
        
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
