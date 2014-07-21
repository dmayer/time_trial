__author__ = 'daniel'

from sqlalchemy import Integer, Column, String
from sqlalchemy.orm import relationship
from lib.base import Base


class Experiment(Base):
    __tablename__ = "experiments"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    trials = relationship("Trial",
                          primaryjoin="Trial.experiment_id==Experiment.id")
