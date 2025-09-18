import json
import pdfplumber
import docx
from fastapi import FastAPI, UploadFile, File, Form,Depends, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.dialects.postgresql import insert
import os
from sqlalchemy import Column, Integer, String, ForeignKey, Text,text,inspect,desc,func
from database import create_engine,SessionLocal
from dotenv import load_dotenv
# from Extract import Biodiversity
import Extract
from sqlalchemy.orm import Session
from typing import Dict,Any,List,Optional
import questions
# import pdf
from models import create_pdf_model,TableRegistry,Base
import randoms

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






undefined_count=0

def get_report_name(report: str | None) -> str:
    if report != "":
    
        return report
    global undefined_count
    if not report or report.strip() == "":
        print("REP UNID")
        undefined_count += 1
        return "Undefined" if undefined_count == 1 else f"Undefined{undefined_count}"
    return report




@app.post("/submit/")
async def extract_document(payload:RequestBody,db: Session = Depends(get_db)):
    category=payload.activeCategory
    section=payload.item.quesSection
    kratos=payload.kratos
    report=kratos.get("Report name","")
    date=kratos.get("Date","")    
    categoryfind=category_find_fun(category)
    section_questions=sections_find_fun_question(section)
    for item in section_questions:
        if item["question"] in payload.kratos:
            item["answer"] = payload.kratos[item["question"]]
    report=get_report_name(report)    
    print("***************** report _ name ",report,"0.0.0.0",date)
    REPORTTABLE = create_pdf_model(report)
    REPORTTABLE.__table__.create(bind=db.get_bind(), checkfirst=True)
    Base.metadata.create_all(bind=db.get_bind(), tables=[TableRegistry.__table__])

    registry_entry = TableRegistry(section=section,category=categoryfind,table_name=report,date=date)
    db.add(registry_entry)
    db.commit()


    for item in section_questions:
        record = REPORTTABLE(
            section=section,
            category=categoryfind,
            question=item["question"],
            answer=item["answer"]
        )
        db.add(record)


    db.commit()
    db.close()    
    return report





card=[
      {
        "name": "Active Suppliers",
        "value": "",
        "icon": "UserOutlined"
      },
      {
        "name": "Low Rated Suppliers",
        "value": "",
        "icon": "SettingOutlined"
      },
      {
        "name": "High Rated Suppliers",
        "value": "",
        "icon": "CheckCircleOutlined"
      },
      {
        "name": "Suppliers at Risk",
        "value": "",
        "icon": "UserOutlined"
      },
      {
        "name": "Audits Completed",
        "value": "",
        "icon": "SettingOutlined"
      },
      {
        "name": "On Time Delivery",
        "value": "",
        "icon": "CheckCircleOutlined"
      }
    ]


report={
        "key": "",
        "supplier": "",
        "industry": "",
        "service": [
            "NAKAKITA's serial number",
            "Plant name (Shipyard name)",
            "Plant number (Ship number)",
            "Application (Valve number)",
            "Product name, etc"
        ],
        "product": [
            {
                "productAdress": "Nozzle, Nakakita Seisakusho Co Ltd,Japan, Stainless Steel 304 Stellited, Psvs Of Uty-2 Plant",
                "key": 1,
                "name": "Nozzle",
                "location": "Yanbu, Saudi Arabia",
                "sku": "GSC034-0321-02-55664",
                "Mfg": "Nakakita Seisakusho Co Ltd, Japan",
                "unspsc": "40141731",
                "hsn": "84249000",
                "material": "Stainless Steel 304 Stellited",
                "application": "Psvs Of Uty-2 Plant"
            },
            {
                "productAdress": "Gasket, Nakakita Seisakusho Co Ltd, Japan, 27,Acbt-3294Dm",
                "key": 2,
                "name": "Gasket",
                "location": "Al-Jubail, Saudi Arabia",
                "sku": "GSC034-1120-01-18029",
                "Mfg": "Nakakita Seisakusho Co Ltd, Japan",
                "unspsc": "31401500",
                "hsn": "40169320",
                "material": "ACBT-3294DM",
                "application": "27"
            }
        ],
        "website": "https://www.demo-s.co.jp/en/companyoutline",
        "websiteName": "www.demo-s.co",
        "companyId": "100000",
        "location": "mambalam",
        "certification": [
            {
                "name": "Quality Management",
                "certificate": "ISO 9001 (LRQA)",
                "expire_date": "Expires 15 Jan 2025"
            },
            {
                "name": "Environment Management",
                "certificate": "CE Marking (LRQA)",
                "expire_date": "Expires 15 Jan 2025"
            }

        ],
        "riskScore":"86",
        "riskLevel": "",
        "compliance": "",
        "category": "",
        "cyberRiskScore": 90,
        "financialRiskScore": 40,
        "healthScore": 60,
        "environment": 79,
        "social": 80,
        "governance": 60,
        "healthSafety": 90,
        "status": True,
        "email": "demo@gmail.com",
        "contactUs": "000000000000",
        "aboutUs": "our founding in 1930, we have been working hard every day to meet our customers' needs, from design and manufacturing to maintenance of fluid control systems centered on valves, under our company motto of 'progressive development.' Meanwhile,in order to respond to the accelerating changes of the times, we are adding 'challenge' to our theme of 'protecting the present while challenging new things'. While refining our 'product development' that gives shape to the voices of our customers, we will also challenge ourselves to develop new 'technologies' and aim to be a company that proposes new values and benefits to our customers. We ask for your continued understanding and support for Nakakita Seisakusho Co., Ltd., which boldly challenges new things.",
        "history": [
            {
                "achivement": "Commenced the production of automatic control valves at Matsugae-cho, Kita-ku, Osaka under a private undertaking owned by Mr. Benzo Nakakita, the first president of Nakakita Seisakusho Co., Ltd",
                "years": "1930"
            },
            {
                "achivement": "Reopened Tokyo office and opened Kyushu office.",
                "years": "1950"
            }
        ],
        "insurance": [
            {
                "name": "Public Liability",
                "amount": "$ 1,00,000.000",
                "expire_date": "Expires 30 Nov 2024"
            },
            {
                "name": "Professional Indemnity",
                "amount": "$ 5,000.000",
                "expire_date": "Expires 22 Dec 2024"
            }
        ]
    }
    
    
    
