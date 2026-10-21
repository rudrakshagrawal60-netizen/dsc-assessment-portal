import streamlit as st
import datetime
import random

# Page Configuration
st.set_page_config(
    page_title="DSC | Digital Student Certification & Assessment Portal", 
    page_icon="🎓", 
    layout="wide"
)

# Professional Custom Styling & CSS for Sidebar & Cards
st.markdown("""
    <style>
    .hero-box { 
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364); 
        padding: 40px; 
        border-radius: 15px; 
        color: white; 
        text-align: center; 
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .captcha-box {
        background-color: #e9ecef;
        color: #0056b3;
        font-size: 26px;
        font-weight: bold;
        letter-spacing: 8px;
        text-align: center;
        padding: 12px;
        border-radius: 8px;
        border: 2px dashed #0056b3;
        margin-bottom: 12px;
    }
    .stButton>button {
        background-color: #0056b3;
        color: white;
        border-radius: 8px;
        font-weight: bold;
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# Session State Initialization
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_role" not in st.session_state:
    st.session_state.user_role = ""
if "username" not in st.session_state:
    st.session_state.username = ""
if "identifier" not in st.session_state:
    st.session_state.identifier = ""

# Persistent Captcha Generation in Session State
if "captcha_val" not in st.session_state:
    st.session_state.captcha_val = str(random.randint(1000, 9999))

def main():
    if not st.session_state.logged_in:
        show_landing_page()
    else:
        if st.session_state.user_role == "Staff / Admin":
            show_staff_dashboard()
        else:
            show_student_dashboard()

def show_landing_page():
    # Top Navigation Bar
    col1, col2, col3 = st.columns([2, 6, 2])
    with col1:
        st.markdown("### 🎓 **DSC**")
    with col2:
        st.markdown("<p style='text-align: center; color: #555; font-size: 14px; font-weight: 600;'>AI PROCTOR | MONITORING | FEATURES | SERVICES</p>", unsafe_allow_html=True)
    with col3:
        if st.button("Login Portal", type="primary"):
            st.session_state.show_login = True

    st.markdown("---")

    # Hero Section
    st.markdown(f"""
        <div class="hero-box">
            <h1>DSC Assessment & Certification Platform</h1>
            <p style="font-size: 16px; margin-top: 10px; color: #d0d7de;">An Advanced Online Examination System with Secure Captcha & AI Proctoring</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")

    # Unified Login Section with Boxed Captcha
    if st.session_state.get("show_login", True):
        st.markdown("<h2 style='text-align: center; margin-top: 20px;'>🔐 Secure DSC Login Portal</h2>", unsafe_allow_html=True)
        
        col_f1, col_f2, col_f3 = st.columns([1, 2, 1])
        with col_f2:
            with st.form("unified_login_form"):
                role_select = st.selectbox("Select Login Role", ["Regular Student", "Staff / Admin"])
                name_input = st.text_input("Full Name")
                id_input = st.text_input("Roll Number / Employee ID")
                password_input = st.text_input("Password", type="password")
                
                # Display Captcha inside a clean styled Box
                st.markdown("<p style='margin-bottom: 5px; font-weight: bold;'>Verification Captcha Code:</p>", unsafe_allow_html=True)
                st.markdown(f"<div class='captcha-box'>{st.session_state.captcha_val}</div>", unsafe_allow_html=True)
                
                captcha_input = st.text_input("Enter the 4-digit code shown above")
                
                col_b1, col_b2 = st.columns(2)
                with col_b1:
                    submit_login = st.form_submit_button("Login")
                with col_b2:
                    refresh_captcha = st.form_submit_button("New Captcha")
                
                if refresh_captcha:
                    st.session_state.captcha_val = str(random.randint(1000, 9999))
                    st.rerun()

                if submit_login:
                    if captcha_input.strip() == st.session_state.captcha_val:
                        if name_input.strip() and id_input.strip():
                            st.session_state.logged_in = True
                            st.session_state.user_role = role_select
                            st.session_state.username = name_input.upper()
                            st.session_state.identifier = id_input.strip()
                            st.success("Login Successful!")
                            st.rerun()
                        else:
                            st.error("Kripya apna Name aur ID dono enter karein.")
                    else:
                        st.error("Galat Captcha number! Sahi number enter karein.")
                        st.session_state.captcha_val = str(random.randint(1000, 9999))

def show_student_dashboard():
    # Sidebar matching your exact screenshot menu
    st.sidebar.image("https://img.icons8.com/color/96/student-male.png", width=70)
    st.sidebar.markdown(f"### **{st.session_state.username}**")
    st.sidebar.markdown(f"<p style='color: gray; font-size: 12px;'>ID: {st.session_state.identifier} | Student</p>", unsafe_allow_html=True)
    st.sidebar.markdown("---")
    
    menu = st.sidebar.radio("Navigation", [
        "📌 Main Dashboard", 
        "👤 Academic Dashboard", 
        "📄 Practice Dashboard", 
        "🤖 Interview", 
        "🗄️ Database/SQL", 
        "🌐 Web Tech",
        "✍️ Essay Writing",
        "😀 Face Registration",
        "❓ Help Desk"
    ])
    
    if st.sidebar.button("Logout 🔴"):
        st.session_state.logged_in = False
        st.session_state.captcha_val = str(random.randint(1000, 9999))
        st.rerun()

    col1, col2 = st.columns([7, 3])
    with col1:
        st.markdown(f"### Student Dashboard — Welcome, **{st.session_state.username}**")
        st.markdown(f"<p style='color: gray;'>Roll Number / ID: <b>{st.session_state.identifier}</b></p>", unsafe_allow_html=True)
    with col2:
        current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
        st.markdown(f"⏰ **{current_time}** | 🟢 Secure Proctor Active")

    st.markdown("---")

    if menu == "📌 Main Dashboard":
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Completed Exams", "0 of 0")
        c2.metric("Needs Attention", "0 Active")
        c3.metric("Upcoming Tests", "1 Scheduled")
        c4.metric("Practice Progress", "0.0%")

        st.markdown("### 📌 Your Exam Journey & Overview")
        st.info("Aapke paas abhi koi urgent action required nahi hai. Sabhi scheduled exams time par yahan show honge.")

        st.markdown("---")
        st.subheader("📜 Recent Activity History")
        st.markdown("""
        * 📄 **Assessment : Full Stack & DSA Evaluation** — *Completed Successfully*
        * 💻 **Coding Lab : Array Manipulation** — *Passed all test cases*
        """)

    elif menu == "👤 Academic Dashboard":
        st.subheader("📚 Academic Examinations & Quizzes")
        st.info("No active examinations are currently live for your ID.")

    elif menu == "📄 Practice Dashboard":
        st.subheader("🎯 Practice Lab & Quiz Progress")
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Quiz Finished", "1")
            st.metric("Active Sessions", "0")
        with c2:
            st.metric("Waiting Quizzes", "4568")
            st.metric("Overall Completion", "0.0%")
        st.success("Your remaining quizzes are waiting — check availability and filters.")

    elif menu == "🤖 Interview":
        st.subheader("🎙️ AI Interview Practice & Self Introduction")
        st.write("Turn every interview into a smarter practice session. Prepare with AI analytics.")
        if st.button("Start AI Powered Analysis"):
            st.balloons()
            st.success("Voice sample analyzed! Confidence Score: 88/100, Fluency: Excellent.")

    elif menu == "🗄️ Database/SQL":
        st.subheader("🗄️ Database & SQL Query Editor")
        query = st.text_area("SQL Query", value=f"SELECT * FROM student_records WHERE id = '{st.session_state.identifier}';")
        if st.button("Execute SQL Query"):
            st.code("Query executed successfully. 1 row returned.", language="sql")

    elif menu == "🌐 Web Tech":
        st.subheader("🌐 Web Tech HTML/CSS Compiler")
        html_code = st.text_area("HTML Code", value="<h2>Welcome to DSC Portal</h2><p>Live Preview Active.</p>")
        st.markdown("#### Live Preview:")
        st.components.v1.html(html_code, height=120)

    elif menu == "✍️ Essay Writing":
        st.subheader("✍️ AI Essay Evaluation")
        st.text_area("Write your essay here:", height=150)
        if st.button("Evaluate Essay"):
            st.success("Grammar & Coherence Score: 92/100")

    elif menu == "😀 Face Registration":
        st.subheader("👤 AI Proctoring Face Recognition")
        st.success(f"Face biometrics verified and linked successfully with ID: {st.session_state.identifier}")

    elif menu == "❓ Help Desk":
        st.subheader("🛠️ Technical Exam Help Desk")
        st.metric("Helpline Number", "9568536853")

def show_staff_dashboard():
    st.sidebar.image("https://img.icons8.com/color/96/administrator-male.png", width=70)
    st.sidebar.markdown(f"### **Staff: {st.session_state.username}**")
    st.sidebar.markdown(f"<p style='color: gray; font-size: 12px;'>ID: {st.session_state.identifier} | Teacher</p>", unsafe_allow_html=True)
    st.sidebar.markdown("---")
    
    staff_menu = st.sidebar.radio("Teacher Panel", [
        "📊 Attendance Management",
        "📝 Quiz & Test Creator",
        "💻 Code Challenges Management"
    ])
    
    if st.sidebar.button("Logout 🔴"):
        st.session_state.logged_in = False
        st.session_state.captcha_val = str(random.randint(1000, 9999))
        st.rerun()

    st.markdown(f"### 👨‍🏫 Teacher & Staff Control Center — **{st.session_state.username}**")
    st.markdown("---")

    if staff_menu == "📊 Attendance Management":
        st.subheader("📋 Student Attendance Management & Tracking")
        st.write("Yahan se aap students ki live exam attendance check, track aur export kar sakte hain.")
        st.selectbox("Select Section / Batch", ["Section AJ", "Section AW", "CSE Batch A"])
        if st.button("Export Attendance Report"):
            st.success("Attendance sheet successfully exported!")

    elif staff_menu == "📝 Quiz & Test Creator":
        st.subheader("✍️ Quiz & Assessment Creator")
        quiz_title = st.text_input("Quiz Title")
        q_count = st.number_input("Number of Questions", min_value=1, max_value=50, value=5)
        st.text_area("Enter Quiz Question Statement & Options")
        if st.button("Publish Quiz Live"):
            st.success("Quiz successfully published for students!")

    elif staff_menu == "💻 Code Challenges Management":
        st.subheader("⚡ Coding Challenges & Test Cases Manager")
        problem_title = st.text_input("Problem Title")
        supported_lang = st.multiselect("Allowed Languages", ["Python", "Java", "C++", "C"], default=["Python", "Java"])
        st.text_area("Problem Statement & Description")
        st.text_area("Hidden Test Cases")
        if st.button("Deploy Coding Challenge"):
            st.success("Coding challenge successfully deployed to student labs!")

if __name__ == "__main__":
    main()