# backend/models.py

from sqlalchemy import Column, Integer, String, Float, Boolean, ARRAY, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class TitleBasics(Base):
    __tablename__ = "title_basics"
    tconst = Column(String, primary_key=True, index=True)
    titleType = Column(String)
    primaryTitle = Column(String, index=True)
    originalTitle = Column(String, index=True)
    isAdult = Column(Boolean)
    startYear = Column(Integer, index=True)
    endYear = Column(Integer)
    runtimeMinutes = Column(Integer)
    genres = Column(ARRAY(String), index=True)

    # This creates a back-reference from TitleAkas to this model
    akas = relationship("TitleAkas", back_populates="title")
    principals = relationship("TitlePrincipals", back_populates="title")

class TitleAkas(Base):
    __tablename__ = "title_akas"
    titleId = Column(String, ForeignKey('title_basics.tconst'), primary_key=True)
    ordering = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    region = Column(String)
    language = Column(String)
    types = Column(ARRAY(String))
    attributes = Column(ARRAY(String))
    isOriginalTitle = Column(Boolean)
    
    # This relationship links an AKA back to its main title in TitleBasics
    title = relationship("TitleBasics", back_populates="akas")

class NameBasics(Base):
    __tablename__ = "name_basics"
    nconst = Column(String, primary_key=True, index=True)
    primaryName = Column(String, index=True)
    birthYear = Column(Integer)
    deathYear = Column(Integer)
    primaryProfession = Column(ARRAY(String))
    knownForTitles = Column(ARRAY(String))

    principals = relationship("TitlePrincipals", back_populates="person")

class TitlePrincipals(Base):
    __tablename__ = "title_principals"
    tconst = Column(String, ForeignKey('title_basics.tconst'), primary_key=True)
    ordering = Column(Integer, primary_key=True)
    nconst = Column(String, ForeignKey('name_basics.nconst'), primary_key=True)
    category = Column(String, index=True)
    job = Column(String)
    characters = Column(String)

    title = relationship("TitleBasics", back_populates="principals")
    person = relationship("NameBasics", back_populates="principals")