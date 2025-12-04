from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Project(Base):
    "Represents a aid system project"
    __tablename__ = 'projects'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    budget = Column(Float, nullable=False)
    status = Column(String, default="active")  
    
    transactions = relationship('Transaction', back_populates='project', cascade='all, delete-orphan')
    fraud_flags = relationship('FraudFlag', back_populates='project', cascade='all, delete-orphan')
    
    def total_spent(self):
        "Calculate total amount spent on this project"
        return sum(t.amount for t in self.transactions)
    
    def remaining_budget(self):
        "Calculate remaining budget"
        return self.budget - self.total_spent()
    
    def __repr__(self):
        return f"<Project(id={self.id}, name='{self.name}', budget={self.budget})>"


class Transaction(Base):
    "Represents a financial transaction for a project"
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(String, nullable=False)
    description = Column(String)
    
    project = relationship('Project', back_populates='transactions')
    
    def __repr__(self):
        return f"<Transaction(id={self.id}, amount={self.amount}, date='{self.date}')>"


class FraudFlag(Base):
    "Represents a detected fraud indicator"
    __tablename__ = 'fraud_flags'
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    flag_type = Column(String, nullable=False)  
    severity = Column(String, nullable=False)   
    message = Column(String, nullable=False)
    status = Column(String, default="open")    
    
    project = relationship('Project', back_populates='fraud_flags')
    
    def __repr__(self):
        return f"<FraudFlag(id={self.id}, type='{self.flag_type}', severity='{self.severity}')>"