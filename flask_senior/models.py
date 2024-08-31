from flask_senior.init_db import Base, world_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.mysql import INTEGER

class Country(world_base):
    __tablename__ = 'Country'
    
    code = Column(String(5), primary_key=True)
    name = Column(String(50))
    continent = Column(String(50))
    region = Column(String(50))
    surfacearea = Column(Integer)
    indepyear = Column(Integer)
    population = Column(Integer)
    lifeexpectancy = Column(Integer)
    gnp = Column(Integer)
    gnpold = Column(Integer)
    localname = Column(String(100))
    governmentform = Column(String(100))
    headofstate = Column(String(100))
    capital = Column(Integer)
    
    cities = relationship('City', back_populates='countries')
    
    def __init__(self, code=None, name=None, continent=None, region=None, surfacearea=None):
        self.code = code
        self.name = name
        self.continent = continent
        self.region = region
        self.surfacearea = surfacearea
        
    def __repr__(self):
        return 'Country %s, %r, %r, %r, %r' % (self.code, self.name, self.continent, self.region, self.surfacearea)
    



class City(world_base):
    __tablename__ = 'City'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    countrycode = Column(String(5), ForeignKey('Country.code'))
    district = Column(String(50))
    population = Column(Integer)
    # countries를 통해서 Country (db)클래스와 연결
    countries = relationship('Country', back_populates='cities')
    
    
    def __init__(self, id=None, name=None, countrycode=None, district=None, population=None):
        self.id = id
        self.name = name
        self.countrycode = countrycode
        self.district = district
        self.population = population
        
    def __repr__(self):
        return 'City %s, %r, %r, %r, %r' % (self.id, self.name, self.countrycode, self.district, self.population)




class User(Base):
    __tablename__ = 'USER'
    
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    passwd = Column(String(256))
    nickname = Column(String(31))

    
    def __init__(self, id=None, email=None, passwd=None, nickname='게스트'):
        self.id = id
        self.email = email
        self.passwd = passwd  # bcrypt로 password hash
        self.nickname = nickname
        
    def __repr__(self):
        return 'USER %s, %r, %r' % (self.id, self.email, self.nickname)
    
    

class User_country(Base):
    __tablename__ = 'USER_COUNTRY'
    
    id = Column(INTEGER(unsigned=True), ForeignKey('USER.id'), primary_key=True)
    countrycode = Column(String(255), primary_key=True)
    country = Column(String(256))
    user = relationship('User', backref=backref('user_countries'))
    
    def __init__(self, countrycode=None, country=None):
        self.countrycode = countrycode
        self.country = country
        
    def __repr__(self):
        return 'USER %s, %r, %r' % (self.id, self.countrycode, self.country)
    
    
    
    
    
    
    
    