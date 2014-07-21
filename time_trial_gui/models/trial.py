__author__ = 'daniel'

from sqlalchemy import Integer, Column, String, ForeignKey, Text, DateTime,Boolean
from sqlalchemy.orm import  relationship
from lib.base import Base
from models.racer import Racer

from PyQt4 import QtCore


class Trial(Base):
    __tablename__ = "trials"

    discriminator = Column('type', String(50))
    __mapper_args__ = {'polymorphic_on': discriminator}

    id = Column(Integer, primary_key=True)

    name = Column(String(50))
    description = Column(String(1000))

    core_id = Column(Integer)
    real_time = Column(Boolean)
    reps = Column(Integer)

    status = Column(String(50))
    job = Column(Text)
    result = Column(Text)
    start_date = Column(DateTime)
    end_date = Column(DateTime)

    racer_id = Column(Integer, ForeignKey('racers.id'))
    racer = relationship("Racer", primaryjoin="Trial.racer_id==Racer.id")

    experiment_id = Column(Integer, ForeignKey('experiments.id'))
    experiment = relationship("Experiment", primaryjoin="Trial.experiment_id==Experiment.id")

class EchoTrial(Trial):
    __tablename__ = 'echo_trials'
    __mapper_args__ = {'polymorphic_identity': 'Echo Trial'}
    id = Column(Integer, ForeignKey('trials.id'), primary_key=True)
    host = Column(String(100))
    port = Column(Integer)
    delay = Column(Integer)

    def duplicate(self):
        x = EchoTrial()

        #common
        x.name = self.name
        x.description = self.description
        x.core_id = self.core_id
        x.real_time = self.real_time
        x.reps = self.reps
        x.racer = self.racer
        x.experiment = self.experiment


        x.host = self.host
        x.port = self.port
        x.delay = self.delay

        return x


class HTTPTrial(Trial):
    __tablename__ = 'http_trials'
    __mapper_args__ = {'polymorphic_identity': 'HTTP Trial'}
    id = Column(Integer, ForeignKey('trials.id'), primary_key=True)
    request_url = Column(String(500))
    request = Column(String(50000))

    def duplicate(self):
        x = HTTPTrial()

        #common
        x.name = self.name
        x.description = self.description
        x.core_id = self.core_id
        x.real_time = self.real_time
        x.reps = self.reps
        x.racer = self.racer
        x.experiment = self.experiment

        x.request_url = self.request_url
        x.request = self.request

        return x







