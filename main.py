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
import Extract
from sqlalchemy.orm import Session
from typing import Dict,Any,List,Optional
import questions
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
        undefined_count += 1
        return "Undefined" if undefined_count == 1 else f"Undefined{undefined_count}"
    return report



    
def risklevel_def(score):
    if score is None or score =="":
        return ""
    elif 20>=score:
        return "High"

    elif 20<50>=score:
        return "Medium"

    elif 50<100>=score:
        return "Low"
    



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
        "riskScore":0,
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
        "aboutUs": "Our founding in 1930, we have been working hard every day to meet our customers' needs, from design and manufacturing to maintenance of fluid control systems centered on valves, under our company motto of 'progressive development.",
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


# black={
#     [
#         {
#         "title": "Revenue",
#         "type": "revenue",
#         "description": "Total Revenue: $1.2M",
#         "buttonText": "View Details",
#         "growth": "8.5% (YoY)",
#         "lastMonth": "$100K"
#         },
#         {
#         "title": "Performance Feedback",
#         "type": "performancefeedback",
#         "description": "Average Rating: 4.5/5",
#         "buttonText": "View Feedbacks",
#         "positiveFeedback": "85%",
#         "customerComplaints": "12"
#         },
#         {
#         "title": "Audits Information",
#         "type": "auditsinformation",
#         "description": "Compliance Status: Passed",
#         "buttonText": "View Audit Reports",
#         "lastAudit": "Sep 2023",
#         "nextAuditDue": "Mar 2024"
#         },
#         {
#         "title": "Supplier Compliance",
#         "type": "suppliercompliance",
#         "description": "Compliance Score: 95%",
#         "buttonText": "View Compliance",
#         "issues": "3 Pending",
#         "lastReview": "1 Month Ago"
#         },
#         {
#         "title": "Order History",
#         "type": "orderhistory",
#         "description": "Total Orders: 520",
#         "buttonText": "Order History",
#         "completedOrders": "510",
#         "pendingOrders": "10"
#         },
#         {
#         "title": "Certifications",
#         "type": "certifications",
#         "description": "Total Certifications: 520",
#         "buttonText": "View Certifications",
#         "validCertifications": "04",
#         "expiredCertifications": "0"
#         }
#         ]
#     }


