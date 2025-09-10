import json
import pdfplumber
import docx
from fastapi import FastAPI, UploadFile, File, Form,Depends, HTTPException
from fastapi.responses import JSONResponse
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from database import create_engine,SessionLocal
from dotenv import load_dotenv
# from Extract import Biodiversity
import Extract
from sqlalchemy.orm import Session
from typing import Dict,Any,List,Optional
import questions
# import pdf
from models import supply_chain_management,create_pdf_model

load_dotenv()
API_KEY=os.getenv("API_KEY")

genai.configure(api_key=API_KEY )

app = FastAPI()
app = FastAPI(title="Document Extractor API" )
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://192.168.2.72:3000","http://localhost:3000",'*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Question(BaseModel):
    text: str
    choices: Optional[List[str]] = None
    isMandatory: bool




class CompanyOverview(BaseModel):
    key: str
    quesSection: str
    questionsAnswer: str
    percentComplete: str | Any
    question: List[Question]
      
class RequestBody(BaseModel):
    item: CompanyOverview
    activeCategory: str
    kratos:Dict
    report:str
    date:str



def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
    


def extract_text_fun(file):
    with pdfplumber.open(file) as pdf:
        return "\n".join([page.extract_text() for page in pdf.pages])
    
def chunk_text(text,max_tokens=1500):
    paragraphs=text.split("\n")
    chunks,current_chunk=[],""
    for para in paragraphs:
        if len(current_chunk)+len(para) < max_tokens:
            current_chunk +=para + "\n"
        else:
            chunks.append(current_chunk)
            current_chunk=para + "\n"
    if current_chunk:
        chunks.append(current_chunk)
        return chunks


def extract_json_from_text(text):
    brace_stack = []
    start_index = None
    for i, char in enumerate(text):
        if char == '{':
            if start_index is None:
                start_index = i
            brace_stack.append('{')
        elif char == '}':
            if brace_stack:
                brace_stack.pop()
                if not brace_stack:
                    json_str = text[start_index:i + 1]
                    try:
                        return json.loads(json_str)
                    except json.JSONDecodeError:
                        continue
    return None



def extract_fileds_with_gemini(text_chunk :str,finded_section :str) -> dict:

    model=genai.GenerativeModel("gemini-2.0-flash")
    prompt=f"""
You are an expert in information extraction. Extraxt the following details from the provided text and return them in valid JSON format with keys exactly as listed below. Only return the JSON — no extra commentary.

{finded_section}
TEXT:
{text_chunk}
""" 
    try:
        response=model.generate_content(prompt) 
        parsed=extract_json_from_text(response.text)
        return parsed if parsed else {}
    except ResourceExhausted:
        raise HTTPException(status_code=429,detail="Gemini API quota exceeded." )
    except Exception as e:
        raise HTTPException(status_code=500,details=str(e))


def merge_results(results):
    final = {}
    for result in results:
        for k, v in result.items():
            if k not in final or not final[k]:
                final[k] = v
    return final


def category_find_fun(category:str):
    catagories={
        "general":"General Information",
        "supplierbenchmark":"Supplier Benchmark",
        "supplier-strategy":"Supplier Strategy & SDG Roadmap",
        "performance":"Performance Reporting",
        "product-supply":"Product & Supply Chain Footprint",
        "governace":"Governace & Certificate",
        "management-system":"M,R & Management System",
        "emissions-waste":"Emissions , Waste & Biodiversity",
        "carbon":"Carbon Offerts",
        "financial-tracking":"Financial Tracking",

    }

    return catagories[category]


