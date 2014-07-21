__author__ = 'daniel'

from sqlalchemy import Integer, Column, String
from sqlalchemy.orm import  relationship
from lib.base import Base


class Racer(Base):
    __tablename__ = "racers"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    hostname = Column(String(50))
    location = Column(String(50))
    trials = relationship("Trial", primaryjoin="Racer.id==Trial.racer_id")
