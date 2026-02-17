import os
import streamlit as st
import google.generativeai as genai

#api_key = "AIzaSxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
#genai.configure(api_key=api_key)

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
  
  context = f'name:{name}\njob_title:{job_title}\nwrite a resume for the above data'

  #start the chat session with the generative model
  chat_session = model.start_chat(
        history = [
            {
                "role": "user",
                "parts": [
                    context
                ],
            },
        ]
    )
  response = chat_session.send_message(context)
  text = response.candidates[0].content if isinstance(response.candidates[0].content, str) else response.candidates[0].content.parts[0].text
  return text

def clean_resume(text):
  
  cleaned_text = text.replace("[Add Email Address]", "[Your Email Address]")
  cleaned_text = cleaned_text.replace("[Add Phone Number]", "[Your Phone Number]")
  cleaned_text = cleaned_text.replace("[Add LinkedIn Profile]", "[Your LinkedIn Profile]")  
  cleaned_text = cleaned_text.replace("[Add GitHub Profile]", "[Your GitHub Profile]")  
  cleaned_text = cleaned_text.replace("[University Name]", "[Your University Name]")
  cleaned_text = cleaned_text.replace("[Graduation Year]", "[Your Graduation Year]")
  return cleaned_text

#frontend
st.title("Resume Generator")

name = st.text_input("Enter your name")
job_title = st.text_input("Enter your job title")

#submit button
if st.button("Generate Resume"):
  if name and job_title:
    resume = generate_resume(name, job_title)
    cleaned = clean_resume(resume)
    st.markdown("### Generated Resume")
    st.markdown(cleaned)
  else:
    st.warning("Please enter your name and job title")