import streamlit as st
import pandas as pd

st.set_page_config(page_title="UPSA GPA Planner", page_icon="🎓")

# --- OFFICIAL UPSA GRADING LOGIC ---
def get_grade_info(score):
    if score >= 80: return "A", "Excellent", 4.0
    elif score >= 75: return "B+", "Very Good", 3.5
    elif score >= 70: return "B", "Good", 3.0
    elif score >= 65: return "B-", "Above Average", 2.5
    elif score >= 60: return "C+", "Average", 2.0
    elif score >= 55: return "C", "Below Average", 1.5
    elif score >= 50: return "C-", "Marginal Pass", 1.0
    elif score >= 45: return "D", "Unsatisfactory", 0.5
    else: return "F", "Fail", 0.0

if 'grade_data' not in st.session_state:
    st.session_state.grade_data = []

st.title("🎓 Carcious UPSA GPA Planner")
st.caption("Official Grading System for Diploma & Degree Students")

# --- SECTION 1: ADD GRADES ---
with st.expander("➕ Add New Course Grade", expanded=True):
    with st.form("grade_form", clear_on_submit=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            subject = st.text_input("Course Name (e.g. BCAD 103)")
        with col2:
            score = st.number_input("Score (%)", 0, 100, 70)
        
        if st.form_submit_button("Save Course"):
            letter, interp, point = get_grade_info(score)
            st.session_state.grade_data.append({
                "Subject": subject, 
                "Score": score, 
                "Grade": letter, 
                "Interpretation": interp,
                "Points": point
            })
            st.rerun()

# --- SECTION 2: RESULTS & STANDING ---
if st.session_state.grade_data:
    df = pd.DataFrame(st.session_state.grade_data)
    st.table(df)
    
    current_gpa = df["Points"].mean()
    num_courses = len(df)
    
    col_gpa, col_class = st.columns(2)
    with col_gpa:
        st.metric("Current GPA", f"{current_gpa:.2f}")
    
    with col_class:
        # Graduation Class Logic from the Flyer
        if current_gpa >= 3.6: standing = "1st Class"
        elif current_gpa >= 3.0: standing = "2nd Class Upper"
        elif current_gpa >= 2.5: standing = "2nd Class Lower"
        elif current_gpa >= 2.0: standing = "3rd Class"
        elif current_gpa >= 1.0: standing = "Pass"
        else: standing = "Fail"
        st.metric("Current Standing", standing)

    # --- SECTION 3: TARGET GPA CALCULATOR ---
    st.divider()
    st.subheader("🎯 Target GPA Goal")
    target_gpa = st.slider("What is your goal GPA?", 1.0, 4.0, 3.5, 0.1)
    remaining_courses = st.number_input("How many courses left this semester?", 1, 10, 1)

    total_points_needed = target_gpa * (num_courses + remaining_courses)
    current_total_points = df["Points"].sum()
    points_needed_per_course = (total_points_needed - current_total_points) / remaining_courses

    if points_needed_per_course > 4.0:
        st.error(f"⚠️ To hit {target_gpa}, you need {points_needed_per_course:.2f} per course. That's above an A!")
    elif points_needed_per_course <= 0:
        st.success(f"✅ You've already secured a {target_gpa}!")
    else:
        st.info(f"💡 To reach **{target_gpa}**, aim for an average of **{points_needed_per_course:.2f} GP** in your next {remaining_courses} courses.")
        
    if st.button("Clear All Data"):
        st.session_state.grade_data = []
        st.rerun()
