# ---------- Skills ----------
SKILLS = [
    "python", "java", "c++", "sql", "excel", "nlp", "machine learning",
    "deep learning", "tensorflow", "pytorch", "aws", "docker", "kubernetes",
    "html", "css", "javascript", "react", "nodejs", "flask", "django",
    "tableau", "power bi", "matlab", "r", "sas", "git", "linux", "cloud computing"
]

# ---------- Career Map ----------
CAREER_MAP = {
    "Data Scientist": ["python", "sql", "machine learning", "nlp", "tensorflow", "pytorch", "r", "matlab", "tableau"],
    "Software Engineer": ["java", "c++", "python", "docker", "kubernetes", "git", "linux", "flask", "django"],
    "Cloud Engineer": ["aws", "docker", "kubernetes", "cloud computing", "git", "linux"],
    "Data Analyst": ["excel", "sql", "python", "tableau", "power bi", "r", "sas"],
    "Web Developer": ["html", "css", "javascript", "react", "nodejs", "python", "django", "flask"],
    "Machine Learning Engineer": ["python", "machine learning", "deep learning", "tensorflow", "pytorch", "nlp"],
    "Business Analyst": ["excel", "sql", "power bi", "tableau", "python"]
}

# ---------- Course Map ----------
COURSE_MAP = {
    "python": "Python for Everybody (Coursera)",
    "sql": "SQL for Data Science (Coursera)",
    "machine learning": "Machine Learning by Andrew Ng (Coursera)",
    "nlp": "Natural Language Processing with Transformers (Hugging Face)",
    "tensorflow": "TensorFlow Developer Certificate",
    "pytorch": "Deep Learning with PyTorch",
    "aws": "AWS Certified Solutions Architect",
    "docker": "Docker Mastery",
    "kubernetes": "Kubernetes for Developers",
    "excel": "Excel Skills for Business",
    "html": "HTML & CSS Crash Course (freeCodeCamp)",
    "css": "HTML & CSS Crash Course (freeCodeCamp)",
    "javascript": "JavaScript Essentials (Codecademy)",
    "react": "React - The Complete Guide (Udemy)",
    "nodejs": "Node.js Basics (Udemy)",
    "flask": "Flask Web Development (Udemy)",
    "django": "Django for Beginners (Udemy)",
    "tableau": "Tableau 2024 A-Z (Udemy)",
    "power bi": "Power BI Essentials (Udemy)",
    "r": "R Programming (Coursera)",
    "sas": "SAS Programming (Coursera)",
    "git": "Git & GitHub Crash Course (Udemy)",
    "linux": "Linux Command Line Basics (Udemy)",
    "cloud computing": "Cloud Computing Basics (Coursera)",
    "matlab": "MATLAB for Engineers (Coursera)"
}


import streamlit as st
from pdfminer.high_level import extract_text
from docx import Document
import re
from fuzzywuzzy import process

# ---------- Functions ----------
def extract_resume_text(file_path):
    if file_path.name.endswith('.pdf'):
        return extract_text(file_path)
    elif file_path.name.endswith('.docx'):
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    else:
        st.error("Unsupported file type")
        return ""

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    return text

def extract_skills(resume_text, skills_list):
    found_skills = []
    resume_text_lower = resume_text.lower()
    for skill in skills_list:
        # Exact match
        if skill.lower() in resume_text_lower:
            found_skills.append(skill)
    return list(set(found_skills))

def recommend_careers(skills, career_map):
    recommendations = {}
    for career, career_skills in career_map.items():
        match_count = len(set(skills) & set(career_skills))
        recommendations[career] = match_count / len(career_skills)
    sorted_recommendations = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)
    return sorted_recommendations

def suggest_skill_gaps(skills, career_recommendations, career_map, course_map):
    top_career = career_recommendations[0][0]
    required_skills = set(career_map[top_career])
    missing_skills = required_skills - set(skills)
    suggested_courses = [course_map[skill] for skill in missing_skills if skill in course_map]
    return missing_skills, suggested_courses

# ---------- Streamlit UI ----------
st.title("📄 Career Guidance from Resume")
uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf","docx"])

if uploaded_file is not None:
    text = extract_resume_text(uploaded_file)
    clean_resume = clean_text(text)
    skills = extract_skills(clean_resume, SKILLS)
    career_recommendations = recommend_careers(skills, CAREER_MAP)
    missing_skills, courses = suggest_skill_gaps(skills, career_recommendations, CAREER_MAP, COURSE_MAP)
    
    st.subheader("✅ Extracted Skills:")
    st.write(skills)
    
    st.subheader("🎯 Recommended Careers:")
    for career, score in career_recommendations:
        st.write(f"{career} - {score*100:.1f}% match")
    
    st.subheader("⚡ Skill Gaps & Suggested Courses:")
    st.write("Missing Skills:", list(missing_skills))
    st.write("Recommended Courses:", courses)
