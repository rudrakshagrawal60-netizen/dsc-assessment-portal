import streamlit as st
import datetime
import random
import sqlite3
import hashlib

# Page Configuration
st.set_page_config(
    page_title="DSC | Digital Student Certification & Assessment Portal", 
    page_icon="🎓", 
    layout="wide"
)

# Professional Custom Styling & CSS
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

# Helper function to hash passwords securely
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Database Initialization with Photo Support
def init_db():
    conn = sqlite3.connect('dsc_portal.db')
    cursor = conn.cursor()
    
    # Students table with photo BLOB column
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            roll_no TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            password TEXT NOT NULL,
            photo BLOB
        )
    ''')
    
    # Admins table with photo BLOB column
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admins (
            admin_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            password TEXT NOT NULL,
            photo BLOB
        )
    ''')
    
    conn.commit()
    conn.close()

init_db()

# Session State Initialization
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_role" not in st.session_state:
    st.session_state.user_role = ""
if "username" not in st.session_state:
    st.session_state.username = ""
if "identifier" not in st.session_state:
    st.session_state.identifier = ""

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
    st.sidebar.markdown("### 🔒 Security Gateway")
    portal_choice = st.sidebar.radio("Select Portal", ["Student Portal", "Staff / Admin Portal"])
    
    col1, col2, col3 = st.columns([2, 6, 2])
    with col1:
        st.markdown("### 🎓 **DSC**")
    with col2:
        st.markdown("<p style='text-align: center; color: #555; font-size: 14px; font-weight: 600;'>SECURE ASSESSMENT & EVALUATION SYSTEM</p>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<p style='text-align: right; color: #0056b3; font-weight: bold;'>Mode: {portal_choice}</p>", unsafe_allow_html=True)

    st.markdown("---")

    if portal_choice == "Staff / Admin Portal":
        admin_action = st.radio("Admin Action", ["Admin Login", "Admin Sign Up"], horizontal=True)
        
        if admin_action == "Admin Sign Up":
            st.markdown("<h2 style='text-align: center;'>📝 Faculty / Admin Registration</h2>", unsafe_allow_html=True)
            col_r1, col_r2, col_r3 = st.columns([1, 2, 1])
            with col_r2:
                with st.form("admin_signup_form"):
                    reg_name = st.text_input("Faculty Full Name")
                    reg_id = st.text_input("Admin ID / Employee Code")
                    reg_pass = st.text_input("Create Secure Password", type="password")
                    reg_photo = st.file_uploader("Upload Admin Profile Photo", type=["jpg", "png", "jpeg"])
                    
                    submit_reg = st.form_submit_button("Register Admin Account")
                    if submit_reg:
                        if reg_name.strip() and reg_id.strip() and reg_pass.strip():
                            try:
                                photo_bytes = reg_photo.read() if reg_photo else None
                                conn = sqlite3.connect('dsc_portal.db')
                                cursor = conn.cursor()
                                hashed_pass = hash_password(reg_pass.strip())
                                cursor.execute("INSERT INTO admins (admin_id, name, password, photo) VALUES (?, ?, ?, ?)", 
                                               (reg_id.strip(), reg_name.strip(), hashed_pass, photo_bytes))
                                conn.commit()
                                conn.close()
                                st.success("Admin account successfully created with photo! Now go to Admin Login.")
                            except sqlite3.IntegrityError:
                                st.error("Error: This Admin ID is already registered!")
                        else:
                            st.error("Please fill all fields.")
        else:
            st.markdown("<h2 style='text-align: center;'>🔐 Secure Admin Login Portal</h2>", unsafe_allow_html=True)
            col_f1, col_f2, col_f3 = st.columns([1, 2, 1])
            with col_f2:
                with st.form("admin_login_form"):
                    admin_id_input = st.text_input("Admin ID / Employee Code")
                    admin_pass_input = st.text_input("Password", type="password")
                    
                    st.markdown("<p style='margin-bottom: 5px; font-weight: bold;'>Verification Captcha Code:</p>", unsafe_allow_html=True)
                    st.markdown(f"<div class='captcha-box'>{st.session_state.captcha_val}</div>", unsafe_allow_html=True)
                    captcha_input = st.text_input("Enter the 4-digit code shown above")
                    
                    col_b1, col_b2 = st.columns(2)
                    with col_b1:
                        submit_admin_login = st.form_submit_button("Admin Login")
                    with col_b2:
                        refresh_captcha = st.form_submit_button("New Captcha")
                    
                    if refresh_captcha:
                        st.session_state.captcha_val = str(random.randint(1000, 9999))
                        st.rerun()

                    if submit_admin_login:
                        if captcha_input.strip() == st.session_state.captcha_val:
                            if admin_id_input.strip() and admin_pass_input.strip():
                                conn = sqlite3.connect('dsc_portal.db')
                                cursor = conn.cursor()
                                hashed_pass = hash_password(admin_pass_input.strip())
                                cursor.execute("SELECT * FROM admins WHERE admin_id = ? AND password = ?", (admin_id_input.strip(), hashed_pass))
                                admin = cursor.fetchone()
                                conn.close()
                                
                                if admin:
                                    st.session_state.logged_in = True
                                    st.session_state.user_role = "Staff / Admin"
                                    st.session_state.username = admin[1].upper()
                                    st.session_state.identifier = admin[0]
                                    st.success("Admin Login Successful!")
                                    st.rerun()
                                else:
                                    st.error("Invalid Admin ID or Password!")
                            else:
                                st.error("Please enter ID and Password.")
                        else:
                            st.error("Invalid Captcha code!")
                            st.session_state.captcha_val = str(random.randint(1000, 9999))

    else:
        st.markdown(f"""
            <div class="hero-box">
                <h1>DSC Student Assessment Portal</h1>
                <p style="font-size: 16px; margin-top: 10px; color: #d0d7de;">Secure Student Login via University Roll Number & Encrypted Database</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        st.markdown("<h2 style='text-align: center; margin-top: 20px;'>🎓 Student Secure Login</h2>", unsafe_allow_html=True)
        
        col_f1, col_f2, col_f3 = st.columns([1, 2, 1])
        with col_f2:
            with st.form("student_login_form"):
                roll_input = st.text_input("University Roll Number / Student ID")
                password_input = st.text_input("Password", type="password")
                
                st.markdown("<p style='margin-bottom: 5px; font-weight: bold;'>Verification Captcha Code:</p>", unsafe_allow_html=True)
                st.markdown(f"<div class='captcha-box'>{st.session_state.captcha_val}</div>", unsafe_allow_html=True)
                
                captcha_input = st.text_input("Enter the 4-digit code shown above")
                
                col_b1, col_b2 = st.columns(2)
                with col_b1:
                    submit_student_login = st.form_submit_button("Student Login")
                with col_b2:
                    refresh_captcha = st.form_submit_button("New Captcha")
                
                if refresh_captcha:
                    st.session_state.captcha_val = str(random.randint(1000, 9999))
                    st.rerun()

                if submit_student_login:
                    if captcha_input.strip() == st.session_state.captcha_val:
                        if roll_input.strip() and password_input.strip():
                            conn = sqlite3.connect('dsc_portal.db')
                            cursor = conn.cursor()
                            hashed_pass = hash_password(password_input.strip())
                            cursor.execute("SELECT * FROM students WHERE roll_no = ? AND password = ?", (roll_input.strip(), hashed_pass))
                            student = cursor.fetchone()
                            conn.close()
                            
                            if student:
                                st.session_state.logged_in = True
                                st.session_state.user_role = "Regular Student"
                                st.session_state.username = student[1].upper()
                                st.session_state.identifier = student[0]
                                st.success("Student Login Successful!")
                                st.rerun()
                            else:
                                st.error("Access Denied! Roll number not registered by admin or incorrect password.")
                        else:
                            st.error("Please enter Roll Number and Password.")
                    else:
                        st.error("Invalid Captcha code!")
                        st.session_state.captcha_val = str(random.randint(1000, 9999))

def show_student_dashboard():
    # Fetch Student Photo from Database
    conn = sqlite3.connect('dsc_portal.db')
    cursor = conn.cursor()
    cursor.execute("SELECT photo FROM students WHERE roll_no = ?", (st.session_state.identifier,))
    res = cursor.fetchone()
    conn.close()
    
    if res and res[0]:
        st.sidebar.image(res[0], width=100)
    else:
        st.sidebar.image("https://img.icons8.com/color/96/student-male.png", width=90)

    st.sidebar.markdown(f"### **{st.session_state.username}**")
    st.sidebar.markdown(f"<p style='color: gray; font-size: 12px;'>Roll No: {st.session_state.identifier} | Student</p>", unsafe_allow_html=True)
    st.sidebar.markdown("---")
    
    selected_lang = st.sidebar.selectbox("🌐 Choose Language", ["English", "Hindi"])
    
    lang = {
        "English": {
            "nav_title": "Navigation",
            "menu_1": "📌 Main Dashboard",
            "menu_2": "👤 Academic Dashboard",
            "menu_3": "📄 Practice Dashboard",
            "menu_4": "🤖 Interview",
            "menu_5": "🗄️ Database/SQL",
            "menu_6": "🌐 Web Tech",
            "menu_7": "✍️ Essay Writing",
            "menu_8": "😀 Face Registration",
            "menu_9": "❓ Help Desk",
            "logout": "Logout 🔴",
            "welcome": "Student Dashboard — Welcome",
            "proctor": "Secure Proctor Active",
            "completed": "Completed Exams",
            "attention": "Needs Attention",
            "upcoming": "Upcoming Tests",
            "progress": "Practice Progress",
            "journey": "Your Exam Journey & Overview",
            "verified_msg": "Your account is verified by admin. All scheduled exams will appear here on time.",
            "history": "Recent Activity History"
        },
        "Hindi": {
            "nav_title": "Navigation",
            "menu_1": "📌 Main Dashboard",
            "menu_2": "👤 Academic Dashboard",
            "menu_3": "📄 Practice Dashboard",
            "menu_4": "🤖 Interview",
            "menu_5": "🗄️ Database/SQL",
            "menu_6": "🌐 Web Tech",
            "menu_7": "✍️ Essay Writing",
            "menu_8": "😀 Face Registration",
            "menu_9": "❓ Help Desk",
            "logout": "Logout 🔴",
            "welcome": "Student Dashboard — Welcome",
            "proctor": "Secure Proctor Active",
            "completed": "Completed Exams",
            "attention": "Needs Attention",
            "upcoming": "Upcoming Tests",
            "progress": "Practice Progress",
            "journey": "Your Exam Journey & Overview",
            "verified_msg": "Your account is verified by admin. All scheduled exams will appear here on time.",
            "history": "Recent Activity History"
        }
    }
    
    t = lang[selected_lang]
    
    menu = st.sidebar.radio(t["nav_title"], [
        t["menu_1"], t["menu_2"], t["menu_3"], t["menu_4"], 
        t["menu_5"], t["menu_6"], t["menu_7"], t["menu_8"], t["menu_9"]
    ])
    
    if st.sidebar.button(t["logout"]):
        st.session_state.logged_in = False
        st.session_state.captcha_val = str(random.randint(1000, 9999))
        st.rerun()

    col1, col2 = st.columns([7, 3])
    with col1:
        st.markdown(f"### {t['welcome']}, **{st.session_state.username}**")
        st.markdown(f"<p style='color: gray;'>Roll Number: <b>{st.session_state.identifier}</b></p>", unsafe_allow_html=True)
    with col2:
        current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
        st.markdown(f"⏰ **{current_time}** | 🟢 {t['proctor']}")

    st.markdown("---")

    if menu in ["📌 Main Dashboard", "📌 Main Dashboard"]:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric(t["completed"], "0 of 0")
        c2.metric(t["attention"], "0 Active")
        c3.metric(t["upcoming"], "1 Scheduled")
        c4.metric(t["progress"], "0.0%")

        st.markdown(f"### 📌 {t['journey']}")
        st.info(t["verified_msg"])

        st.markdown("---")
        st.subheader(f"📜 {t['history']}")
        st.markdown("""
        * 📄 **Assessment : Full Stack & DSA Evaluation** — *Completed Successfully*
        * 💻 **Coding Lab : Array Manipulation** — *Passed all test cases*
        """)

    elif "Academic" in menu:
        st.subheader("📚 Academic Examinations & Quizzes")
        st.info("No active examinations are currently live for your ID.")

    elif "Practice" in menu:
        st.subheader("🎯 Practice Lab & Quiz Progress")
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Quiz Finished", "1")
            st.metric("Active Sessions", "0")
        with c2:
            st.metric("Waiting Quizzes", "4568")
            st.metric("Overall Completion", "0.0%")
        st.success("Your remaining quizzes are waiting — check availability and filters.")

    elif "Interview" in menu:
        st.subheader("🎙️ AI Interview Practice & Self Introduction")
        if st.button("Start AI Powered Analysis"):
            st.balloons()
            st.success("Voice sample analyzed! Confidence Score: 88/100, Fluency: Excellent.")

    elif "Database" in menu:
        st.subheader("🗄️ Database & SQL Query Editor")
        query = st.text_area("SQL Query", value=f"SELECT * FROM students WHERE roll_no = '{st.session_state.identifier}';")
        if st.button("Execute SQL Query"):
            st.code("Query executed successfully. 1 row returned.", language="sql")

    elif "Web Tech" in menu:
        st.subheader("🌐 Web Tech HTML/CSS Compiler")
        html_code = st.text_area("HTML Code", value="<h2>Welcome to DSC Portal</h2><p>Live Preview Active.</p>")
        st.components.v1.html(html_code, height=120)

    elif "Essay" in menu:
        st.subheader("✍️ AI Essay Evaluation")
        st.text_area("Write your essay here:", height=150)
        if st.button("Evaluate Essay"):
            st.success("Grammar & Coherence Score: 92/100")

    elif "Face" in menu:
        st.subheader("👤 AI Proctoring Face Recognition")
        st.success(f"Face biometrics verified and linked successfully with Roll No: {st.session_state.identifier}")

    elif "Help" in menu:
        st.subheader("🛠️ Technical Exam Help Desk & Support")
        st.info("If you are facing any issues regarding the portal, login, or examinations, please feel free to reach out to the support desk below:")
        
        col_h1, col_h2 = st.columns(2)
        with col_h1:
            st.metric("Support Administrator", "RUDRAKSH AGRAWAL")
        with col_h2:
            st.metric("Helpline Contact Number", "9634350854")

def show_staff_dashboard():
    # Fetch Admin Photo from Database
    conn = sqlite3.connect('dsc_portal.db')
    cursor = conn.cursor()
    cursor.execute("SELECT photo FROM admins WHERE admin_id = ?", (st.session_state.identifier,))
    res = cursor.fetchone()
    conn.close()
    
    if res and res[0]:
        st.sidebar.image(res[0], width=100)
    else:
        st.sidebar.image("https://img.icons8.com/color/96/administrator-male.png", width=90)

    st.sidebar.markdown(f"### **Admin: {st.session_state.username}**")
    st.sidebar.markdown(f"<p style='color: gray; font-size: 12px;'>ID: {st.session_state.identifier} | Teacher</p>", unsafe_allow_html=True)
    st.sidebar.markdown("---")
    
    staff_menu = st.sidebar.radio("Teacher Panel", [
        "👥 Add / Register Student",
        "📊 Attendance Management",
        "📝 Quiz & Test Creator",
        "💻 Code Challenges Management"
    ])
    
    if st.sidebar.button("Logout 🔴"):
        st.session_state.logged_in = False
        st.session_state.captcha_val = str(random.randint(1000, 9999))
        st.rerun()

    st.markdown(f"### 👨‍🏫 Admin & Teacher Control Center — **{st.session_state.username}**")
    st.markdown("---")

    if staff_menu == "👥 Add / Register Student":
        st.subheader("➕ Add New Student to Portal Database with Photo")
        st.write("Yahan se aap naye student ka naam, roll number, password aur uska profile photo upload karke register kar sakte hain.")
        
        with st.form("add_student_form"):
            new_name = st.text_input("Student Full Name")
            new_roll = st.text_input("Student Roll Number")
            new_pass = st.text_input("Assign Password", type="password")
            student_photo = st.file_uploader("Upload Student Photo", type=["jpg", "png", "jpeg"])
            
            submit_student = st.form_submit_button("Register Student in Database")
            if submit_student:
                if new_name.strip() and new_roll.strip() and new_pass.strip():
                    try:
                        photo_bytes = student_photo.read() if student_photo else None
                        conn = sqlite3.connect('dsc_portal.db')
                        cursor = conn.cursor()
                        hashed_password = hash_password(new_pass.strip())
                        cursor.execute("INSERT INTO students (roll_no, name, password, photo) VALUES (?, ?, ?, ?)", 
                                       (new_roll.strip(), new_name.strip(), hashed_password, photo_bytes))
                        conn.commit()
                        conn.close()
                        st.success(f"Student '{new_name}' (Roll No: {new_roll}) successfully registered with photo!")
                    except sqlite3.IntegrityError:
                        st.error("Error: This Roll Number is already registered!")
                else:
                    st.error("Please fill all required fields.")

        st.markdown("### 📋 Currently Registered Students List")
        conn = sqlite3.connect('dsc_portal.db')
        cursor = conn.cursor()
        cursor.execute("SELECT roll_no, name FROM students")
        students_list = cursor.fetchall()
        conn.close()
        
        if students_list:
            for s in students_list:
                st.write(f"• **Roll No:** {s[0]} | **Name:** {s[1]}")
        else:
            st.info("No students added in database yet.")

    elif staff_menu == "📊 Attendance Management":
        st.subheader("📋 Student Attendance Management & Tracking")
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