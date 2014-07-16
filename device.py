from sqlalchemy.sql.functions import GenericFunction
from sqlalchemy.types import DateTime
from sqlalchemy import Column, Integer, String
from database import Base
from sqlalchemy.sql import func

class Device(Base):
    __tablename__ = 'device'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    registration = Column(String(512) )
    last_time = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def __init__(self, name=None, registration=None):
        self.name = name
        self.registration = registration

    #def __repr__(self):
    #    return '<Device %r>' % (self.name)

