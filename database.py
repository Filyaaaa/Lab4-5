from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

base = declarative_base()

SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://user1:user1@db:3306/lab2py'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
