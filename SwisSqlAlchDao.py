import datetime

from sqlalchemy import distinct, func
from sqlalchemy.sql import and_

import sqlalch_swis_mappings as map

#TODO
class SwisSqlAlchDao(object):
    
    def get_all_sites(self):
        return map.Site.query.all()
    
    def get_site_by_code(self, site_code):
        return map.Site.query.filter(map.Site.SiteCode == site_code).first()
    
    def get_sites_by_codes(self, site_codes_arr):
        return map.Site.query.filter(map.Site.SiteCode.in_(site_codes_arr)).all()
    
    def get_all_variables(self):
        return map.Variable.query.all()
    
    def get_variable_by_code(self, var_code):
        return map.Variable.query.filter(
            map.Variable.VariableCode == var_code).first()
    
    def get_variables_by_codes(self, var_codes_arr):
        return map.Variable.query.filter(map.Variable.VariableCode.in_(
            var_codes_arr)).all()
    
    def get_series_by_sitecode(self, site_code):
        
        siteResult = map.Site.query.filter(map.Site.SiteCode==site_code).one()
        
        if siteResult:
            
            resultList = map.db_session.query(
                map.DataValue.VariableID.label('VariableID'),
                func.count(map.DataValue.DataValue).label('ValueCount'),
                func.min(map.DataValue.DateTimeUTC).label('BeginDateTimeUTC'),
                func.max(map.DataValue.DateTimeUTC).label('EndDateTimeUTC'),
                map.DataValue.UTCOffset.label('UTCOffset')
            ).group_by(
                map.DataValue.VariableID).filter(
                    map.DataValue.SiteID==siteResult.SiteID
                ).order_by(map.DataValue.VariableID).all()
            
            varIDArr = [r.VariableID for r in resultList]

            varResultArr = map.Variable.query.filter(
                map.Variable.VariableID.in_(varIDArr)).order_by(
                    map.Variable.VariableID).all()

            seriesCatArr = []
            for i in range(len(resultList)):

                begin_date = None
                end_date = None

                if resultList[i].UTCOffset:
                    offset_delta = datetime.timedelta(
                        hours=resultList[i].UTCOffset)
                    
                    begin_date = resultList[i].BeginDateTimeUTC + offset_delta
                    end_date = resultList[i].EndDateTimeUTC + offset_delta
                
                seriesCat = map.SeriesCatalog(
                    siteResult, varResultArr[i],
                    resultList[i].ValueCount,
                    resultList[i].BeginDateTimeUTC,
                    resultList[i].EndDateTimeUTC,
                    begin_date, end_date)
                               
                seriesCatArr.append(seriesCat)
            return seriesCatArr
            
        return None
    
    def get_series_by_sitecode_and_varcode(self, site_code, var_code):
        siteResult = map.Site.query.filter(map.Site.SiteCode==site_code).one()
        varResult = map.Variable.query.filter(
            map.Variable.VariableCode==var_code).one()
                
        res = map.db_session.query(
                func.count(map.DataValue.DataValue).label('ValueCount'),
                func.min(map.DataValue.DateTimeUTC).label('BeginDateTimeUTC'),
                func.max(map.DataValue.DateTimeUTC).label('EndDateTimeUTC'),
                map.DataValue.UTCOffset.label('UTCOffset')
            ).filter(and_(map.DataValue.SiteID==siteResult.SiteID,
                        map.DataValue.VariableID==varResult.VariableID)).one()
            
        begin_date = None
        end_date = None
                
        if res.UTCOffset:
            offset_delta = datetime.timedelta(hours=res.UTCOffset)
            
            begin_date = res.BeginDateTimeUTC + offset_delta
            end_date = res.EndDateTimeUTC + offset_delta

        seriesCat = map.SeriesCatalog(
            siteResult, varResult, res.ValueCount, res.BeginDateTimeUTC,
            res.EndDateTimeUTC, begin_date, end_date)
       
        return [seriesCat]
         
    #TODO
    def get_datavalues(self, site_code, var_code, begin_date_time=None,
                       end_date_time=None):
        
        #first find the site and variable
        siteResult = self.get_site_by_code(site_code)
        varResult = self.get_variable_by_code(var_code)
        
        valueResultArr = None
        
        #TODO: Should we be using DateTimeUTC instead of LocalDateTime?
        # All the other WOF services uses local
        
        if (not begin_date_time or not end_date_time):
            valueResultArr = map.DataValue.query.filter(
                and_(map.DataValue.SiteID == siteResult.SiteID,
                     map.DataValue.VariableID == varResult.VariableID)
                ).order_by(map.DataValue.DateTimeUTC).all()
        else:
            valueResultArr = map.DataValue.query.filter(
                and_(map.DataValue.SiteID == siteResult.SiteID,
                     map.DataValue.VariableID == varResult.VariableID,
                     map.DataValue.DateTimeUTC >= begin_date_time, #TODO: SWIS doesn't have localdatetime
                     map.DataValue.DateTimeUTC <= end_date_time) #TODO: SWIS doesn't have localdatetime
                ).order_by(map.DataValue.DateTimeUTC).all()
            
        return valueResultArr
    
    def get_method_by_id(self, methodID):
        return map.Method.query.filter(map.Method.MethodID == methodID).first()
        
    def get_methods_by_ids(self, method_id_arr):
        return map.Method.query.filter(
            map.Method.MethodID.in_(method_id_arr)).all()
        
    def get_source_by_id(self, source_id):
        return map.Source.query.filter(map.Source.SourceID == source_id).first()
        
    def get_sources_by_ids(self, source_id_arr):
        return map.Source.query.filter(
            map.Source.SourceID.in_(source_id_arr)).all()
    
    def get_qualifier_by_id(self, qualifier_id):
        return map.Qualifier()
    
    def get_qualifiers_by_ids(self, qualifier_id_arr):
        return [map.Qualifier()]
    
    def get_qualcontrollvl_by_id(self, qual_control_lvl_id):
        return map.QualityControlLevel()
    
    def get_qualcontrollvls_by_ids(self, qual_control_lvl_id_arr):
        return [map.QualityControlLevel()]
    
    def get_offsettype_by_id(self, offset_type_id):
        #TODO
        return None
    
    def get_offsettypes_by_ids(self, offset_type_id_arr):
        #TODO
        return None
        