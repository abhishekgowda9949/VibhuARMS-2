# database.py
from datetime import date
from sqlalchemy import TEXT, VARCHAR, create_engine, Column, String, Integer, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configure the database connection
DATABASE_URI = 'mysql://root:''@localhost/vibhuarms-2'
engine = create_engine(DATABASE_URI)

# Create a sessionmaker to create sessions
DBSession = sessionmaker(bind=engine)

# Create a base class
Base = declarative_base()

# Define a model for the Admin table
class IQAC_C0(Base):
    __tablename__ = 'iqac_co'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    emailid = Column(String(255), unique=True)
    password = Column(String(255))

class ATTRIBUTE_CO(Base):
    __tablename__ = 'attributer_co'
    id = Column(Integer, primary_key=True, autoincrement=True)
    attributerid = Column(VARCHAR(255), primary_key=True)
    name = Column(String(255))
    emailid = Column(String(255), unique=True)
    password = Column(String(255))

class ATTRIBUTE_ALLOT(Base):
    __tablename__ = 'attributer_allot'
    id = Column(Integer, primary_key=True, autoincrement=True)
    attributerid = Column(VARCHAR(255), primary_key=True)
    name = Column(String(255))
    emailid = Column(String(255), unique=True)
    attributeid = Column(VARCHAR(255))

class Employee(Base):
    __tablename__ = 'employees'    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    empid = Column(String(10), unique=True)
    department = Column(String(100))
    email = Column(String(100), unique=True)
    mobile = Column(String(20))
    password = Column(String(50))

# Create the table if it doesn't exist
Base.metadata.create_all(engine)