# {
#         "key": "green",
#         "supplier": "Green Field Material Handling",
#         "industry": "Automobile",
#         "service": [
#           "Samson material handeling",
#           "Samson solar power Samson",
#           "agro equipment",
#           "Samson agro biotech"
#         ],
#         "product": "",
#         "website": "https://samsonmaterialhandling.com/",
#         "websiteName": "samsonmaterialhandling.com",
#         "companyId": "15468456",
#         "location": "Plot No. N-49/1, MIDC, Additional Ambernath Indl. Area, Ambernath (E), Thane - 421506, Maharashtra, India.",
#         "certification": [
#           {
#             "environment_management_system": "ISO 14001:2004"
#           },
#           {
#             "health&safety_management_system": "OHSAS 18001:2007"
#           },
#           {
#             "quantity_management_system": "ISO9001:2008"
#           }
#         ],
#         "riskScore": 84,
#         "riskLevel": "Low",
#         "compliance": "Compliant",
#         "category": "Safety Material",
#         "cyberRiskScore": 90,
#         "financialRiskScore": 40,
#         "healthScore": 60,
#         "environment": 79,
#         "social": 80,
#         "governance": 60,
#         "healthSafety": 90,
#         "status": True,
#         "email": "info@hararamagroup.com",
#         "contactUs": "+91 251 3217880 / +91 251 2621681",
#         "aboutUs": "Green Field Material Handling P. Ltd., An ISO 9001-2000 Certified Company, a group of companies founded in 1990, offering a wide range of products and services to industry in the specialized field of materials handling and lifting. The vital strength of the organization is the vast experience of our key person, for more than two decades, in the field of Material Handling and Critical Lifting, which has solved a lot of lifting problems in India and Overseas as well. Our accomplished engineering sales force could solve any sort of lifting problems. Advise and implement up-to-date, latest innovative designs and solutions to meet newer challenges. We sincerely attend to your requirement, small or large, from a single hook to a 50-meter long non-metallic sling. Our speciality is heavy-duty non-metallic sling, made of polyester. These are of two types: flat webbing sling with Eye-loop at the ends and Round (endless) slings. Both are available in different lengths and weight lifting capacities, ranging from 1 ton up to 300 tons. We also have various types of Hooks, D-Shackles, Bow Shackles, Multi-leg slings, Master Rings & Cargo lashings, Safety Harness, lifting beams, lifting clamps & crane weighing systems, etc. The Green Field's efficient personnel are always available to advise you on any type of problem in material handling and lifting."
#       }



    
 
    
@app.get("/dashboard/")
async def dashboard(db:Session=Depends(get_db)):
    dashboard_list=db.query(TableRegistry).order_by(TableRegistry.created_at.asc()).all()
    report_list = [report.copy() for _ in range(len(dashboard_list))]

    def rr(table,question):
        REPORTTABLE = create_pdf_model(table)
        result = db.query(REPORTTABLE).filter(REPORTTABLE.question==question).first()
        if result is None:
            return ""
        return result.answer

    def gr(table,question):
        REPORTTABLE = create_pdf_model(table)
        result = db.query(REPORTTABLE).filter(REPORTTABLE.question==question).first()
        if result is None:
            return ""
        return result.answer.split(",")

    for i,dl in enumerate(dashboard_list):
        report_list[i]["supplier"]=dl.table_name
        report_list[i]["key"]=dl.table_name
        report_list[i]["industry"]=dl.industry
        report_list[i]["category"]=dl.category
        report_list[i]["riskScore"]=dl.riskscore
        report_list[i]["riskLevel"]=dl.risklevel
        report_list[i]["compliance"]=dl.compliance
        report_list[i]["status"]=dl.status
        report_list[i]["location"]=rr(dl.table_name,"Where is the company headquartered?")
        report_list[i]["service"]=gr(dl.table_name,"What is the product name, type, and function?")
        report_list[i]["email"]=rr(dl.table_name,"Email")
        report_list[i]["contactUs"]=rr(dl.table_name,"Contact No")

        # report_list[i][""]=dl.status
        # report_list[i][""]=dl.status
        # report_list[i][""]=dl.status
        # report_list[i][""]=dl.status
        
        
        


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
    card[5]["value"]="0"
    
    demo_list=[
      {
        "key": "green",
        "supplier": "Green Field Material Handling",
        "industry": "Automobile",
        "service": [
          "Samson material handeling",
          "Samson solar power Samson",
          "agro equipment",
          "Samson agro biotech"
        ],
        "product": "",
        "website": "https://samsonmaterialhandling.com/",
        "websiteName": "samsonmaterialhandling.com",
        "companyId": "15468456",
        "location": "Plot No. N-49/1, MIDC, Additional Ambernath Indl. Area, Ambernath (E), Thane - 421506, Maharashtra, India.",
        "certification": [
          {
            "environment_management_system": "ISO 14001:2004"
          },
          {
            "health&safety_management_system": "OHSAS 18001:2007"
          },
          {
            "quantity_management_system": "ISO9001:2008"
          }
        ],
        "riskScore": 84,
        "riskLevel": "Low",
        "compliance": "Compliant",
        "category": "Safety Material",
        "cyberRiskScore": 90,
        "financialRiskScore": 40,
        "healthScore": 60,
        "environment": 79,
        "social": 80,
        "governance": 60,
        "healthSafety": 90,
        "status": True,
        "email": "info@hararamagroup.com",
        "contactUs": "+91 251 3217880 / +91 251 2621681",
        "aboutUs": "Green Field Material Handling P. Ltd., An ISO 9001-2000 Certified Company, a group of companies founded in 1990, offering a wide range of products and services to industry in the specialized field of materials handling and lifting. The vital strength of the organization is the vast experience of our key person, for more than two decades, in the field of Material Handling and Critical Lifting, which has solved a lot of lifting problems in India and Overseas as well. Our accomplished engineering sales force could solve any sort of lifting problems. Advise and implement up-to-date, latest innovative designs and solutions to meet newer challenges. We sincerely attend to your requirement, small or large, from a single hook to a 50-meter long non-metallic sling. Our speciality is heavy-duty non-metallic sling, made of polyester. These are of two types: flat webbing sling with Eye-loop at the ends and Round (endless) slings. Both are available in different lengths and weight lifting capacities, ranging from 1 ton up to 300 tons. We also have various types of Hooks, D-Shackles, Bow Shackles, Multi-leg slings, Master Rings & Cargo lashings, Safety Harness, lifting beams, lifting clamps & crane weighing systems, etc. The Green Field's efficient personnel are always available to advise you on any type of problem in material handling and lifting."
      },
      {
        "key": "fasteners",
        "supplier": "V.K. Fasteners Private Limited",
        "industry": "Automobile",
        "service": "",
        "product": [
          "HEX HEAD FLANGE SCREW/BOLT",
          "Cross pan/flat screw",
          "Hex nut",
          "U blot"
        ],
        "location": "No.79, Valmiki Street Thiruvanmiyur, Chennai - 600 041Tamil Nadu, India",
        "certification": [
          {
            "environment_management_system": "ISO 9001:2015"
          },
          {
            "eu_certificate_of_quality_system_approval": "0343/PED/MUM/2210015/2"
          },
          {
            "quantity_management_system": "0038/UK/PER/MUM/2210015/4"
          }
        ],
        "riskScore": 73,
        "riskLevel": "Low",
        "compliance": "Compliant",
        "category": "Safety Material",
        "cyberRiskScore": 41,
        "financialRiskScore": 80,
        "healthScore": 60,
        "environment": 70,
        "social": 79,
        "governance": 55,
        "healthSafety": 80,
        "status": True,
        "companyId": "15440456",
        "website": "https://www.vkfasteners.co.in/",
        "websiteName": "www.vkfasteners.co.in",
        "email": "marketing1@vkf.co.in",
        "contactUs": "+91 89259 50777",
        "aboutUs": "VK Fasteners - Another MILESTONE of IGP Group, serving the industries more than 60 years. As a traditional family business the core values of optimization, reliability, continuity, and sustainability hold true for every business in IGP Family.Now VK Fasteners Private Limited, a group company of IGP is set at Chennai, Tamilnadu for manufacture of HIGH TENSILE FASTENERS AND PARTS to cater the need of automotive manufacturer through Cold Forging Process.Highly trained and experienced professional along with latest automatic imported bolt former with quality control equipment shall assure you ONTIME DELIVERY AND BEST QUALITY Plant has a installed capacity around 5000MTPA Plant is capable enough to produce all types of fasteners to national and international standards and to customer designed specification"
      },
      {
        "key": "rahul",
        "supplier": "Rahul Agencies",
        "industry": "Automobile",
        "service": "",
        "product": [
          "Epoxy adhesive",
          "Steam solenoid servo valve",
          "Flow control valve",
          "Pneumatic cylinder",
          "Pneumatic actuators",
          "Solenoid coil",
          "Auto drain valve",
          "Pneumatic tubes",
          "Air cylinders"
        ],
        "location": "Plot No. N-49/1, MIDC, Additional Ambernath Indl. Area, Ambernath (E), Thane - 421506, Maharashtra, India.",
        "certification": "Power tool accessories & fasteners and hand tools",
        "riskScore": 48,
        "riskLevel": "Medium",
        "compliance": "Compliant",
        "category": "Adhesive",
        "cyberRiskScore": 35,
        "financialRiskScore": 52,
        "healthScore": 60,
        "environment": 40,
        "social": 17,
        "governance": 69,
        "healthSafety": 34,
        "companyId": "15110451",
        "website": "https://rahulagencies.in/",
        "websiteName": "rahulagencies.in",
        "status": True,
        "email": "mayur.rahulagencies@gmail.com",
        "contactUs": "+91 9824138242",
        "aboutUs": "Established as a Proprietor firm in the year 2019 at Vapi (Gujarat, India), we “Rahul Agencies” are a leading Distributor / Channel Partner of a wide ran of Solenoid Valves, Pneumatic Cylinder, etc. We procure these products from the most trusted and renowned vendors after stringent market analysis. Further, we offer these products at reasonable rates and deliver these within the promised time-frame. Under the headship of “Mr. Mayur Shah”, we have gained a huge clientele across the nation."
      },
      {
        "key": "sonic",
        "supplier": "Sonic Enterprises",
        "industry": "Oil and Gas",
        "service": "",
        "product": [
          "Pumps",
          "fans",
          "Room heater",
          "Exhaust motors",
          "Electric iron",
          "Immersion rod"
        ],
        "location": "Meerut Road Industrial Area, Ghaziabad - 201003, Uttar Pradesh, India",
        "certification": "",
        "riskScore": 42,
        "riskLevel": "Medium",
        "compliance": "Non-Compliant",
        "category": "Safety Material",
        "cyberRiskScore": 50,
        "financialRiskScore": 40,
        "healthScore": 60,
        "environment": 37,
        "social": 31,
        "governance": 49,
        "healthSafety": 19,
        "status": False,
        "email": "sonic.surat@gmail.com",
        "companyId": "10110411",
        "website": "https://www.sonichomeappliances.com/",
        "websiteName": "www.sonichomeappliances.com",
        "contactUs": "+91 9998012325",
        "aboutUs": "We “Sonic Enterprise” founded in the year 2005 are a renowned firm that is engaged in manufacturing a wide assortment of Kitchen Jali, PVC Curtain Bracket Holder, PVC Curtain Bracket, Wall Hanger, etc. We have a wide and well functional infrastructural unit that is situated at Rajkot (Gujarat, India) and helps us in making a remarkable collection of products as per the set industry standards. We are a Sole Proprietorship firm that is managed under the headship of “Mr. Mukesh” (Manager), and have achieved a significant position in this sector"
      }]    
    return {"card_list":card,"report_list":report_list}
    # return {"card_list":card,"report_list":demo_list}




