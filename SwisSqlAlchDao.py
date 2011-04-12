from sqlalchemy.sql import and_

import sqlalch_swis_mappings as map

#TODO
class SwisSqlAlchDao(object):
    
    def get_all_sites(self):
        return map.Site.query.all()
    
    def get_site_by_code(self, siteCode):
        return map.Site.query.filter(map.Site.SiteCode == siteCode).first()
    
    def get_sites_by_codes(self, siteCodesArr):
        return map.Site.query.filter(map.Site.SiteCode.in_(siteCodesArr)).all()
    
    def get_all_variables(self):
        return map.Variable.query.all()
    
    def get_variable_by_code(self, varCode):
        return map.Variable.query.filter(
            map.Variable.VariableCode == varCode).first()
    
    def get_variables_by_codes(self, varCodesArr):
        return map.Variable.query.filter(map.Variable.VariableCode.in_(
            varCodesArr)).all()
    
    def get_series_by_sitecode(self, siteCode):
        return map.SeriesCatalog.query.filter(
            map.SeriesCatalog.SiteCode == siteCode).all()
    
    def get_series_by_sitecode_and_varcode(self, siteCode, varCode):
                
        return map.SeriesCatalog.query.filter(and_(
            map.SeriesCatalog.SiteCode == siteCode,
            map.SeriesCatalog.VariableCode == varCode)).all()
        
    def get_datavalues(self, siteCode, varCode, startDateTime=None,
                       endDateTime=None):
        
        #first find the site and variable
        siteResult = self.get_site_by_code(siteCode)
        varResult = self.get_variable_by_code(varCode)
        
        valueResultArr = None
        
        if (not startDateTime or not endDateTime):
            valueResultArr = map.DataValue.query.filter(
                and_(map.DataValue.SiteID == siteResult.SiteID,
                     map.DataValue.VariableID == varResult.VariableID)
                ).order_by(map.DataValue.LocalDateTime).all()
        else:
            valueResultArr = map.DataValue.query.filter(
                and_(map.DataValue.SiteID == siteResult.SiteID,
                     map.DataValue.VariableID == varResult.VariableID,
                     map.DataValue.LocalDateTime >= startDateTime, #TODO: SWIS doesn't have localdatetime
                     map.DataValue.LocalDateTime <= endDateTime) #TODO: SWIS doesn't have localdatetime
                ).order_by(map.DataValue.LocalDateTime).all()
            
        return valueResultArr
    
    def get_method_by_id(self, methodID):
        return map.Method.query.filter(map.Method.MethodID == methodID).first()
        
    def get_methods_by_ids(self, methodIdArr):
        return map.Method.query.filter(
            map.Method.MethodID.in_(methodIdArr)).all()
        
    def get_source_by_id(self, sourceID):
        return map.Source.query.filter(map.Source.SourceID == sourceID).first()
        
    def get_sources_by_ids(self, sourceIdArr):
        return map.Source.query.filter(
            map.Source.SourceID.in_(sourceIdArr)).all()
    
    def get_qualifier_by_id(self, qualID):
        return map.Qualifier.query.filter(
            map.Qualifier.QualifierID == qualID).first()
    
    def get_qualifiers_by_ids(self, qualIdArr):
        return map.Qualifier.query.filter(
            map.Qualifier.QualifierID.in_(qualIdArr)).all()
    
    def get_qualcontrollvl_by_id(self, qualControlLvlID):
        return map.QualityControlLevel.query.filter(
                map.QualityControlLevel.QualityControlLevelID ==
                qualControlLvlID).first()
    
    def get_qualcontrollvls_by_ids(self, qualControlLvlIdArr):
        return map.QualityControlLevel.query.filter(
                map.QualityControlLevel.QualityControlLevelID.in_(
                    qualControlLvlIdArr)).all()
    
    def get_offsettype_by_id(self, offsetTypeID):
        return map.OffsetType.query.filter(
            map.OffsetType.OffsetTypeID == offsetTypeID).first()
    
    def get_offsettypes_by_ids(self, offsetTypeIdArr):
        return map.OffsetType.query.filter(map.OffsetType.OffsetTypeID.in_(
            offsetTypeIdArr)).all()
        

