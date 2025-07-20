import os
import streamlit as st
import sqlite3
from typing import Dict
from uuid import uuid4
from difflib import SequenceMatcher

from job_descriptions import JOB_DESCRIPTIONS
from resume_parser import extract_text_from_pdf, extract_info
from gpt_evaluator import evaluate_resume_gpt
from db_manager import save_to_db, load_ranked_resumes

# ========== CONFIG ==========
DB_NAME = "resumes.db"
UPLOAD_DIR = "resumes"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ========== UTILS ==========
def compute_similarity(resume_text: str, jd: str) -> int:
    return int(SequenceMatcher(None, resume_text.lower(), jd.lower()).ratio() * 100)

# ========== STREAMLIT UI ==========
st.title("📄 AI Resume Screener & Evaluator")

menu = st.sidebar.selectbox("Menu", ["Upload & Evaluate", "Ranked Results"])

if menu == "Upload & Evaluate":
    role = st.selectbox("Select Job Role", list(JOB_DESCRIPTIONS.keys()))
    file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

    if file and role:
        uid = str(uuid4())
        filepath = os.path.join(UPLOAD_DIR, f"{uid}.pdf")
        with open(filepath, "wb") as f:
            f.write(file.read())

        resume_text = extract_text_from_pdf(filepath)
        
        print("###########", resume_text[:300])  # Log a preview

        if not resume_text.strip():
            st.error("⚠️ Could not extract text from the uploaded PDF. Please upload a valid, text-based PDF.")
        else:
            info = extract_info(resume_text)
            relevance = compute_similarity(resume_text, JOB_DESCRIPTIONS[role])
            evaluation = evaluate_resume_gpt(resume_text, JOB_DESCRIPTIONS[role])

            score = int("".join(filter(str.isdigit, evaluation.split("/100")[0]))) if "/100" in evaluation else relevance
            status = "Shortlisted" if score >= 70 else "Rejected"

            data = {
                "id": uid,
                "name": info["name"],
                "email": info["email"],
                "skills": info["skills"],
                "relevance": score,
                "evaluation": evaluation,
                "status": status,
                "job_role": role,
                "filepath": filepath
            }

            save_to_db(data)
            st.success("✅ Resume evaluated and saved.")
            st.write(data)

elif menu == "Ranked Results":
    filter_role = st.selectbox("Filter by Job Role", ["All"] + list(JOB_DESCRIPTIONS.keys()))
    data = load_ranked_resumes(None if filter_role == "All" else filter_role)

    st.write("### 🏆 Ranked Resumes")

    if not data:
        st.info("No resumes found.")
    else:
        # Wider column widths for full screen layout
        header_cols = st.columns([2.5, 3.5, 1.5, 2.5, 3, 1])
        header_cols[0].markdown("**Name**")
        header_cols[1].markdown("**Email**")
        header_cols[2].markdown("**Relevance**")
        header_cols[3].markdown("**Status**")
        header_cols[4].markdown("**Job Role**")
        header_cols[5].markdown("**Resume**")

        for r in data:
            cols = st.columns([2.5, 3.5, 1.5, 2.5, 3, 1])
            cols[0].write(r[1])  # Name
            cols[1].write(r[2])  # Email
            cols[2].write(f"{r[4]} / 100")  # Relevance
            cols[3].write(r[6])  # Status
            cols[4].write(r[7])  # Job Role

            filepath = r[8]
            if filepath and os.path.exists(filepath):
                with open(filepath, "rb") as pdf_file:
                    cols[5].download_button(
                        label="⬇️",
                        data=pdf_file,
                        file_name=os.path.basename(filepath),
                        mime="application/pdf",
                        key=f"download_{r[0]}"
                    )
            else:
                cols[5].warning("⚠️")
