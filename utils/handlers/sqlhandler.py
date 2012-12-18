#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import logging

from sqlalchemy import Column, create_engine
from sqlalchemy.types import DateTime, Integer, String
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

__all__ = ['SQLHandler']

class Log(Base):
    __tablename__ = 'restlos_logs'
    id = Column(Integer, primary_key=True)
    logger = Column(String(128))
    level = Column(String(128))
    trace = Column(String(1024))
    msg = Column(String(1024))
    created_at = Column(DateTime, default=func.now())

    def __init__(self, logger=None, level=None, trace=None, msg=None):
        self.logger = logger
        self.level = level
        self.trace = trace
        self.msg = msg

    def __unicode__(self):
        return self.__repr__()

    def __repr__(self):
        return "<Log: %s - %s>" % (self.created_at.strftime('%m/%d/%Y-%H:%M:%S'), self.msg[:50])

class SQLHandler(logging.Handler):
    def __init__(self, dsn, audit=False):
        logging.Handler.__init__(self)
        self.dsn = dsn
        self.audit = audit
        self._sql_init()
        self._create()

    def _sql_init(self):
        self.engine = create_engine(self.dsn)
        self.session_maker = sessionmaker(bind=self.engine)
        self.session = None

    def _create(self):
        Base.metadata.create_all(self.engine) 

    def emit(self, record):
        if self.session is None:
            self.session = self.session_maker()

        if not self.audit or record.message.startswith('[audit]'):
            log = Log(logger=record.name, level=record.levelname, trace=str(record.exc_info), msg=record.message)

            self.session.add(log)
            self.session.commit()

    def close(self):
        if self.session:
            self.session.close()
        logging.Handler.close(self)
