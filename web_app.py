import streamlit as st
import pandas as pd
from fpdf import FPDF
import urllib.parse

# 1. Page Configuration
st.set_page_config(page_title="UPSA GPA Tracker", page_icon="🎓", layout="centered")

# Custom CSS for a cleaner look
st.markdown("""
    <style>
    .main { text-align: center; }
    .stMetric { background-color: #f0f2f6; padding: 15px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎓 Carcious UPSA GPA Tracker")
st.write("Calculate your CGPA and plan your academic goals based on official UPSA grading.")

# Initialize session state for grades
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=['Course', 'Score', 'Grade', 'GP'])

# 2. Grading Logic (Official UPSA Scale)
def calculate_grade(score_input):
    if score_input >= 80: return "A", 4.0
    elif score_input >= 75: return "B+", 3.5
    elif score_input >= 70: return "B", 3.0
    elif score_input >= 65: return "C+", 2.5
    elif score_input >= 60: return "C", 2.0
    elif score_input >= 55: return "D+", 1.5
    elif score_input >= 50: return "D", 1.0
    else: return "F", 0.0

# 3. Input Form
with st.form("grade_entry_form", clear_on_submit=True):
    col1, col2 = st.columns([3, 1])
    with col1:
        course_name = st.text_input("Course Name", placeholder="e.g. BCAD 103")
    with col2:
        score_val = st.number_input("Score", min_value=0, max_value=100, step=1)
    
    submit_btn = st.form_submit_button("Add Course to Records")

# Processing Input
if submit_btn and course_name:
    grade_letter, grade_point = calculate_grade(score_val)
    new_entry = pd.DataFrame({
        'Course': [course_name.upper()], 
        'Score': [score_val], 
        'Grade': [grade_letter], 
        'GP': [grade_point]
    })
    st.session_state.df = pd.concat([st.session_state.df, new_entry], ignore_index=True)

# 4. Results Display
if not st.session_state.df.empty:
    st.subheader("📊 Your Academic Records")
    st.table(st.session_state.df)
    
    # CGPA Calculation
    current_cgpa = st.session_state.df['GP'].mean()
    
    # Classification Logic
    if current_cgpa >= 3.6: standing = "First Class"
    elif current_cgpa >= 3.0: standing = "Second Class Upper"
    elif current_cgpa >= 2.0: standing = "Second Class Lower"
    elif current_cgpa >= 1.5: standing = "Third Class"
    else: standing = "Pass/Fail"

    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.metric("Current CGPA", f"{current_cgpa:.2f}")
    with col_m2:
        st.metric("Standing", standing)

    # 5. Target GPA Calculator
    st.divider()
    st.subheader("🎯 Target GPA Planner")
    t_col1, t_col2 = st.columns(2)
    with t_col1:
        target_val = st.number_input("Desired CGPA", min_value=0.0, max_value=4.0, value=3.5, step=0.1)
    with t_col2:
        remaining = st.number_input("Remaining Courses", min_value=1, step=1)
    
    current_total_points = st.session_state.df['GP'].sum()
    total_courses = len(st.session_state.df) + remaining
    needed_gp = (target_val * total_courses) - current_total_points
    required_avg = needed_gp / remaining

    if required_avg > 4.0:
        st.error(f"Mathematically impossible! You need a **{required_avg:.2f}** average (Max is 4.0).")
    elif required_avg <= 0:
        st.success("Target already secured! Just maintain your passing grades.")
    else:
        st.info(f"To reach {target_val}, you need an average GP of **{required_avg:.2f}** in remaining courses.")

    # 6. PDF Generation (Fixed for Phone/Browser Compatibility)
    def create_pdf(data_frame, cgpa_val):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, txt="UPSA GPA Report", ln=True, align='C')
        pdf.ln(10)
        pdf.set_font("Arial", size=12)
        for i, row in data_frame.iterrows():
            pdf.cell(200, 10, txt=f"{row['Course']}: Score {row['Score']} | Grade {row['Grade']} | GP {row['GP']}", ln=True)
        pdf.ln(10)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, txt=f"Final CGPA: {cgpa_val:.2f}", ln=True)
        return pdf.output() # No .encode needed in newer fpdf versions

    # Download Button
    pdf_output = create_pdf(st.session_state.df, current_cgpa)
    st.download_button(
        label="📥 Download My Results as PDF", 
        data=pdf_output, 
        file_name="UPSA_GPA_Report.pdf", 
        mime="application/pdf"
    )

else:
    st.info("Your record is currently empty. Use the form above to add your first course score!")

# 7. WhatsApp Support
st.divider()
whatsapp_number = "233553754858"
support_msg = urllib.parse.quote("Hi Carcious, I need help with the GPA Tracker app.")
wa_link = f"https://wa.me/{whatsapp_number}?text={support_msg}"

st.markdown(f'''
    <div style="text-align: center;">
        <p>Developed by Carcious Osei</p>
        <a href="{wa_link}" target="_blank">
            <button style="background-color:#25D366; color:white; border:none; padding:12px 24px; border-radius:8px; cursor:pointer; font-weight:bold;">
                💬 Contact Tech Support
            </button>
        </a>
    </div>
    ''', unsafe_allow_html=True)