from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, DateTime, Table
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.database import Base

class ApiInfo(Base):
    __tablename__ = "api_info"
    
    api_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    method = Column(String, nullable=False)
    endpoint = Column(String, nullable=False)
    description = Column(Text)
    
    # 관계 설정
    test_cases = relationship("ApiTestCase", back_populates="api_info", cascade="all, delete-orphan")

class ApiTestCase(Base):
    __tablename__ = "api_test_case"
    
    test_case_id = Column(Integer, primary_key=True, autoincrement=True)
    api_id = Column(Integer, ForeignKey("api_info.api_id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    
    # 관계 설정
    api_info = relationship("ApiInfo", back_populates="test_cases")
    test_data = relationship("ApiTestData", back_populates="test_case", cascade="all, delete-orphan")
    test_runs = relationship("ApiTestRun", back_populates="test_case", cascade="all, delete-orphan")
    collections = relationship("CollectionTestCase", back_populates="test_case", cascade="all, delete-orphan")

class ApiTestData(Base):
    __tablename__ = "api_test_data"
    
    test_data_id = Column(Integer, primary_key=True, autoincrement=True)
    test_case_id = Column(Integer, ForeignKey("api_test_case.test_case_id"), nullable=False)
    request_data = Column(Text, nullable=False)
    expected_response = Column(Text, nullable=False)
    
    # 관계 설정
    test_case = relationship("ApiTestCase", back_populates="test_data")

class User(Base):
    __tablename__ = "user"
    
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    role = Column(String)
    
    # 관계 설정
    collections = relationship("ApiTestCollection", back_populates="user", cascade="all, delete-orphan")
    test_runs = relationship("ApiTestRun", back_populates="user", cascade="all, delete-orphan")

class ApiTestCollection(Base):
    __tablename__ = "api_test_collection"
    
    collection_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    
    # 관계 설정
    user = relationship("User", back_populates="collections")
    test_cases = relationship("CollectionTestCase", back_populates="collection", cascade="all, delete-orphan")

class CollectionTestCase(Base):
    __tablename__ = "collection_test_case"
    
    collection_id = Column(Integer, ForeignKey("api_test_collection.collection_id"), primary_key=True)
    test_case_id = Column(Integer, ForeignKey("api_test_case.test_case_id"), primary_key=True)
    
    # 관계 설정
    collection = relationship("ApiTestCollection", back_populates="test_cases")
    test_case = relationship("ApiTestCase", back_populates="collections")

class ApiTestRun(Base):
    __tablename__ = "api_test_run"
    
    test_run_id = Column(Integer, primary_key=True, autoincrement=True)
    test_case_id = Column(Integer, ForeignKey("api_test_case.test_case_id"), nullable=False)
    executed_at = Column(DateTime, server_default=func.now())
    status = Column(String, nullable=False)
    actual_response = Column(Text)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    
    # 관계 설정
    test_case = relationship("ApiTestCase", back_populates="test_runs")
    user = relationship("User", back_populates="test_runs")
    results = relationship("ApiTestResult", back_populates="test_run", cascade="all, delete-orphan")

class ApiTestResult(Base):
    __tablename__ = "api_test_result"
    
    result_id = Column(Integer, primary_key=True, autoincrement=True)
    test_run_id = Column(Integer, ForeignKey("api_test_run.test_run_id"), nullable=False)
    assertion = Column(Text, nullable=False)
    passed = Column(Boolean, nullable=False)
    message = Column(Text)
    
    # 관계 설정
    test_run = relationship("ApiTestRun", back_populates="results")