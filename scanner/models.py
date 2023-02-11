from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.sql import func

from scanner.database import Base
from scanner.settings import DB_STRING_LENGTH


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(DB_STRING_LENGTH), unique=True, nullable=False)
    password = Column(String(DB_STRING_LENGTH), nullable=False)
    email = Column(String(DB_STRING_LENGTH), unique=True, nullable=False)
    date_create = Column(DateTime(timezone=True), server_default=func.now())


class VulnerabilityType(Base):
    __tablename__ = 'vulnerability_types'

    id = Column(Integer, primary_key=True)
    name = Column(String(DB_STRING_LENGTH), unique=True, nullable=False)
    description = Column(Text, nullable=False)


class Scan(Base):
    __tablename__ = 'scans'

    id = Column(Integer, primary_key=True)
    url = Column(String(DB_STRING_LENGTH), nullable=False)
    date_start = Column(DateTime(timezone=True), server_default=func.now())
    date_end = Column(DateTime(timezone=True))
    risk_level = Column(String(DB_STRING_LENGTH), nullable=False)
    status = Column(String(DB_STRING_LENGTH))
    result = Column(Text)
    user = Column(ForeignKey('users.id'), nullable=False)
    vulnerability_type = Column(ForeignKey('vulnerability_types.id'), nullable=False)


class Script(Base):
    __tablename__ = 'scripts'

    id = Column(Integer, primary_key=True)
    body = Column(Text, nullable=False)
