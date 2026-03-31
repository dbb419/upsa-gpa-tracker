import streamlit as st
import pandas as pd

st.set_page_config(page_title="UPSA GPA Planner", page_icon="🎓")

def get_grade_info(score):
    if score >= 80: return "A", 4.0
    elif score >= 75: return "B+", 3.5
    elif score >= 70: return "B", 3.0
    elif score >= 65: return "C+", 2.5
    elif score >= 60: return "C", 2.0
    elif score >= 55: return "D+", 1.5
    elif score >= 50: return "D", 1.0
    else: return "F", 0.0

if 'grade_data' not in st.session_state:
    st.session_state.grade_data = []

st.title("🎓 Carcious UPSA GPA Planner")

# --- SECTION 1: ADD GRADES ---
with st.expander("➕ Add New Course Grade", expanded=True):
    with st.form("grade_form", clear_on_submit=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            subject = st.text_input("Course Name")
        with col2:
            score = st.number_input("Score (0-100)", 0, 100, 70)
        
        if st.form_submit_button("Save Course"):
            letter, point = get_grade_info(score)
            st.session_state.grade_data.append({"Subject": subject, "Score": score, "Grade": letter, "Points": point})
            st.rerun()

# --- SECTION 2: RESULTS TABLE ---
if st.session_state.grade_data:
    df = pd.DataFrame(st.session_state.grade_data)
    st.table(df)
    
    current_gpa = df["Points"].mean()
    num_courses = len(df)
    
    st.metric("Current GPA", f"{current_gpa:.2f}")

    # --- SECTION 3: TARGET GPA CALCULATOR (New!) ---
    st.divider()
    st.subheader("🎯 Target GPA Calculator")
    st.write("How many more courses are you taking, and what is your goal?")

    col_target, col_remaining = st.columns(2)
    with col_target:
        target_gpa = st.slider("Target GPA Goal", 1.0, 4.0, 3.5, 0.1)
    with col_remaining:
        remaining_courses = st.number_input("Remaining Courses", 1, 10, 1)

    # The Math: (Total Points Needed - Current Points) / Remaining Courses
    total_points_needed = target_gpa * (num_courses + remaining_courses)
    current_total_points = df["Points"].sum()
    points_needed_per_course = (total_points_needed - current_total_points) / remaining_courses

    if points_needed_per_course > 4.0:
        st.error(f"⚠️ To hit {target_gpa}, you'd need {points_needed_per_course:.2f} points per course. (Impossible! Try a lower target).")
    elif points_needed_per_course <= 0:
        st.success(f"✅ You've already secured a {target_gpa}! Just keep passing.")
    else:
        st.info(f"💡 To reach your goal of **{target_gpa}**, you need an average of **{points_needed_per_course:.2f} GP** in your next {remaining_courses} courses.")
        
    if st.button("Clear All"):
        st.session_state.grade_data = []
        st.rerun()
