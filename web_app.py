import streamlit as st
import pandas as pd
from fpdf import FPDF
import urllib.parse

# 1. Page Configuration
st.set_page_config(page_title="UPSA GPA Tracker", page_icon="🎓")

st.title("🎓 Carcious UPSA GPA Tracker")
st.write("Enter your course results below to calculate your cumulative GPA.")

# Initialize session state for grades
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=['Course', 'Score', 'Grade', 'GP'])

# 2. Grading Logic (The "Brain")
def get_grade_info(score):
    if score >= 80: return "A", 4.0
    elif score >= 75: return "B+", 3.5
    elif score >= 70: return "B", 3.0
    elif score >= 65: return "C+", 2.5
    elif score >= 60: return "C", 2.0
    elif score >= 55: return "D+", 1.5
    elif score >= 50: return "D", 1.0
    else: return "F", 0.0

# 3. Input Section
with st.form("grade_form", clear_on_submit=True):
    col1, col2 = st.columns([2, 1])
    with col1:
        course = st.text_input("Course Name (e.g., BCAD 103)")
    with col2:
        score = st.number_input("Score", min_value=0, max_value=100, step=1)
    
    submit = st.form_submit_button("Add to My Records")

if submit and course:
    grade, gp = get_grade_info(score)
    new_row = pd.DataFrame({'Course': [course], 'Score': [score], 'Grade': [grade], 'GP': [gp]})
    st.session_state.df = pd.concat([st.session_state.df, new_row], ignore_index=True)

# 4. Display Results
if not st.session_state.df.empty:
    st.table(st.session_state.df)
    cgpa = st.session_state.df['GP'].mean()
    
    # Degree Classification
    if cgpa >= 3.6: class_text = "First Class"
    elif cgpa >= 3.0: class_text = "Second Class Upper"
    elif cgpa >= 2.0: class_text = "Second Class Lower"
    elif cgpa >= 1.5: class_text = "Third Class"
    else: class_text = "Pass/Fail"

    st.metric("Current CGPA", f"{cgpa:.2f}", help=f"Your current standing: {class_text}")

    # 5. Target GPA Section
    st.divider()
    st.subheader("🎯 Target GPA Calculator")
    target_gpa = st.number_input("What is your Target CGPA?", min_value=0.0, max_value=4.0, value=3.5, step=0.1)
    remaining_courses = st.number_input("How many courses are remaining?", min_value=1, step=1)
    
    current_total_gp = st.session_state.df['GP'].sum()
    total_courses = len(st.session_state.df) + remaining_courses
    required_total_gp = (target_gpa * total_courses) - current_total_gp
    required_avg = required_total_gp / remaining_courses

    if required_avg > 4.0:
        st.error(f"To hit {target_gpa}, you'd need an average of {required_avg:.2f}. That is mathematically impossible!")
    elif required_avg <= 0:
        st.success(f"Goal met! Just keep passing to stay above {target_gpa}.")
    else:
        st.info(f"To reach {target_gpa}, you need an average GP of **{required_avg:.2f}** in your remaining courses.")

    # 6. PDF Generation
    def generate_pdf(df, final_gpa):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, txt="UPSA GPA Report", ln=True, align='C')
        pdf.set_font("Arial", size=12)
        pdf.ln(10)
        for i, row in df.iterrows():
            pdf.cell(200, 10, txt=f"{row['Course']}: Score {row['Score']} | Grade {row['Grade']} | GP {row['GP']}", ln=True)
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"Final CGPA: {final_gpa:.2f}", ln=True)
        return pdf.output(dest='S').encode('latin-1')

    pdf_data = generate_pdf(st.session_state.df, cgpa)
    st.download_button(label="📥 Download Results as PDF", data=pdf_data, file_name="UPSA_GPA_Report.pdf", mime="application/pdf")

else:
    st.info("No grades added yet. Start by entering a course above!")

# 7. WhatsApp Support Section (Restored)
st.divider()
st.subheader("🛠 Technical Support")
whatsapp_num = "233550242207"  # Your number
message = "Hi Carcious, I'm using your GPA Tracker and I need some help."
encoded_msg = urllib.parse.quote(message)
whatsapp_url = f"https://wa.me/{whatsapp_num}?text={encoded_msg}"

st.markdown(f'''
<a href="{whatsapp_url}" target="_blank">
    <button style="background-color:#25D366; color:white; border:none; padding:10px 20px; border-radius:5px; cursor:pointer;">
        💬 Contact Support on WhatsApp
    </button>
</a>
''', unsafe_content_type=True)