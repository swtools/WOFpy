

from soaplib.core.service import soap
from soaplib.core.service import DefinitionBase
from soaplib.core.model.primitive import String, Integer, DateTime
from soaplib.core.model.clazz import Array, ClassModel, XMLAttribute



class DocumentMetadataType(ClassModel):
    id = XMLAttribute('xsi:string')
    generationDate = DateTime
    generationSystem = String
    
class Metadata(ClassModel):
    DocumentMetadata = DocumentMetadataType

class WaterCollection(ClassModel):
    metadata = Metadata
    #observationMember

class WaterMonitoringObservation(ClassModel):
    pass

class identifier(ClassModel):
    #__namespace__
    #__type_name__
    pass