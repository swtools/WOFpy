from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy import Boolean

from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

#TODO: How can this be put in init method of the DAO?
import private_config
engine = create_engine(private_config.swis_connection_string,
                       convert_unicode=True)

db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

class Site(Base):
    __tablename__ = 'site'
    
    SiteID = Column('id', Integer, primary_key=True)
    SiteCode = Column('site_code', String)
    SiteName = Column('name', String)
    #Latitude
    #Longitude
    #Elevation_m
    #VerticalDatum
    #LocalX
    #LocalY
    #PosAccuracy_m
    #State
    #County
    Comments = Column('description', String)
    
    #SiteID = Column(Integer, primary_key = True)
    #SiteCode = Column(String)
    #SiteName = Column(String)
    #Latitude = Column(Float)
    #Longitude = Column(Float)
    #LatLongDatumID = Column(Integer, ForeignKey('SpatialReferences.SpatialReferenceId')) #FK to SpatialReferences
    #Elevation_m = Column(Float)
    #VerticalDatum = Column(String)
    #LocalX = Column(Float)
    #LocalY = Column(Float)
    #LocalProjectionID = Column(Integer, ForeignKey('SpatialReferences.SpatialReferenceId')) #FK to SpatialReferences
    #PosAccuracy_m = Column(Float)
    #State = Column(String)
    #County = Column(String)
    #Comments = Column(String)
    
    #LatLongDatum = relationship("SpatialReference",
    #                                    primaryjoin='Site.LatLongDatumID==SpatialReference.SpatialReferenceId')
    
    #LocalProjection = relationship("SpatialReference",
    #                                    primaryjoin='Site.LocalProjectionID==SpatialReference.SpatialReferenceId')
    
    
    
    
    
    
    
    
    
    