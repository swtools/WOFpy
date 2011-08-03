import datetime
import ConfigParser

from sqlalchemy import create_engine, distinct, func
from sqlalchemy.orm import mapper, scoped_session, sessionmaker
from sqlalchemy.sql import and_
from dateutil.parser import parse

from wof.dao import BaseDao
import sqlalch_LCM_models as model
import wof.models as wof_base

class LCMDao(BaseDao):
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
    def __init__(self, db_connection_string, config_file_path):
        '''
        For SQLite connection - no need to specify for pool size in connection
        string, e.g.
        self.engine = create_engine(db_connection_string, convert_unicode=True)
        
        For non-SQLite connections (e.g. MSSQL) - indicate default pool_size of
        100, e.g.
        self.engine = create_engine(db_connection_string, convert_unicode=True,
         pool_size=100)
        '''
        
        self.engine = create_engine(db_connection_string, convert_unicode=True)
                
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

    '''
    The function, 'append_units', is added because WOFpy expects unit
    properties such as UnitsName, UnitsAbbreviation, etc to be stored as
    child objects under VariableUnits in the Variable class.
    Normally this kind of hierarchy is generated when a 'Units'-like table in
    the database is joined to a 'Variable'-like table using UnitsID as the Foreign Key.
    
    However, in the LCM database, both units information and variable
    information are lumped together within the 'variables' table.
    To generate the required hierarchy, the 'append units' function loops
    through each row in the variable table, creates an instance of VariableUnits,
    and fills in the child objects (UnitsID, UnitsName, UnitsAbbreviation,etc).
    with unit information from the variables table.
    '''
    def append_units(self,get_variables_response):
        r = get_variables_response
        for i in range(len(get_variables_response)):
            #Declare a new instance of BaseUnits for each VariableUnits object of
            #each item in get_all_variables response.
            #If you don't do this all items will end up referencing the same
            #memory location for VariableUnits.            
            r[i].VariableUnits = wof_base.BaseUnits()
            
            r[i].VariableUnits.UnitsID = r[i].VariableUnits_UnitsID
            r[i].VariableUnits.UnitsName = r[i].VariableUnits_UnitsName
            r[i].VariableUnits.UnitsAbbreviation = r[i].VariableUnits_UnitsAbbreviation    
        
        return r
    
    def get_all_variables(self):        
        r = model.Variable.query.all()               
        r = self.append_units(r)
        
        return r

    def get_variable_by_code(self, var_code):
        r = model.Variable.query.filter(
            model.Variable.VariableCode == var_code).first()
        r.VariableUnits.UnitsID = r.VariableUnits_UnitsID
        r.VariableUnits.UnitsName = r.VariableUnits_UnitsName
        r.VariableUnits.UnitsAbbreviation = r.VariableUnits_UnitsAbbreviation   
        return r

    def get_variables_by_codes(self, var_codes_arr):
        r = model.Variable.query.filter(model.Variable.VariableCode.in_(
            var_codes_arr)).all()
        r = self.append_units(r)        
        return r
    
    #ET: Experimental, not used.
    #def format_DateTimeUTC(self,DateString,TimeString):
    #    dformat = '%m/%d/%Y'
    #    tformat = '%H:%M'
    #    DateTimeUTC = [datetime.datetime.strptime(Item[0:-1], dformat) for Item in DateTimeUTC.DateString]        
    #    return DateTimeUTC
    
    def get_series_by_sitecode(self, site_code):
        siteResult = model.Site.query.filter(
            model.Site.SiteCode == site_code).one()        
        if siteResult:            
            resultList = self.db_session.query(                
                model.DataValue.VariableCode.label('VariableCode'),
                func.count(model.DataValue.DataValue).label('ValueCount'),
                func.min(model.DataValue.DateTimeUTC).label(
                    'BeginDateTimeUTC'),
                func.max(model.DataValue.DateTimeUTC).label('EndDateTimeUTC')              
            ).group_by(
                model.DataValue.VariableCode).filter(
                    model.DataValue.SiteCode == siteResult.SiteCode
                ).order_by(model.DataValue.VariableCode).all()           
            varCodeArr = [r.VariableCode for r in resultList]
            varResultArr = model.Variable.query.filter(               
                model.Variable.VariableCode.in_(varCodeArr)).order_by(                    
                    model.Variable.VariableCode).all()
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
                and_(model.DataValue.SiteCode == siteResult.SiteCode,                     
                     model.DataValue.VariableCode == varResult.VariableCode)).one()

        seriesCat = model.Series(
            siteResult, varResult, res.ValueCount, res.BeginDateTimeUTC,
            res.EndDateTimeUTC, self.get_source_by_id())

        return [seriesCat]

    def get_datavalues(self, site_code, var_code, begin_date_time=None,
                       end_date_time=None):
        #todo: convert inputs dates to UTC
        #first find the site and variable
        siteResult = self.get_site_by_code(site_code)
        varResult = self.get_variable_by_code(var_code)
        valueResultArr = None
        if siteResult and varResult:
            if (not begin_date_time or not end_date_time):
                valueResultArr = model.DataValue.query.filter(                    
                    and_(model.DataValue.SiteCode == site_code,
                        model.DataValue.VariableCode == var_code)
                    ).order_by(model.DataValue.DateTimeUTC).all()                
            else:
                begin_date_time = parse(begin_date_time)
                end_date_time = parse(end_date_time)
                valueResultArr = model.DataValue.query.filter(
                    and_(model.DataValue.SiteCode == site_code,
                         model.DataValue.VariableCode == var_code,
                         model.DataValue.DateTimeUTC >= begin_date_time,
                         model.DataValue.DateTimeUTC <= end_date_time)
                    ).order_by(model.DataValue.DateTimeUTC).all()
                
        for i in range(len(valueResultArr)):
            #Replace offset values of None with offset values = 0
            if not valueResultArr[i].OffsetValue:
                valueResultArr[i].OffsetValue = 0
            #Compute local datetime
            valueResultArr[i].LocalDateTime = valueResultArr[i].DateTimeUTC + \
                datetime.timedelta(hours=valueResultArr[i].UTCOffset)
            
            
            
        return valueResultArr
       
    def get_method_by_id(self, method_id):
        #return model.Method.query.filter(
        #    model.Method.MethodID == method_id).first()
        return model.DataValue.query.filter(
            model.DataValue.MethodID == method_id).first()

    def get_methods_by_ids(self, method_id_arr):
        #return model.Method.query.filter(
        #    model.Method.MethodID.in_(method_id_arr)).all()
        return model.DataValue.query.filter(
            model.DataValue.MethodID.in_(method_id_arr)).all()

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
        #There is only ever one source for LCM, which is LCM
        return [self.get_source_by_id()]

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
        r = wof_base.BaseOffsetType()
        r.OffsetTypeID = 1
        r.OffsetUnitsID = 6
        r.OffsetDescription = 'depth below water surface'

        #r.OffsetUnits = wof_base.BaseUnits()        
        r.OffsetUnits.UnitsID = 6
        r.OffsetUnits.UnitsName = 'meters'
        r.OffsetUnits.UnitsType = 'depth'
        r.OffsetUnits.UnitsAbbreviation = 'm'
        rarr = [r]
        return rarr
        #return model.OffsetType.query.filter(model.OffsetType.OffsetTypeID.in_(
        #    offset_type_id_arr)).all()
        
