from pydantic import BaseModel
from typing import Any
from sqlalchemy import Column,Integer,String,Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime


Base=declarative_base()

class supply_chain_management(Base):
    __tablename__="SSSS"
    id =Column(Integer,primary_key=True,index=True)
    category=Column(String(70))
    section=Column(String(50))
    question=Column(String(300))
    answer=Column(String(300))
    
    


# Registry model to store table creation order
class TableRegistry(Base):
    __tablename__ = "table_registry"
    id = Column(Integer, primary_key=True, index=True)
    section=Column(String(50))
    principle=Column(String(50))
    table_name = Column(String(100), unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

def create_pdf_model(table_name: str):
    class_attrs = {
        "__tablename__": table_name,
        "id": Column(Integer, primary_key=True, index=True),
        "section": Column(String(50)),
        "title": Column(String(255)),
        "partRoman":Column(String(255)),
        "categoryNo": Column(String(50)),
        "subtitle": Column(String(255)),
        "question_no": Column(String(50)),
        "question": Column(Text),
        "answer": Column(Text),
        "created_at": Column(DateTime, default=datetime.utcnow),
        "__table_args__": {'extend_existing': True},
    }
    return type("PDFTable", (Base,), class_attrs)

