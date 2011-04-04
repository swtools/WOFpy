
from sqlalch_odm_mappings import *

class OdmSqlAlchDao(object):

    def __init__(self):
        #TODO: anything?
        pass
    
    def Get_All_Sites(self):
        return Site.query.all()
    
    def Get_Site_By_Code(self, siteCode):
        return Site.query.filter(Site.SiteCode == siteCode).first()
    
    def Get_Sites_By_Codes(self, siteCodesArr):
        return Site.query.filter(Site.SiteCode.in_(siteCodesArr)).all()
    
    def Get_All_Variables(self):
        return Variable.query.all()
    
    def Get_Variable_By_Code(self, varCode):
        Variable.query.filter(Variable.VariableCode == varCode).first()
    
    def Get_Variables_By_Codes(self, varCodesArr):
        return Variable.query.filter(Variable.VariableCode.in_(varCodesArr)).all()
    
    def Get_Series_By_SiteCode(self, siteCode):
        return SeriesCatalog.query.filter(SeriesCatalog.SiteCode == siteCode).all()
    
    def Get_Series_By_SiteCode_And_VarCode(self, siteCode, varCode):
        return SeriesCatalog.query.filter(and_(
            SeriesCatalog.SiteCode == siteCode,
            SeriesCatalog.VariableCode == varCode)).all()
        
    def Get_DataValues(self, siteCode, varCode, startDateTime=None,
                       endDateTime=None):
        #first find the site and variable
        siteResult = Get_Site_By_Code(siteCode)
        varResult = Get_Variable_By_Code(varCode)
        
        valueResultArr = None
        
        if (startDateTime == None or endDateTime == None):
            valueResultArr = DataValue.query.filter(
                and_(DataValue.SiteID == siteResult.SiteID,
                     DataValue.VariableID == varResult.VariableID))\
                .order_by(DataValue.LocalDateTime).all()
        else:
            valueResultArr = DataValue.query.filter(
                and_(DataValue.SiteID == siteResult.SiteID,
                     DataValue.VariableID == varResult.VariableID,
                     DataValue.LocalDateTime >= startDateTime,
                     DataValue.LocalDateTime <= endDateTime))\
                .order_by(DataValue.LocalDateTime).all()
            
        return valueResultArr
    
    def Get_Method_By_ID(self, methodID):
        return Method.query.filter(Method.MethodID == methodID).first()
        
    def Get_Methods_By_IDs(self, methodIdArr):
        return Method.query.filter(Method.MethodID.in_(methodIdArr)).all()
        
    def Get_Source_By_ID(self, sourceID):
        return Source.query.filter(Source.SourceID == sourceID).first()
        
    def Get_Sources_By_IDs(self, sourceIdArr):
        return Source.query.filter(Source.SourceID.in_(sourceIdArr)).all()
    
    def Get_Qualifier_By_ID(self, qualID):
        return Qualifier.query.filter(Qualifier.QualifierID == qualID).first()
    
    def Get_Qualifiers_By_IDs(self, qualIdArr):
        return Qualifier.query.filter(Qualifier.QualifierID.in_(qualIdArr)).all()
    
    def Get_QualControlLvl_By_ID(self, qualControlLvlID):
        return QualityControlLevel.query.filter(
                QualityControlLevel.QualityControlLevelID ==
                qualControlLvlID).first()
    
    def Get_QualControlLvls_By_IDs(self, qualControlLvlIdArr):
        return QualityControlLevel.query.filter(
                QualityControlLevel.QualityControlLevelID.in_(qualControlLvlIdArr)).all()
    
    def Get_OffsetType_By_ID(self, offsetTypeID):
        return OffsetType.query.filter(OffsetType.OffsetTypeID ==
                                       offsetTypeID).first()
    
    def Get_OffsetTypes_By_IDs(self, offsetTypeIdArr):
        return OffsetType.query.filter(OffsetType.OffsetTypeID.in_(offsetTypeIdArr)).all()