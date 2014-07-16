import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#Database environment variable configure on heroku
db_path = os.environ.get('DATABASE_URL')

engine = create_engine(
        db_path,
        isolation_level="READ UNCOMMITTED" )

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():    
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import device    
    Base.metadata.create_all(bind=engine)    
