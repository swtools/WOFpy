from sqlalchemy.sql import and_

from sqlalch_swis_mappings import *

#TODO
class SwisSqlAlchDao(object):
    
    def get_all_sites(self):
        return Site.query.all()
    
    def get_site_by_code(self, siteCode):
        return Site.query.filter(Site.SiteCode == siteCode).first()
    
    def get_sites_by_codes(self, siteCodesArr):
        return Site.query.filter(Site.SiteCode.in_(siteCodesArr)).all()
    
    def get_all_variables(self):
        return Variable.query.all()
    
    def get_variable_by_code(self, varCode):
        return Variable.query.filter(Variable.VariableCode == varCode).first()
    
    def get_variables_by_codes(self, varCodesArr):
        return Variable.query.filter(Variable.VariableCode.in_(
            varCodesArr)).all()
    
    def get_series_by_sitecode(self, siteCode):
        return SeriesCatalog.query.filter(
            SeriesCatalog.SiteCode == siteCode).all()
    
    def get_series_by_sitecode_and_varcode(self, siteCode, varCode):
        return SeriesCatalog.query.filter(and_(
            SeriesCatalog.SiteCode == siteCode,
            SeriesCatalog.VariableCode == varCode)).all()
        
    def get_datavalues(self, siteCode, varCode, startDateTime=None,
                       endDateTime=None):
        
        #first find the site and variable
        siteResult = self.get_site_by_code(siteCode)
        varResult = self.get_variable_by_code(varCode)
        
        valueResultArr = None
        
        #TODO: Something Wrong Here
        if (not startDateTime or not endDateTime):
            valueResultArr = DataValue.query.filter(
                and_(DataValue.SiteID == siteResult.SiteID,
                     DataValue.VariableID == varResult.VariableID)
                ).order_by(DataValue.LocalDateTime).all()
        else:
            valueResultArr = DataValue.query.filter(
                and_(DataValue.SiteID == siteResult.SiteID,
                     DataValue.VariableID == varResult.VariableID,
                     DataValue.LocalDateTime >= startDateTime, #TODO: SWIS doesn't have localdatetime
                     DataValue.LocalDateTime <= endDateTime) #TODO: SWIS doesn't have localdatetime
                ).order_by(DataValue.LocalDateTime).all()
            
        return valueResultArr
    
    def get_method_by_id(self, methodID):
        return Method.query.filter(Method.MethodID == methodID).first()
        
    def get_methods_by_ids(self, methodIdArr):
        return Method.query.filter(Method.MethodID.in_(methodIdArr)).all()
        
    def get_source_by_id(self, sourceID):
        return Source.query.filter(Source.SourceID == sourceID).first()
        
    def get_sources_by_ids(self, sourceIdArr):
        return Source.query.filter(Source.SourceID.in_(sourceIdArr)).all()
    
    def get_qualifier_by_id(self, qualID):
        return Qualifier.query.filter(Qualifier.QualifierID == qualID).first()
    
    def get_qualifiers_by_ids(self, qualIdArr):
        return Qualifier.query.filter(Qualifier.QualifierID.in_(
            qualIdArr)).all()
    
    def get_qualcontrollvl_by_id(self, qualControlLvlID):
        return QualityControlLevel.query.filter(
                QualityControlLevel.QualityControlLevelID ==
                qualControlLvlID).first()
    
    def get_qualcontrollvls_by_ids(self, qualControlLvlIdArr):
        return QualityControlLevel.query.filter(
                QualityControlLevel.QualityControlLevelID.in_(
                    qualControlLvlIdArr)).all()
    
    def get_offsettype_by_id(self, offsetTypeID):
        return OffsetType.query.filter(OffsetType.OffsetTypeID ==
                                       offsetTypeID).first()
    
    def get_offsettypes_by_ids(self, offsetTypeIdArr):
        return OffsetType.query.filter(OffsetType.OffsetTypeID.in_(
            offsetTypeIdArr)).all()
        

