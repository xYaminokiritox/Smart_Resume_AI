import google.generativeai as genai
import streamlit as st
from fpdf import FPDF

genai.configure(api_key="AIzaSyCNgFEyq3K1pLud_3M5EUNYtIut2YKSNBw")

def generate_resume(name, job_title):
    model = genai.GenerativeModel("gemini-2.0-flash")
    
    context = f"""
    fname: {name}
    job_title: {job_title}
    Write a professional ATS-friendly resume based on the above data.
    """

    chat_session = model.start_chat(history=[])

    response = chat_session.send_message(context)
    
    text = response.text
    return text

def clean_resume_text(text):
    text = text.replace("[Add Email Address]", "[Your Email Address]")
    text = text.replace("[Add Phone Number]", "[Your Phone Number]")
    text = text.replace("[Add LinkedIn Profile URL (optional)]", "[Your LinkedIn URL (optional)]")
    text = text.replace("[University Name]", "[Your University Name]")
    text = text.replace("[Graduation Year]", "[Your Graduation Year]")
    return text

# ✅ Function to generate PDF from text
def generate_pdf(name, job_title, content):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Add content to PDF
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, txt=f"Resume for {name}", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(200, 10, txt=content)

    # Save the PDF
    file_path = f"{name.replace(' ', '_')}_Resume.pdf"
    pdf.output(file_path)
    return file_path

# ✅ Streamlit UI
st.title("🚀 AI Resume Generator (Powered by Gemini 2.0)")

# Input fields
name = st.text_input("Enter your Name")
job_title = st.text_input("Enter your Job Title")

# Submit button
if st.button("Generate Resume"):
    if name and job_title:
        # Generate the resume using Gemini API
        resume = generate_resume(name, job_title)
        cleaned_resume = clean_resume_text(resume)
        
        # Display the generated resume
        st.markdown("## 🎓 Generated Resume")
        st.markdown(cleaned_resume)
        
        # ✅ Generate PDF button
        pdf_path = generate_pdf(name, job_title, cleaned_resume)
        with open(pdf_path, "rb") as pdf_file:
            st.download_button(
                label="📄 Download Resume as PDF",
                data=pdf_file,
                file_name=f"{name.replace(' ', '_')}_Resume.pdf",
                mime="application/pdf"
            )
    else:
        st.warning("⚠️ Please enter both your Name and Job Title.")
