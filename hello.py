import streamlit as st
import time

# --- Page Configuration ---
st.set_page_config(page_title="Resume Generator", page_icon="📄", layout="centered")

# --- Header ---
st.title("Resume Generator")
st.markdown("Create a professional resume structure for any job role instantly.")

# --- User Inputs ---
st.subheader("Candidate Details")

# Input 1: Name
name_input = st.text_input("Enter your name", placeholder="e.g. ABCAtlas")

# Input 2: Job Title
job_title_input = st.text_input("Enter your job title", placeholder="e.g. Machine Learning Engineer")

# --- Generation Trigger ---
st.markdown("---")

if st.button("Generate Resume", type="primary"):

    # 1. Validation
    if not name_input or not job_title_input:
        st.error("⚠️ Please enter both your Name and the Job Title.")
    else:

        # 2. Processing (Simulation)
        with st.spinner(f'Creating a perfect resume template for a {job_title_input}...'):
            time.sleep(1.5) # Simulate AI thinking time

            # --- SIMULATED AI OUTPUT ---
            generated_skills = "Python, TensorFlow, Scikit-learn, SQL, AWS, Deep Learning"
            generated_summary = (
                f"Results-oriented {job_title_input} with a strong background in building scalable AI solutions. "
                f"Proven track record of optimizing data pipelines and deploying models to production."
            )

            st.success("✅ Resume Generated!")
            st.divider()

            # 3. Preview Display
            st.header(name_input)
            st.subheader(job_title_input.upper())

            st.markdown(f"**Professional Summary**\n\n{generated_summary}")

            st.markdown(f"**Core Competencies**\n\n{generated_skills}")

            st.markdown("**Experience**")
            st.markdown(f"""
            * **Senior {job_title_input}** | Tech Global Inc. (2020 - Present)
                * Led a team of 5 engineers to develop...
                * Optimized algorithms reducing latency by 40%...

            * **Junior {job_title_input}** | StartupX (2018 - 2020)
                * Collaborated with cross-functional teams to...
            """)

            # 4. Download Button
            resume_content = f"{name_input}\n{job_title_input}\n\nSUMMARY:\n{generated_summary}\n\nSKILLS:\n{generated_skills}"

            st.download_button(
                label="📥 Download Resume Template",
                data=resume_content,
                file_name=f"{name_input}_Resume.txt",
                mime="text/plain"
            )