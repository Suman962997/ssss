from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

# Function to create PDF for CDP Scores
def create_pdf(cdp_data: list, pdf_name: str):
    print("Generating PDF...")

    # PDF setup
    doc = SimpleDocTemplate(pdf_name, pagesize=A4)
    story = []

    # Styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Question', fontSize=12, spaceAfter=6, leading=14, textColor=colors.black))
    styles.add(ParagraphStyle(name='Answer', fontSize=12, textColor=colors.darkblue, leftIndent=20, leading=14))

    # Add Title
    story.append(Paragraph("CDP Score Report", styles['Title']))
    story.append(Spacer(1, 12))

    # Loop through questions/answers
    for item in cdp_data:
        question = item.get("question", "")
        answer = item.get("answer", "Not Provided")

        story.append(Paragraph(f"Q: {question}", styles['Question']))
        story.append(Paragraph(f"A: {answer}", styles['Answer']))
        story.append(Spacer(1, 8))

    # Build PDF
    doc.build(story)
    print(f"PDF '{pdf_name}' created successfully.")




# Example usage
CDP_Score = [
    {"question": "What is your current CDP score for Climate Change?", "answer": None},
    {"question": "What is your current CDP score for Water?", "answer": None},
    {"question": "What is your current CDP score for Forests?", "answer": None}
]

create_pdf(CDP_Score, "cdp_score.pdf")
