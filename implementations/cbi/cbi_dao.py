import urllib2
import time
import ConfigParser

from lxml import etree
from StringIO import StringIO
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql import and_

from wof.dao import BaseDao

import cbi_cache_models as cache
import cbi_models as model
import cbi_sos_client
import cbi_sos_parser


class CbiDao(BaseDao):
    def __init__(self, config_file_path, database_uri=None):
        config = ConfigParser.RawConfigParser()
        config.read(config_file_path)
        if not database_uri:
            database_uri = config.get('Database', 'URI')

        self.engine = create_engine(database_uri, convert_unicode=True)
        #TODO: use pool_size for non-sqlite database
        self.db_session = scoped_session(sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine))
        cache.init_model(self.db_session)

        self.cbi_sos_client = cbi_sos_client.CbiSosClient(
            'http://lighthouse.tamucc.edu/sos')

        if config.has_section('Contact'):
            self.contact_info = dict(
                name=config.get('Contact', 'Name'),
                phone=config.get('Contact', 'Phone'),
                email=config.get('Contact', 'Email'),
                organization=config.get('Contact', 'Organization'),
                link=config.get('Contact', 'Link'),
                description=config.get('Contact', 'Description'),
                address=config.get('Contact', 'Address'),
                city=config.get('Contact', 'City'),
                state=config.get('Contact', 'State'),
                zipcode=config.get('Contact', 'ZipCode')
            )

    def __del__(self):
        self.db_session.close()

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
            cache.Site.SiteCode == site_code).first()

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
            cache.SeriesCatalog.SiteCode == site_code).all()
        for sr in seriesResultArr:
            #TODO: Get current time in GMT
            if sr.IsCurrent:
                et = time.gmtime(time.time())
                sr.EndDateTimeUTC = time.strftime("%Y-%m-%d %H:%M:%S", et)
            sr.Source = self.get_source_by_id()
        return seriesResultArr

    def get_series_by_sitecode_and_varcode(self, site_code, var_code):
        """
        Returns a list of SeriesCatalogs for the given site code and variable
        code combination.
        """

        seriesResultArr = cache.SeriesCatalog.query.filter(and_(
             cache.SeriesCatalog.SiteCode == site_code,
             cache.SeriesCatalog.VariableCode == var_code)).all()
        for sr in seriesResultArr:
            if sr.IsCurrent:
                #Get current time in GMT
                et = time.gmtime(time.time())
                sr.EndDateTimeUTC = time.strftime("%Y-%m-%d %H:%M:%S", et)
            sr.Source = self.get_source_by_id()
        return seriesResultArr

    def get_datavalues(self, site_code, var_code, begin_date_time=None,
                       end_date_time=None):
        """
        Returns a list of DataValues for the given site code and variable code,
        filtered by the optional begin and end datetimes.
        """
        #if begin and end date time are not specified, then need to
        #check series catalog to get full time extent and use those values
        #in the getobservation request.  The expected behavior of WOF:GetValues
        #is to return all data values for the full period of record, but
        #the CBI SOS:GetObservation method only returns the last 9.
        if not begin_date_time or not end_date_time:
            #need to find the start and end dates from the cache
            series_cat = self.get_series_by_sitecode_and_varcode(
                site_code, var_code)[0]
            if not begin_date_time:
                begin_date_time = series_cat.BeginDateTimeUTC
                begin_date_time = str(begin_date_time).replace(' ', 'T')
            if not end_date_time:
                end_date_time = series_cat.EndDateTimeUTC
                end_date_time = str(end_date_time).replace(' ', 'T')
        if not begin_date_time.find(':'):
            begin_date_time = begin_date_time + 'T00:00:00'
        if not end_date_time.find(':'):
            end_date_time = end_date_time + 'T23:59:59'
        #Call GetObservation
        response = self.cbi_sos_client.get_observation(
            site_code, var_code,
            begin_date_time,
            end_date_time)
        if not response:
            return None
        tree = etree.parse(StringIO(response.read()))
        datavalue_list = \
            cbi_sos_parser.parse_datavalues_from_get_observation(
            tree, site_code, var_code)
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

    def get_source_by_id(self, source_id=1):
        """
        Returns a single Source identified by the given id.
        """
        source = model.Source()

        source.ContactName = self.contact_info['name']
        source.Phone = self.contact_info['phone']
        source.Email = self.contact_info['email']
        source.Organization = self.contact_info['organization']
        source.SourceLink = self.contact_info['link']
        source.SourceDescription = self.contact_info['description']
        source.Address = self.contact_info['address']
        source.City = self.contact_info['city']
        source.State = self.contact_info['state']
        source.ZipCode = self.contact_info['zipcode']

        return source

    def get_sources_by_ids(self, source_id_arr):
        """
        Returns a list of Sources identified by the given id list.
        """
        return [self.get_source_by_id()]

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
