# db_manager.py
import sqlite3
import os

DB_NAME = "resumes.db"
conn = sqlite3.connect(DB_NAME, check_same_thread=False)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS resume_data (
                id TEXT PRIMARY KEY,
                name TEXT,
                email TEXT,
                skills TEXT,
                relevance INTEGER,
                evaluation TEXT,
                status TEXT,
                job_role TEXT,
                filepath TEXT
            )''')

conn.commit()

def save_to_db(data):
    conn = sqlite3.connect("resumes.db")
    c = conn.cursor()

    # Convert list to comma-separated string
    name = data["name"]
    email = data["email"]
    skills = data["skills"]
    if isinstance(skills, list):
        skills = ', '.join(skills)
    score = data["relevance"]
    evaluation = data["evaluation"]
    status = data["status"]
    job_role = data["job_role"]
    filepath = data["filepath"]
    uid = data["id"]

    c.execute('''INSERT INTO resume_data 
                 (id, name, email, skills, relevance, evaluation, status, job_role, filepath)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (uid, name, email, skills, score, evaluation, status, job_role, filepath))

    conn.commit()
    conn.close()

def load_ranked_resumes(role_filter=None):
    conn = sqlite3.connect("resumes.db")
    c = conn.cursor()
    if role_filter:
        c.execute('SELECT * FROM resume_data WHERE job_role = ? ORDER BY relevance DESC', (role_filter,))
    else:
        c.execute('SELECT * FROM resume_data ORDER BY relevance DESC')
    data = c.fetchall()
    conn.close()
    return data