def sections_find_fun(section:str):
  sections={
  "Company Overview":Extract.Company_Overview,
  "Business Operations":Extract.Business_Operations,
  "Clients Partnerships":Extract.Clients_Partnership,
  "Technology Innovation":Extract.Technology_Innovation,
  "Risk and Business Continuity":Extract.Risk_and_Business_Continuity,
  "Company Growth":Extract.Company_Growth,
  "Workforce":Extract.Workforce,
  "ESG Policies Governance":Extract.ESG_Policies_Governance,
  "Risk Screening":Extract.Risk_Screening,
  "Certification Compliance":Extract.Certification_Compliance,
  "Sustainability Performance":Extract.Sustainability_Performance,
  "Collaboration & Innovation":Extract.Collaboration_Innovation,
  "Supplier":Extract.Supplier,
  "CDP Score":Extract.CDP_Score,
  "Product":Extract.Product,
  "Certification":Extract.Certification,
  "Management":Extract.Management,
  "Monitoring":Extract.Monitoring,

  
  }
  
  return sections[section]



def sections_find_fun_question(section:str):
  sections={
  "Company Overview":questions.Company_Overview,
  "Business Operations":questions.Business_Operations,
  "Clients Partnerships":questions.Clients_Partnership,
  "Technology Innovation":questions.Technology_Innovation,
  "Risk and Business Continuity":questions.Risk_and_Business_Continuity,
  "Company Growth":questions.Company_Growth,
  "Workforce":questions.Workforce,
  "ESG Policies Governance":questions.ESG_Policies_Governance,
  "Risk Screening":questions.Risk_Screening,
  "Certification Compliance":questions.Certification_Compliance,
  "Sustainability Performance":questions.Sustainability_Performance,
  "Collaboration & Innovation":questions.Collaboration_Innovation,
  "Supplier":questions.Supplier,
  "CDP Score":questions.CDP_Score,
  "Product":questions.Product,
  "Certification":questions.Certification,
  "Management":questions.Management,
  "Monitoring":questions.Monitoring,
  "GHG Reporting Standards & Methodology":questions.GHG_Reporting_Standards_Methodology,
  "Emissions":questions.Emissions,
  "Supply Chain Emissions":questions.Supply_Chain_Emissions,
  "Upstream Categories":questions.Upstream_Categories,
  "Downstream Categories":questions.Downstream_Categories,
  "Exclusion":questions.Exclusion,
  "GHG Reduction Targets":questions.GHG_Reduction_Targets,
  "Resource Management":questions.Resource_Management,
  "Waste":questions.Waste,
  "Biodiversity":questions.Biodiversity,
  "energy":questions.energy,
  "CDP":questions.CDP,
  "Financial":questions.Financial,  
  }
  
  return sections[section]


@app.post("/submit/")
async def extract_document(payload:RequestBody,db: Session = Depends(get_db)):
    # item=payload.item
    category=payload.activeCategory
    section=payload.item.quesSection
    # print("Category YTHIS ",category,section)
    report=payload.report
    print("KIKII",report,payload.date)
    categoryfind=category_find_fun(category)
    section_questions=sections_find_fun_question(section)
    # print(section_questions)
    # print(payload.kratos)
    for item in section_questions:
        if item["question"] in payload.kratos:
            item["answer"] = payload.kratos[item["question"]]
            
    print(categoryfind)
    print("***********")
    print(section)
    print("***********")
    print(section_questions)
    
    # PDFTable = create_pdf_model(report)


    # PDFTable.__table__.create(bind=db.get_bind(), checkfirst=True)
    
    for item in section_questions:
        record = supply_chain_management(
            category=category,
            section=section,
            question=item["question"],
            answer=item["answer"]
        )
        db.add(record)

    # Commit to DB
    db.commit()
    db.close()    
    return section
    
    
    
# @app.get("/download/")
# async def download_pdf(section:str, db: Session = Depends(get_db)):
#     print(section)
#     rows = db.query(supply_chain_management).all()
#     print(rows)
    
#     return "PDF DOWNLOAD SUCESSFULLY !"


@app.delete("/delete/{section}")
async def delete_fun(section:str,db:Session=Depends(get_db)):
    data=db.query(supply_chain_management).filter(supply_chain_management.section==section).all()
    print(data)
    return f"{data}PDF DELETED SUCESSFULLY !"



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=False, log_level="debug" )

