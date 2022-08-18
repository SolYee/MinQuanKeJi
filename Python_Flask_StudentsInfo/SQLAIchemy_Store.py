#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2022/8/16 9:13
# @Author:yishouquan
# @File:SQLAIchemy_Store.py
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from datetime import datetime
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "user_account"
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    phone = Column(String)
    studentsinfo = relationship(
        "StudentsInfo", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, phone={self.phone!r})"


class StudentsInfo(Base):
    __tablename__ = "StudentsInfo"
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    teacher = Column(String(128))
    class_type = Column(String(128))
    tuition = Column(String(128))
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, onupdate=datetime.now, default=datetime.now)
    user_id = Column(Integer, ForeignKey("user_account.id"), nullable=False)
    user = relationship("User", back_populates="studentsinfo")

    def __repr__(self):
        return f"StudentsInfo(id={self.id!r}, email_address={self.email_address!r}," \
               f"teacher={self.teacher!r}, class_type={self.class_type!r}," \
               f"tuition={self.tuition!r}, update_time={self.update_time!r}," \
               f"create_time={self.id!r}, user_id={self.user_id!r})"


from sqlalchemy import create_engine

engine = create_engine("sqlite://", echo=True, future=True)
Base.metadata.create_all(engine)
