import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="UPSA GPA Tracker", page_icon="🎓")

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

# 3. Initialize Session Storage (This keeps data while the tab is open)
if 'grade_data' not in st.session_state:
    st.session_state.grade_data = []

# 4. The User Interface
st.title("🎓 Carcious UPSA GPA Tracker")
st.markdown("Enter your course results below to calculate your cumulative GPA.")

with st.form("grade_form", clear_on_submit=True):
    col1, col2 = st.columns([3, 1])
    with col1:
        subject = st.text_input("Course Name (e.g., BCAD 103)")
    with col2:
        score = st.number_input("Score", min_value=0, max_value=100, step=1)
    
    submit = st.form_submit_button("Add to My Records")

if submit and subject:
    letter, point = get_grade_info(score)
    st.session_state.grade_data.append({
        "Subject": subject,
        "Score": score,
        "Grade": letter,
        "Points": point
    })

# 5. Display the Table & Stats
if st.session_state.grade_data:
    df = pd.DataFrame(st.session_state.grade_data)
    
    # Show the table
    st.table(df)

    # Calculate Totals
    avg_score = df["Score"].mean()
    avg_gpa = df["Points"].mean()

    # Display Big Stats Boxes
    c1, c2 = st.columns(2)
    c1.metric("Cumulative GPA", f"{avg_gpa:.2f}")
    c2.metric("Average Score", f"{avg_score:.1f}%")

    if st.button("Clear All Data"):
        st.session_state.grade_data = []
        st.rerun()
else:
    st.info("No grades added yet. Start by entering a course above!")