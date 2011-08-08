import datetime
import ConfigParser

from sqlalchemy import create_engine, distinct, func
from sqlalchemy.orm import mapper, scoped_session, sessionmaker
from sqlalchemy.sql import and_
from dateutil.parser import parse

import sqlalch_swis_models as model

from wof.dao import BaseDao


class SwisDao(BaseDao):
    contact_info = {
        'name': 'NAME',
        'phone': 'PHONE',
        'email': 'EMAIL',
        'organization': 'ORGANIZATION',
        'link': 'LINK',
        'description': 'DESCRIPTION',
        'address': 'ADDRESS',
        'city': 'CITY',
        'state': 'STATE',
        'zipcode': 'ZIP'
        }

    def __init__(self, config_file_path, database_uri=None):
        self.engine = create_engine(database_uri, convert_unicode=True)
        #TODO: Use pool_size for non-sqlite database connection
        self.db_session = scoped_session(sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine))
        model.init_model(self.db_session)
        config = ConfigParser.RawConfigParser()
        config.read(config_file_path)
        if config.has_section('Contact'):
            self.contact_info = {
                'name': config.get('Contact', 'Name'),
                'phone': config.get('Contact', 'Phone'),
                'email': config.get('Contact', 'Email'),
                'organization': config.get('Contact', 'Organization'),
                'link': config.get('Contact', 'Link'),
                'description': config.get('Contact', 'Description'),
                'address': config.get('Contact', 'Address'),
                'city': config.get('Contact', 'City'),
                'state': config.get('Contact', 'State'),
                'zipcode': config.get('Contact', 'ZipCode')
                }

    def __del__(self):
        self.db_session.close()

    def get_all_sites(self):
        return model.Site.query.all()

    def get_site_by_code(self, site_code):
        return model.Site.query.filter(
            model.Site.SiteCode == site_code).first()

    def get_sites_by_codes(self, site_codes_arr):
        return model.Site.query.filter(
            model.Site.SiteCode.in_(site_codes_arr)).all()

    def get_all_variables(self):
        return model.Variable.query.all()

    def get_variable_by_code(self, var_code):
        return model.Variable.query.filter(
            model.Variable.VariableCode == var_code).first()

    def get_variables_by_codes(self, var_codes_arr):
        return model.Variable.query.filter(model.Variable.VariableCode.in_(
            var_codes_arr)).all()

    def get_series_by_sitecode(self, site_code):
        siteResult = model.Site.query.filter(
            model.Site.SiteCode == site_code).one()

        if siteResult:
            resultList = self.db_session.query(
                model.DataValue.VariableID.label('VariableID'),
                func.count(model.DataValue.DataValue).label('ValueCount'),
                func.min(model.DataValue.DateTimeUTC).label(
                    'BeginDateTimeUTC'),
                func.max(model.DataValue.DateTimeUTC).label('EndDateTimeUTC')
            ).group_by(
                model.DataValue.VariableID).filter(
                    model.DataValue.SiteID == siteResult.SiteID
                ).order_by(model.DataValue.VariableID).all()
            varIDArr = [r.VariableID for r in resultList]
            varResultArr = model.Variable.query.filter(
                model.Variable.VariableID.in_(varIDArr)).order_by(
                    model.Variable.VariableID).all()
            seriesCatArr = []
            for i in range(len(resultList)):
                seriesCat = model.Series(
                        siteResult, varResultArr[i],
                        resultList[i].ValueCount,
                        resultList[i].BeginDateTimeUTC,
                        resultList[i].EndDateTimeUTC,
                        self.get_source_by_id()
                    )

                seriesCatArr.append(seriesCat)
            return seriesCatArr
        return None

    def get_series_by_sitecode_and_varcode(self, site_code, var_code):
        siteResult = model.Site.query.filter(
            model.Site.SiteCode == site_code).one()
        varResult = model.Variable.query.filter(
            model.Variable.VariableCode == var_code).one()

        res = self.db_session.query(
                func.count(model.DataValue.DataValue).label('ValueCount'),
                func.min(model.DataValue.DateTimeUTC).label(
                    'BeginDateTimeUTC'),
                func.max(model.DataValue.DateTimeUTC).label('EndDateTimeUTC'),
            ).filter(
                and_(model.DataValue.SiteID == siteResult.SiteID,
                     model.DataValue.VariableID == varResult.VariableID)).one()

        seriesCat = model.Series(
            siteResult, varResult, res.ValueCount, res.BeginDateTimeUTC,
            res.EndDateTimeUTC, self.get_source_by_id())

        return [seriesCat]

    def get_datavalues(self, site_code, var_code, begin_date_time=None,
                       end_date_time=None):
        #first find the site and variable
        siteResult = self.get_site_by_code(site_code)
        varResult = self.get_variable_by_code(var_code)
        valueResultArr = None
        if siteResult and varResult:
            if (not begin_date_time or not end_date_time):
                valueResultArr = model.DataValue.query.filter(
                    and_(model.DataValue.SiteID == siteResult.SiteID,
                         model.DataValue.VariableID == varResult.VariableID)
                    ).order_by(model.DataValue.DateTimeUTC).all()
            else:
                begin_date_time = parse(begin_date_time)
                end_date_time = parse(end_date_time)
                valueResultArr = model.DataValue.query.filter(
                    and_(model.DataValue.SiteID == siteResult.SiteID,
                         model.DataValue.VariableID == varResult.VariableID,
                         #SWIS doesn't have localdatetime, so using UTC
                         model.DataValue.DateTimeUTC >= begin_date_time,
                         model.DataValue.DateTimeUTC <= end_date_time)
                    ).order_by(model.DataValue.DateTimeUTC).all()

        return valueResultArr

    def get_method_by_id(self, methodID):
        return model.Method.query.filter(
            model.Method.MethodID == methodID).first()

    def get_methods_by_ids(self, method_id_arr):
        return model.Method.query.filter(
            model.Method.MethodID.in_(method_id_arr)).all()

    def get_source_by_id(self, source_id=1):
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
        #There is only ever one Source for SWIS: TWDB
        return [self.get_source_by_id()]

    def get_qualifier_by_id(self, qualifier_id):
        return model.Qualifier()

    def get_qualifiers_by_ids(self, qualifier_id_arr):
        return [model.Qualifier()]

    def get_qualcontrollvl_by_id(self, qual_control_lvl_id):
        return model.QualityControlLevel()

    def get_qualcontrollvls_by_ids(self, qual_control_lvl_id_arr):
        return [model.QualityControlLevel()]

    def get_offsettype_by_id(self, offset_type_id):
        #TODO
        return None

    def get_offsettypes_by_ids(self, offset_type_id_arr):
        #TODO
        return None
