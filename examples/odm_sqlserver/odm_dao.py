from datetime import datetime
from sqlalchemy import create_engine, distinct, func
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql import and_

from dateutil.parser import parse

from wof.dao import BaseDao
import sqlalch_odm_models as model


class OdmDao(BaseDao):

    def __init__(self, db_connection_string):
        self.engine = create_engine(db_connection_string, convert_unicode=True,
            pool_size=100)
        # Default application pool size is 5. Use 100 to improve performance.
        self.db_session = scoped_session(sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine))
        model.init_model(self.db_session)

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
        return model.Series.query.filter(
            model.Series.SiteCode == site_code).all()

    def get_series_by_sitecode_and_varcode(self, site_code, var_code):
        return model.Series.query.filter(and_(
            model.Series.SiteCode == site_code,
            model.Series.VariableCode == var_code)).all()

    def parse_dates(self, begin_date_time, end_date_time):
        """Returns a list with parsed datetimes.

        Required Arguments:
            begin_date_time (begin datetime as text)
            end_date_time (end datetime as text)
        Remarks:
            The returned list has three items:
                begin datetime as datetime.datetime object
                end datetime as datetime.datetime object
                bool that is True if times are UTC, False otherwise
            The datetimes are None if the input strings were None.
        
        """
        
        # Convert input strings to datetime objects
        try:
            if begin_date_time:
                b = parse(begin_date_time)
            else:
                b = None
        except:
            raise ValueError('invalid start date: ' + str(begin_date_time))
        try:
            if end_date_time:
                e = parse(end_date_time)
            else:
                e = None
        except:
            raise ValueError('invalid end date: ' + str(end_date_time))

        # If we know time zone for both, convert to UTC time
        utc_time_zone = parse('2001-01-01T00Z').tzinfo # dummy time to get tz
        if b and b.tzinfo and e and e.tzinfo:
            b = b.astimezone(utc_time_zone)
            e = e.astimezone(utc_time_zone)
            using_utc = True
        # If we know time zone for one, assume other is also UTC time
        elif b and b.tzinfo:
            b = b.astimezone(utc_time_zone)
            if e:
                e = e.replace(tzinfo=utc_time_zone)
            using_utc = True
        elif e and e.tzinfo:
            e = e.astimezone(utc_time_zone)
            if b:
                b = b.replace(tzinfo=utc_time_zone)
            using_utc = True
        # Otherwise, assume local time
        else:
            using_utc = False

        return [b, e, using_utc]
    
    def get_datavalues(self, site_code, var_code, begin_date_time=None,
                       end_date_time=None):

        #first find the site and variable
        siteResult = self.get_site_by_code(site_code)
        varResult = self.get_variable_by_code(var_code)

        valueResultArr = None
        
        if siteResult and varResult:
            parse_result = self.parse_dates(begin_date_time, end_date_time)
            begin_datetime = parse_result[0]
            end_datetime = parse_result[1]
            using_utc = parse_result[2]

            if using_utc:
                if begin_datetime and end_datetime:
                    valueResultArr = model.DataValue.query.filter(
                        and_(model.DataValue.SiteID == siteResult.SiteID,
                             model.DataValue.VariableID == varResult.VariableID,
                             model.DataValue.DateTimeUTC >= begin_datetime,
                             model.DataValue.DateTimeUTC <= end_datetime)
                        ).order_by(model.DataValue.DateTimeUTC).all()
                elif begin_datetime:
                    valueResultArr = model.DataValue.query.filter(
                        and_(model.DataValue.SiteID == siteResult.SiteID,
                             model.DataValue.VariableID == varResult.VariableID,
                             model.DataValue.DateTimeUTC >= begin_datetime)
                        ).order_by(model.DataValue.DateTimeUTC).all()
                elif end_datetime:
                    valueResultArr = model.DataValue.query.filter(
                        and_(model.DataValue.SiteID == siteResult.SiteID,
                             model.DataValue.VariableID == varResult.VariableID,
                             model.DataValue.DateTimeUTC <= end_datetime)
                        ).order_by(model.DataValue.DateTimeUTC).all()
                else:
                    valueResultArr = model.DataValue.query.filter(
                        and_(model.DataValue.SiteID == siteResult.SiteID,
                             model.DataValue.VariableID == varResult.VariableID)
                        ).order_by(model.DataValue.DateTimeUTC).all()
            else:
                if begin_datetime and end_datetime:
                    valueResultArr = model.DataValue.query.filter(
                        and_(model.DataValue.SiteID == siteResult.SiteID,
                             model.DataValue.VariableID == varResult.VariableID,
                             model.DataValue.LocalDateTime >= begin_datetime,
                             model.DataValue.LocalDateTime <= end_datetime)
                        ).order_by(model.DataValue.DateTimeUTC).all()
                elif begin_datetime:
                    valueResultArr = model.DataValue.query.filter(
                        and_(model.DataValue.SiteID == siteResult.SiteID,
                             model.DataValue.VariableID == varResult.VariableID,
                             model.DataValue.LocalDateTime >= begin_datetime)
                        ).order_by(model.DataValue.DateTimeUTC).all()
                elif end_datetime:
                    valueResultArr = model.DataValue.query.filter(
                        and_(model.DataValue.SiteID == siteResult.SiteID,
                             model.DataValue.VariableID == varResult.VariableID,
                             model.DataValue.LocalDateTime <= end_datetime)
                        ).order_by(model.DataValue.DateTimeUTC).all()
                else:
                    valueResultArr = model.DataValue.query.filter(
                        and_(model.DataValue.SiteID == siteResult.SiteID,
                             model.DataValue.VariableID == varResult.VariableID)
                        ).order_by(model.DataValue.DateTimeUTC).all()

        return valueResultArr

    def get_method_by_id(self, method_id):
        return model.Method.query.filter(
            model.Method.MethodID == method_id).first()

    def get_methods_by_ids(self, method_id_arr):
        return model.Method.query.filter(
            model.Method.MethodID.in_(method_id_arr)).all()

    def get_source_by_id(self, source_id):
        return model.Source.query.filter(
            model.Source.SourceID == source_id).first()

    def get_sources_by_ids(self, source_id_arr):
        return model.Source.query.filter(
            model.Source.SourceID.in_(source_id_arr)).all()

    def get_qualifier_by_id(self, qualifier_id):
        return model.Qualifier.query.filter(
            model.Qualifier.QualifierID == qualifier_id).first()

    def get_qualifiers_by_ids(self, qualifier_id_arr):
        return model.Qualifier.query.filter(model.Qualifier.QualifierID.in_(
            qualifier_id_arr)).all()

    def get_qualcontrollvl_by_id(self, qual_control_lvl_id):
        return model.QualityControlLevel.query.filter(
                model.QualityControlLevel.QualityControlLevelID ==
                qual_control_lvl_id).first()

    def get_qualcontrollvls_by_ids(self, qual_control_lvl_id_arr):
        return model.QualityControlLevel.query.filter(
               model.QualityControlLevel.QualityControlLevelID.in_(
                    qual_control_lvl_id_arr)).all()

    def get_offsettype_by_id(self, offset_type_id):
        return model.OffsetType.query.filter(
            model.OffsetType.OffsetTypeID == offset_type_id).first()

    def get_offsettypes_by_ids(self, offset_type_id_arr):
        return model.OffsetType.query.filter(model.OffsetType.OffsetTypeID.in_(
            offset_type_id_arr)).all()
