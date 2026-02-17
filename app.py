import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION ---
API_KEY = "AIzaSyBgWOeOEeMB-mYzL3yXNKmVii0uWJwuiNo"

if API_KEY == "YOUR_GEMINI_API_KEY":
    st.error("⚠️ Please replace 'YOUR_GEMINI_API_KEY' in the code with your actual API key.")
    st.stop()

genai.configure(api_key=API_KEY)

#configure the model generation settings
generation_config = {
    "temperature": 1,
    "top_p" : 0.95,
    "top_k" : 64,
    "max_output_tokens": 1024,
    "response_mime_type": "text/plain",
}

#to generate resume
def generate_resume(name, job_title):
  
  model = genai.GenerativeModel('gemini-2.5-flash')
  prompt = f"""
    You are a professional resume writer and career expert.

Generate a clean, professional resume in Markdown format using the following inputs:
- Candidate Name: {name}
- Job Title: {job_title}

Follow these rules strictly:
- Output must be in Markdown
- Use clear section headings and bullet points
- Keep the tone professional and ATS-friendly
- Do NOT invent real companies, people, or credentials
- Use placeholders where personal or sensitive details are required
- Assume the candidate is a fresher or early-career professional unless the job title implies otherwise
- Customize skills, experience, and projects based on the given job title
- Use generic but role-relevant content

The resume MUST include the following sections in this order:

1. Name (main heading)
2. Job Title (below the name)
3. Contact Information  
   (Use placeholders: email, phone number, LinkedIn URL)

4. Professional Summary  
   - 3–4 lines tailored to the given job title  
   - Highlight relevant skills, responsibilities, and impact  
   - Use placeholders for years of experience if needed  

5. Experience  
   - Add one relevant role aligned with the job title  
   - Use placeholders for company name, location, and dates  
   - Include 3–4 bullet points describing responsibilities or achievements  
   - Use placeholders for metrics, tools, and results  

6. Projects  
   - Add 2 relevant projects related to the job title  
   - Use placeholders for project titles, tools, technologies, and outcomes  
   - Include optional project links as placeholders  

7. Skills  
   - Technical Skills (role-specific)  
   - Tools / Technologies  
   - Soft Skills (communication, teamwork, problem-solving, etc.)  

8. Education  
   - University Name, Location (placeholders)  
   - Degree, Major (placeholders)  
   - Graduation Year (placeholder)  
   - Optional relevant coursework or certifications  

Formatting requirements:
- Use bullet points where appropriate
- Keep spacing clean and readable
- Do not include explanations or extra commentary
- Return ONLY the resume content
- Ensure the formatting, structure, and wording closely resemble a real professional resume.

    """
  try:
        response = model.generate_content(prompt)
        return response.text
  except Exception as e:
        return f"Error generating summary: {e}"
  

# --- BACKEND: AI GENERATION FUNCTION ---
def generate_summary_with_ai(name, job_title, tone):
    """Sends a prompt to the AI model to generate a professional summary."""
    model = genai.GenerativeModel('gemini-2.5-flash') # Using the faster flash model
    
    prompt = f"""
    Write a professional, 3-sentence resume summary for a candidate named {name} 
    who is applying for the role of {job_title}. 
    The tone should be {tone}.
    Focus on being results-oriented. Do not include placeholders.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating summary: {e}"

# --- FRONTEND: STREAMLIT UI ---
st.title("AI Resume Generator")
st.markdown("Generate and export a resume summary instantly.")

# 1. User Input
with st.form("resume_form"):
    name = st.text_input("Enter your name", value="ABCAtlas")
    job_title = st.text_input("Enter your job title", value="Machine Learning Engineer")
    #tone = st.selectbox("Select Tone", ["Professional", "Creative", "Academic"], index=0)
    
    submitted = st.form_submit_button("Generate Resume Content")

# 2. Processing & Generation
if submitted:
    if name and job_title:
        with st.spinner('AI is writing your summary...'):
            generated_summary = generate_resume(name, job_title)
            
            # Save to session state
            st.session_state['summary'] = generated_summary
            st.session_state['name'] = name
            st.session_state['job_title'] = job_title
            
        st.success("Content Generated!")
    else:
        st.error("Please fill in all fields.")

# 3. Customization & 4. Export
if 'summary' in st.session_state:
    st.subheader("Review & Edit")
    
    # Allow user to edit the AI output
    final_summary = st.text_area(
        "Edit the AI-generated summary if needed:", 
        value=st.session_state['summary'],
        height=150
    )
    
    st.markdown("---")
    
    # Format the text for export
    export_text = f"Name: {st.session_state['name']}\nRole: {st.session_state['job_title']}\n\n--- PROFESSIONAL SUMMARY ---\n\n{final_summary}"
    
    # Streamlit's native download button handles text strings directly!
    st.download_button(
        label="⬇️ Download as Text File (.txt)",
        data=export_text,
        file_name=f"{st.session_state['name']}_Resume_Summary.txt",
        mime="text/plain"
    )