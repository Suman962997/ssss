from pydantic import BaseModel
from typing import Any
from sqlalchemy import Column,Integer,String,Text,Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime


Base=declarative_base()
    

# Registry model to store table creation order
class TableRegistry(Base):
    __tablename__ = "table_registry"
    id = Column(Integer, primary_key=True, index=True)
    industry=Column(String(50))    
    table_name = Column(String(100), unique=True, index=True)
    category=Column(String(50))    
    riskscore=Column(Integer)    
    risklevel=Column(String(50))    
    compliance=Column(String(50))  
    status=Column(Boolean, default=True)
    section=Column(String(50))
    date=Column(String(50))    
    created_at = Column(DateTime, default=datetime.utcnow)

def create_pdf_model(table_name: str):
    class_attrs = {
        "__tablename__": table_name,
        "id": Column(Integer, primary_key=True, index=True),
        "section": Column(String(50)),
        "category": Column(String(50)),
        "question": Column(Text),
        "answer": Column(Text),
        "created_at": Column(DateTime, default=datetime.utcnow),
        "__table_args__": {'extend_existing': True},
    }
    return type("REPORTTABLE", (Base,), class_attrs)