@app.get("/dashboard/")
async def dashboard(db:Session=Depends(get_db)):
    dashboard_list=db.query(TableRegistry).order_by(TableRegistry.created_at.asc()).all()
    report_list = [report.copy() for _ in range(len(dashboard_list))]

    # REPORTTABLE = create_pdf_model("suman")
    # result = db.query(REPORTTABLE).filter(REPORTTABLE.question == "Where is the company headquartered?").first()
    # print("MOON",result.answer)
    def rr(table,question):
        REPORTTABLE = create_pdf_model(table)
        result = db.query(REPORTTABLE).filter(REPORTTABLE.question==question).first()
        if result is None:
            return ""
        return result.answer

    
    for i,dl in enumerate(dashboard_list):
        # print(db.query().filter("Where is the company headquartered?"))
        report_list[i]["supplier"]=dl.table_name
        report_list[i]["key"]=dl.table_name
        report_list[i]["industry"]=randoms.Industry()
        report_list[i]["category"]=randoms.Category()
        report_list[i]["riskScore"]=randoms.Risk_Score()
        report_list[i]["riskLevel"]=randoms.Risk_Level()
        report_list[i]["compliance"]=randoms.Compliance()
        report_list[i]["status"]=randoms.Status()
        report_list[i]["location"]=rr(dl.table_name,"Where is the company headquartered?")


    # Active Suppliers 
    card[0]["value"]=str(sum(1 for item in report_list if item.get("status") is True))
    # Low Rated Suppliers
    card[1]["value"]=str(sum(1 for item in report_list if item.get("riskLevel") == "Low"))
    # High Rated Suppliers 
    card[2]["value"]=str(sum(1 for item in report_list if item.get("riskLevel") == "High"))
    # Suppliers at Risk
    card[3]["value"]=str(sum(1 for item in report_list if item.get("riskLevel") == "High"))
    # Audits Completed
    card[4]["value"]=str(sum(1 for item in report_list if item.get("compliance") == "Compliant"))   
    # On Time Delivery
    card[5]["value"]="7"
        
    return {"card_list":card,"report_list":report_list}


@app.delete("/delete/{report}")
async def delete_fun(report:str,db:Session=Depends(get_db)):
    
    data=db.query(TableRegistry).filter(TableRegistry.table_name==report).all()
    print(data)
    
    registry_entry = db.query(TableRegistry).filter_by(table_name=report).first()
    if not registry_entry:
        raise HTTPException(status_code=404, detail=f"Table '{report}' not found in registry.")

    # Step 2: Check if the table exists in the actual database
    inspector = inspect(db.get_bind())
    if not inspector.has_table(report):
        raise HTTPException(status_code=404, detail=f"Table '{report}' does not exist in the database.")

    # Step 3: Dynamically create model
    REPORTTABLE = create_pdf_model(report)

    # Step 4: Drop the table
    try:
        REPORTTABLE.__table__.drop(bind=db.get_bind())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete table '{report}': {str(e)}")

    # Step 5: Remove the table entry from table_registry
    db.delete(registry_entry)
    db.commit()
    
    return f"{report} PDF DELETED SUCESSFULLY !"






if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=False, log_level="debug" )

