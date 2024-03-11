from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

database = 'mysql+pymysql://root:@localhost:3306/lab2py'

engine = create_engine(database)

session_local = sessionmaker(autocommit = False, autoflush=False, bind=engine)
base = declarative_base()