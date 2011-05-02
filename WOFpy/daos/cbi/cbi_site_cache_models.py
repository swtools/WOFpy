
from sqlalchemy import (Column, Integer, String, ForeignKey, Float, DateTime,
                        Boolean)

from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

import wof.base_models as wof_base

Base = declarative_base()


def init_model(db_session):
    Base.query = db_session.query_property()


class Site(Base, wof_base.BaseSite):
    __tablename__ = 'Sites'
    
    SiteID = Column(Integer, primary_key = True)
    SiteCode = Column(String)
    SiteName = Column(String)
    Latitude = Column(Float)
    Longitude = Column(Float)
    LatLongDatumID = Column(Integer,
                        ForeignKey('SpatialReferences.SpatialReferenceId')) #FK to SpatialReferences
    Elevation_m = Column(Float)
    VerticalDatum = Column(String)
    LocalX = Column(Float)
    LocalY = Column(Float)
    LocalProjectionID = Column(Integer,
                        ForeignKey('SpatialReferences.SpatialReferenceId')) #FK to SpatialReferences
    PosAccuracy_m = Column(Float)
    State = Column(String)
    County = Column(String)
    Comments = Column(String)
    
    LatLongDatum = relationship("SpatialReference",
                                    primaryjoin='Site.LatLongDatumID==\
                                        SpatialReference.SpatialReferenceId')
    
    LocalProjection = relationship("SpatialReference",
                                    primaryjoin='Site.LocalProjectionID==\
                                        SpatialReference.SpatialReferenceId')
      
    def __repr__(self):
        return "<Site('%s','%s', ['%s' '%s'])>" % (self.SiteCode,
                                                   self.SiteName,
                                                   str(self.Latitude),
                                                   str(self.Longitude))