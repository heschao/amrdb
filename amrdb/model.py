import os

from sqlalchemy import Column, DateTime, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Message(Base):
    __tablename__ = 'message'
    timestamp = Column(DateTime, primary_key=True)
    device_id = Column(Integer)
    device_type = Column(Integer)
    consumption = Column(Integer)

    def __init__(self, timestamp, device_id, device_type, consumption ):
        self.timestamp = timestamp
        self.device_id = device_id
        self.device_type = device_type
        self.consumption = consumption

    def __repr__(self):
        return 'Message(timestamp={},device_id={},device_type={},consumption={})'.format(
            self.timestamp, self.device_id, self.device_type, self.consumption
        )


def get_session(connection_string=os.getenv('CONNECTION_STRING')):
    if not connection_string:
        raise Exception('empty connection string')
    engine = create_engine(connection_string)
    Session = sessionmaker(bind=engine)
    return Session()