import streamlit as st
import time
import PyPDF2
import io
import random

# Set page configuration
st.set_page_config(
    page_title="Resume Analyzer", 
    page_icon="📄", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Simple CSS for minimal styling
st.markdown("""
<style>
    .main-title {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 30px;
    }
    .upload-box {
        border: 2px dashed #1f77b4;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        margin: 20px 0;
        background-color: #f9f9f9;
    }
    .result-box {
        background-color: #f0f8ff;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .match-score {
        font-size: 32px;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin: 15px 0;
    }
    .keyword-pill {
        display: inline-block;
        background-color: #e0f0ff;
        color: #1f77b4;
        padding: 6px 12px;
        border-radius: 16px;
        margin: 4px;
        font-size: 14px;
    }
    .good-score { color: #2ecc71; }
    .average-score { color: #f39c12; }
    .poor-score { color: #e74c3c; }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'analysis_data' not in st.session_state:
    st.session_state.analysis_data = None
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False
if 'resume_file' not in st.session_state:
    st.session_state.resume_file = None

# Function to extract text from uploaded file
def extract_text_from_file(uploaded_file):
    try:
        if uploaded_file.type == "application/pdf":
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            return text if text.strip() else None
        elif uploaded_file.type == "text/plain":
            return str(uploaded_file.read(), "utf-8")
        else:
            return None
    except Exception as e:
        st.error(f"Error reading file: {str(e)}")
        return None

# Function to calculate a more realistic score
def calculate_match_score(resume_text, job_description):
    # This is a simplified simulation of how a real AI might analyze the resume
    # In a real application, this would use NLP techniques to analyze content
    
    # Base score starts at 50
    score = 50
    
    # Adjust score based on resume length (longer resumes tend to have more content)
    resume_length = len(resume_text)
    if resume_length > 1000:
        score += 10
    elif resume_length > 500:
        score += 5
    
    # Adjust score based on job description length
    job_length = len(job_description)
    if job_length > 500:
        # More detailed job descriptions allow for better matching
        score += 5
    
    # Check for common important keywords in tech roles
    important_keywords = [
        "python", "javascript", "java", "sql", "aws", "docker", 
        "kubernetes", "react", "node", "api", "cloud", "agile",
        "scrum", "devops", "ci/cd", "machine learning", "ai"
    ]
    
    # Count how many important keywords appear in the resume
    resume_lower = resume_text.lower()
    keyword_count = sum(1 for keyword in important_keywords if keyword in resume_lower)
    score += min(keyword_count * 3, 15)  # Max 15 points for keywords
    
    # Add some random variation to make it more realistic
    score += random.randint(-5, 5)
    
    # Ensure score is within reasonable bounds
    return max(40, min(score, 95))

# Function to generate relevant feedback based on content
def generate_feedback(resume_text, job_description, score):
    feedback = {
        "strengths": [],
        "improvements": [],
        "missing_keywords": []
    }
    
    resume_lower = resume_text.lower()
    job_lower = job_description.lower()
    
    # Common strengths
    if len(resume_text) > 800:
        feedback["strengths"].append("Comprehensive resume with detailed experience")
    else:
        feedback["improvements"].append("Consider adding more details about your experience")
    
    # Check for quantifiable achievements
    if any(word in resume_lower for word in ["increased", "decreased", "improved", "reduced", "saved"]):
        feedback["strengths"].append("Good use of quantifiable achievements")
    else:
        feedback["improvements"].append("Add metrics to quantify your achievements (e.g., 'increased efficiency by 20%')")
    
    # Check for technical skills
    tech_keywords = ["python", "java", "javascript", "sql", "html", "css", "react", "node"]
    found_tech = [kw for kw in tech_keywords if kw in resume_lower]
    if found_tech:
        feedback["strengths"].append(f"Strong technical skills including {', '.join(found_tech[:3])}")
    else:
        feedback["improvements"].append("Highlight your technical skills more prominently")
    
    # Check for action verbs
    action_verbs = ["developed", "designed", "implemented", "managed", "led", "created"]
    if any(verb in resume_lower for verb in action_verbs):
        feedback["strengths"].append("Effective use of action verbs")
    else:
        feedback["improvements"].append("Start bullet points with action verbs (e.g., 'Developed', 'Designed', 'Implemented')")
    
    # Find missing keywords from job description
    job_words = set(job_lower.split())
    resume_words = set(resume_lower.split())
    missing = job_words - resume_words
    
    # Filter to only include relevant keywords
    relevant_keywords = [word for word in missing if len(word) > 5 and word.isalpha()]
    feedback["missing_keywords"] = relevant_keywords[:6]  # Limit to 6 keywords
    
    return feedback

# Function to simulate AI analysis
def analyze_resume_with_ai(resume_text, job_title, job_description):
    # Simulate processing time
    time.sleep(2)
    
    # Calculate a more realistic score
    match_score = calculate_match_score(resume_text, job_description)
    
    # Generate feedback based on content
    feedback = generate_feedback(resume_text, job_description, match_score)
    
    # Generate analysis based on inputs
    position = job_title if job_title else "this position"
    analysis = {
        "match_score": match_score,
        "summary": f"Your resume shows a {match_score}% match with {position}.",
        "strengths": feedback["strengths"],
        "improvements": feedback["improvements"],
        "missing_keywords": feedback["missing_keywords"]
    }
    
    return analysis

# Function to generate report text
def generate_report_text(analysis_data, job_title):
    position = job_title if job_title else "the position"
    report = f"Resume Analysis Report for {position}\n"
    report += "=" * 50 + "\n\n"
    report += f"Match Score: {analysis_data['match_score']}%\n\n"
    report += "SUMMARY:\n"
    report += f"{analysis_data['summary']}\n\n"
    
    report += "STRENGTHS:\n"
    for strength in analysis_data['strengths']:
        report += f"- {strength}\n"
    report += "\n"
    
    report += "AREAS FOR IMPROVEMENT:\n"
    for improvement in analysis_data['improvements']:
        report += f"- {improvement}\n"
    report += "\n"
    
    report += "MISSING KEYWORDS:\n"
    for keyword in analysis_data['missing_keywords']:
        report += f"- {keyword}\n"
    
    return report

# Main app
def main():
    # Header
    st.markdown("<h1 class='main-title'>📄 AI Resume Analyzer</h1>", unsafe_allow_html=True)
    
    st.write("Upload your resume and job description to get AI-powered analysis and improvement suggestions.")
    
    # File upload section
    st.markdown("### Upload Your Resume")
    st.markdown("<div class='upload-box'>📤 Drag and drop your resume here (PDF or TXT)</div>", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose a file", 
        type=["pdf", "txt"],
        label_visibility="collapsed"
    )
    
    if uploaded_file is not None:
        st.session_state.resume_file = uploaded_file
        st.success(f"File uploaded: {uploaded_file.name}")
    
    # Job details
    st.markdown("### Job Information")
    job_title = st.text_input("Job Title (Optional)", placeholder="e.g., Software Engineer")
    job_description = st.text_area("Job Description*", height=150, placeholder="Paste the job description here...", help="Required field")
    
    # Analyze button
    if st.button("Analyze Resume", type="primary", use_container_width=True):
        if not job_description or not st.session_state.resume_file:
            st.error("Please upload your resume and provide a job description")
        else:
            with st.spinner("Analyzing your resume..."):
                resume_text = extract_text_from_file(st.session_state.resume_file)
                
                if resume_text is None:
                    st.error("Could not extract text from the file. Please try a different file.")
                else:
                    # Perform analysis
                    analysis_result = analyze_resume_with_ai(resume_text, job_title, job_description)
                    st.session_state.analysis_data = analysis_result
                    st.session_state.analysis_complete = True
                    st.rerun()
    
    # Display results if analysis is complete
    if st.session_state.analysis_complete and st.session_state.analysis_data:
        st.markdown("---")
        st.markdown("## Analysis Results")
        
        # Match score with color coding
        score = st.session_state.analysis_data['match_score']
        score_class = "good-score" if score >= 75 else "average-score" if score >= 60 else "poor-score"
        
        st.markdown(f"<div class='match-score {score_class}'>{score}% Match</div>", unsafe_allow_html=True)
        
        # Progress bar
        st.progress(score / 100)
        
        # Score interpretation
        if score >= 75:
            st.success("Strong match! Your resume aligns well with the job requirements.")
        elif score >= 60:
            st.warning("Moderate match. Your resume has some alignment but could be improved.")
        else:
            st.error("Weak match. Consider tailoring your resume more specifically to this role.")
        
        # Summary
        st.markdown("### Summary")
        st.info(st.session_state.analysis_data['summary'])
        
        # Two columns for strengths and improvements
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### ✅ Strengths")
            for strength in st.session_state.analysis_data['strengths']:
                st.markdown(f"- {strength}")
        
        with col2:
            st.markdown("### 📈 Improvements")
            for improvement in st.session_state.analysis_data['improvements']:
                st.markdown(f"- {improvement}")
        
        # Missing keywords with improved UI
        if st.session_state.analysis_data['missing_keywords']:
            st.markdown("### 🔍 Keywords to Consider")
            st.write("These keywords from the job description are missing from your resume:")
            
            # Create a container for the keyword pills
            keywords_html = "<div style='margin: 10px 0;'>"
            for keyword in st.session_state.analysis_data['missing_keywords']:
                keywords_html += f"<span class='keyword-pill'>{keyword}</span>"
            keywords_html += "</div>"
            
            st.markdown(keywords_html, unsafe_allow_html=True)
        else:
            st.markdown("### 🔍 Keywords")
            st.info("Good job! Your resume includes most relevant keywords from the job description.")
        
        # Generate report text for download
        report_text = generate_report_text(st.session_state.analysis_data, job_title)
        
        # Action buttons
        st.markdown("---")
        col3, col4 = st.columns(2)
        
        with col3:
            if st.button("Analyze Another Resume", use_container_width=True):
                st.session_state.analysis_complete = False
                st.session_state.analysis_data = None
                st.session_state.resume_file = None
                st.rerun()
        
        with col4:
            # Fixed download button
            st.download_button(
                "Download Report",
                report_text,
                file_name=f"resume_analysis_{time.strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain",
                use_container_width=True
            )

# Run the app
if __name__ == "__main__":
    main()