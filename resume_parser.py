import fitz  # PyMuPDF
import re
from typing import List

def extract_text_from_pdf(pdf_path: str) -> str:
    with fitz.open(pdf_path) as doc:
        return "\n".join([page.get_text() for page in doc])

def extract_email(text: str) -> str:
    match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    return match.group(0) if match else "N/A"

def extract_name(text: str) -> str:
    lines = text.strip().split("\n")
    # Heuristic: likely the top line, or first line with 2+ capitalized words
    for line in lines[:5]:
        if len(line.split()) >= 2 and all(w[0].isupper() for w in line.split() if w):
            return line.strip()
    return lines[0].strip()

def extract_skills(text: str) -> List[str]:
    # You can expand this list based on your job roles
    skills_list = [
        "Python", "Java", "C++", "SQL", "Machine Learning", "Deep Learning", "NLP",
        "Django", "Flask", "FastAPI", "AWS", "Azure", "React", "Node.js", "Git", 
        "Docker", "Kubernetes", "Pandas", "NumPy", "TensorFlow", "PyTorch", "Power BI"
    ]
    text_lower = text.lower()
    extracted_skills = [skill for skill in skills_list if skill.lower() in text_lower]
    return extracted_skills

def extract_info(text: str):
    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "skills": extract_skills(text)
    }