@app.post("/submit/")
async def extract_document(payload: RequestBody, db: Session = Depends(get_db)):
    category = payload.activeCategory
    section = payload.item.quesSection
    kratos = payload.kratos
    report = kratos.get("Report name", "")
    date = kratos.get("Date", "")    
    industry = kratos.get("industry", "")    

    categoryfind = category_find_fun(category)
    section_questions = sections_find_fun_question(section)

    # attach answers to section questions if present in kratos
    for item in section_questions:
                    
        if item["question"] in kratos:
            item["answer"] = kratos[item["question"]]

    report = get_report_name(report)    

    # check if report already exists in registry
    check = db.query(TableRegistry).filter(TableRegistry.table_name == report).first()
    REPORTTABLE = create_pdf_model(report)

    if check:
        print("🐍🪼🐚🦀")

        # add only if record not already there
        for question, answer in kratos.items():
            exists = db.query(REPORTTABLE).filter_by(
                category=categoryfind,
                section=section,
                question=question
            ).first()
            if not exists:
                db.add(REPORTTABLE(
                    section=section,
                    category=categoryfind,
                    question=question,
                    answer=answer
                ))

        db.commit()
        db.close()
        return report

    # if report is new → create table + registry entry
    REPORTTABLE.__table__.create(bind=db.get_bind(), checkfirst=True)
    Base.metadata.create_all(bind=db.get_bind(), tables=[TableRegistry.__table__])
    score=randoms.Risk_Score()
    registry_entry = TableRegistry(
        table_name=report,
        industry=industry,
        category=categoryfind,
        riskscore=score,
        risklevel=risklevel_def(score),
        compliance=randoms.Compliance(),
        status=randoms.Status(),
        section=section,
        date=date
    )
    db.add(registry_entry)
    db.commit()

    # insert all Q/A for this new report
    for question, answer in kratos.items():
        db.add(REPORTTABLE(
            section=section,
            category=categoryfind,
            question=question,
            answer=answer
        ))

    db.commit()
    db.close()    
    return report


@app.put("/update/")
async def update_document(report:dict,db:Session=Depends(get_db)):
    print(report)
    report=report["key"]
    if report:
        name=db.query(TableRegistry).filter_by(table_name=report).first()
        if not name:
            raise HTTPException(status_code=404, detail=f"Table '{report}' not found in registry.")
        print("looo")
        return report
        

@app.delete("/delete/{report}")
async def delete_fun(report:str,db:Session=Depends(get_db)):
    
    # data=db.query(TableRegistry).filter(TableRegistry.table_name==report).all()
    
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

