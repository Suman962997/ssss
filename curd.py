from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Example model
class Report(BaseModel):
    id: int
    title: str
    description: str

# Mock database
reports = {
    1: {"title": "First Report", "description": "This is the first report."},
    2: {"title": "Second Report", "description": "This is the second report."},
}

@app.put("/update/{report_id}")
async def update_report(report_id: int, report: Report):
    if report_id not in reports:
        raise HTTPException(status_code=404, detail="Report not found")
    
    # Update the "database"
    reports[report_id] = {
        "title": report.title,
        "description": report.description
    }
    return {"message": "Report updated successfully", "data": reports[report_id]}
