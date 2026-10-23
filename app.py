import streamlit as st
import datetime
import random
import sqlite3
import hashlib
import base64
import os

# Page Configuration
st.set_page_config(
    page_title="DSC Portal | Digital Student Certification & Assessment System", 
    page_icon="🎓", 
    layout="wide"
)

# Safe function to convert local background image to base64 if present
def get_base64_of_bin_file(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

# Set background image & Ultra-Professional Dark DSC Portal CSS
try:
    bin_str = get_base64_of_bin_file('bg.jpg')
    if bin_str:
        bg_css = f'''
        .stApp {{
            background-image: linear-gradient(rgba(10, 18, 26, 0.95), rgba(15, 28, 40, 0.97)), url("data:image/jpg;base64,{bin_str}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
            color: #ffffff !important;
        }}
        '''
    else:
        bg_css = '''
        .stApp {{
            background: linear-gradient(135deg, #0d1b2a, #1b263b);
            color: #ffffff !important;
        }}
        '''
    
    page_bg_img = f'''
    <style>
    {bg_css}
    
    /* Ensure all text, labels, and headers are crystal clear white/light */
    h1, h2, h3, h4, h5, h6, p, span, label, div {{
        color: #ffffff !important;
    }}

    /* Sidebar Professional Theme */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #0d1b2a 0%, #1b263b 100%) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
        color: #ffffff !important;
    }}
    
    section[data-testid="stSidebar"] .stMarkdown, 
    section[data-testid="stSidebar"] label, 
    section[data-testid="stSidebar"] span {{
        color: #ffffff !important;
    }}

    /* Completely Hide Radio Circles and make navigation look like professional menu cards */
    section[data-testid="stSidebar"] div.row-widget.stRadio > div {{
        gap: 5px;
    }}
    section[data-testid="stSidebar"] div.row-widget.stRadio input[type="radio"] {{
        display: none !important;
    }}
    section[data-testid="stSidebar"] div.row-widget.stRadio label {{
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.12);
        padding: 8px 12px;
        border-radius: 8px;
        transition: all 0.3s ease;
        cursor: pointer;
        color: #ffffff !important;
    }}
    section[data-testid="stSidebar"] div.row-widget.stRadio label:hover {{
        background: rgba(0, 123, 255, 0.3);
        border-color: rgba(0, 123, 255, 0.6);
    }}

    /* Professional Top Header Banner */
    .dashboard-header-banner {{
        background: linear-gradient(135deg, rgba(20, 35, 50, 0.95), rgba(12, 24, 35, 0.98));
        padding: 22px 30px;
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        box-shadow: 0 8px 25px rgba(0,0,0,0.6);
        backdrop-filter: blur(10px);
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 25px;
        color: #ffffff !important;
    }}

    /* Modern Hero Card */
    .hero-box {{ 
        background: linear-gradient(135deg, rgba(20, 35, 50, 0.9), rgba(13, 27, 38, 0.95)); 
        padding: 30px; 
        border-radius: 14px; 
        color: white !important; 
        text-align: center; 
        box-shadow: 0 8px 25px rgba(0,0,0,0.6);
        border: 1px solid rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        margin-bottom: 25px;
    }}
    
    /* Professional Dashboard Metrics Cards */
    .dash-card {{
        background: linear-gradient(135deg, rgba(22, 40, 58, 0.9), rgba(13, 27, 38, 0.95));
        padding: 20px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        box-shadow: 0 6px 20px rgba(0,0,0,0.5);
        backdrop-filter: blur(8px);
        text-align: center;
        margin-bottom: 10px;
        color: #ffffff !important;
    }}
    
    /* Captcha Box Styling */
    .captcha-box {{
        background: linear-gradient(135deg, #e6f2ff, #cce5ff) !important;
        color: #004085 !important;
        font-size: 28px !important;
        font-weight: 800 !important;
        letter-spacing: 10px !important;
        text-align: center !important;
        padding: 12px !important;
        border-radius: 8px !important;
        border: 2px dashed #0056b3 !important;
        margin-bottom: 12px !important;
    }}
    
    /* Input Fields Theme */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div {{
        background-color: rgba(16, 32, 44, 0.95) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 8px !important;
    }}

    /* Standard Button Customization */
    .stButton>button {{
        background: linear-gradient(135deg, #007bff, #0056b3) !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        width: 100% !important;
        padding: 10px 15px !important;
        box-shadow: 0 4px 12px rgba(0,123,255,0.4) !important;
        border: none !important;
        transition: all 0.3s ease;
    }}
    .stButton>button:hover {{
        background: linear-gradient(135deg, #0056b3, #003d82) !important;
        box-shadow: 0 6px 16px rgba(0,123,255,0.6) !important;
    }}
    
    /* Stylish Logout Button inside Sidebar */
    section[data-testid="stSidebar"] .stButton:last-child > button {{
        background: linear-gradient(135deg, #ff4d4d, #cc0000) !important;
        box-shadow: 0 4px 12px rgba(255, 77, 77, 0.4) !important;
    }}
    section[data-testid="stSidebar"] .stButton:last-child > button:hover {{
        background: linear-gradient(135deg, #cc0000, #990000) !important;
    }}

    /* Forms Styling */
    div.stForm {{
        background: rgba(13, 27, 38, 0.95);
        padding: 25px;
        border-radius: 14px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.7);
        border: 1px solid rgba(255, 255, 255, 0.15);
        color: white !important;
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)
except Exception as e:
    pass

# Helper function to hash passwords securely
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Database Initialization with Fees Columns
def init_db():
    conn = sqlite3.connect('dsc_portal.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            roll_no TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            password TEXT NOT NULL,
            section TEXT DEFAULT 'Section AJ',
            status TEXT DEFAULT 'Active',
            id_card_status TEXT DEFAULT 'Not Applied',
            doc_status TEXT DEFAULT 'Not Uploaded',
            status_10th TEXT DEFAULT 'Pending',
            status_12th TEXT DEFAULT 'Pending',
            status_tc TEXT DEFAULT 'Pending',
            status_photo TEXT DEFAULT 'Pending',
            father_name TEXT,
            mother_name TEXT,
            student_mobile TEXT,
            mother_mobile TEXT,
            father_mobile TEXT,
            email TEXT,
            marksheet_10th BLOB,
            marksheet_12th BLOB,
            tc BLOB,
            photo BLOB,
            academic_fee REAL DEFAULT 0.0,
            hostel_fee REAL DEFAULT 0.0,
            mess_fee REAL DEFAULT 0.0,
            bus_fee REAL DEFAULT 0.0
        )
    ''')
    
    cols = [
        ("doc_status", "TEXT DEFAULT 'Not Uploaded'"),
        ("status_10th", "TEXT DEFAULT 'Pending'"),
        ("status_12th", "TEXT DEFAULT 'Pending'"),
        ("status_tc", "TEXT DEFAULT 'Pending'"),
        ("status_photo", "TEXT DEFAULT 'Pending'"),
        ("father_name", "TEXT"), ("mother_name", "TEXT"),
        ("student_mobile", "TEXT"), ("mother_mobile", "TEXT"), ("father_mobile", "TEXT"),
        ("email", "TEXT"), ("marksheet_10th", "BLOB"), ("marksheet_12th", "BLOB"), ("tc", "BLOB"),
        ("academic_fee", "REAL DEFAULT 0.0"),
        ("hostel_fee", "REAL DEFAULT 0.0"),
        ("mess_fee", "REAL DEFAULT 0.0"),
        ("bus_fee", "REAL DEFAULT 0.0")
    ]
    for c_name, c_type in cols:
        try:
            cursor.execute(f"ALTER TABLE students ADD COLUMN {c_name} {c_type}")
        except sqlite3.OperationalError:
            pass

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

if not st.session_state.logged_in and "logged_in" in st.query_params and st.query_params["logged_in"] == "true":
    st.session_state.logged_in = True
    st.session_state.user_role = st.query_params.get("role", "")
    st.session_state.username = st.query_params.get("username", "")
    st.session_state.identifier = st.query_params.get("identifier", "")

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
    st.sidebar.markdown("### 🔒 DSC Gateway")
    portal_choice = st.sidebar.radio("Select Portal", ["Student Portal", "Staff / Admin Portal"])
    
    col1, col2, col3 = st.columns([2, 6, 2])
    with col1:
        st.markdown("### 🎓 **DSC**")
    with col2:
        st.markdown("<p style='text-align: center; color: #ffffff; font-size: 14px; font-weight: 600;'>SECURE ASSESSMENT & CERTIFICATION SYSTEM</p>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<p style='text-align: right; color: #4da6ff; font-weight: bold;'>Mode: {portal_choice}</p>", unsafe_allow_html=True)

    st.markdown("---")

    if portal_choice == "Staff / Admin Portal":
        admin_action = st.radio("Admin Action", ["Admin Login", "Admin Sign Up"], horizontal=True)
        
        if admin_action == "Admin Sign Up":
            st.markdown("<h2 style='text-align: center; color: white;'>📝 Faculty / Admin Registration</h2>", unsafe_allow_html=True)
            col_r1, col_r2, col_r3 = st.columns([1, 2, 1])
            with col_r2:
                with st.form("admin_signup_form"):
                    reg_name = st.text_input("Faculty Full Name")
                    reg_id = st.text_input("Admin ID / Employee Code")
                    reg_pass = st.text_input("Create Secure Password", type="password")
                    reg_photo = st.file_uploader("Upload Faculty Profile Photo", type=["jpg", "png", "jpeg"])
                    
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
                                st.success("Admin account successfully created! Now go to Admin Login.")
                            except sqlite3.IntegrityError:
                                st.error("Error: This Admin ID is already registered!")
                        else:
                            st.error("Please fill all fields.")
        else:
            st.markdown("<h2 style='text-align: center; color: white;'>🔐 Secure Faculty Login Portal</h2>", unsafe_allow_html=True)
            col_f1, col_f2, col_f3 = st.columns([1, 2, 1])
            with col_f2:
                with st.form("admin_login_form"):
                    admin_id_input = st.text_input("Faculty ID / Employee Code")
                    admin_pass_input = st.text_input("Password", type="password")
                    
                    st.markdown("<p style='margin-bottom: 5px; font-weight: bold;'>Verification Captcha Code:</p>", unsafe_allow_html=True)
                    st.markdown(f"<div class='captcha-box'>{st.session_state.captcha_val}</div>", unsafe_allow_html=True)
                    captcha_input = st.text_input("Enter the 4-digit code shown above")
                    
                    col_b1, col_b2 = st.columns(2)
                    with col_b1:
                        submit_admin_login = st.form_submit_button("Faculty Login")
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
                                    
                                    st.query_params["logged_in"] = "true"
                                    st.query_params["role"] = st.session_state.user_role
                                    st.query_params["username"] = st.session_state.username
                                    st.query_params["identifier"] = st.session_state.identifier
                                    
                                    st.success("Login Successful!")
                                    st.rerun()
                                else:
                                    st.error("Invalid Faculty ID or Password!")
                            else:
                                st.error("Please enter ID and Password.")
                        else:
                            st.error("Invalid Captcha code!")
                            st.session_state.captcha_val = str(random.randint(1000, 9999))

    else:
        st.markdown(f"""
            <div class="hero-box">
                <h1>DSC Student Portal</h1>
                <p style="font-size: 15px; margin-top: 10px; color: #d0d7de;">Secure Authentication via Roll Number & Encrypted Database</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        st.markdown("<h2 style='text-align: center; margin-top: 15px; color: white;'>🎓 Student Secure Login</h2>", unsafe_allow_html=True)
        
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
                                if student[4] == 'Blocked':
                                    st.error("Your account has been BLOCKED by the administration. Contact support desk.")
                                else:
                                    st.session_state.logged_in = True
                                    st.session_state.user_role = "Regular Student"
                                    st.session_state.username = student[1].upper()
                                    st.session_state.identifier = student[0]
                                    
                                    st.query_params["logged_in"] = "true"
                                    st.query_params["role"] = st.session_state.user_role
                                    st.query_params["username"] = st.session_state.username
                                    st.query_params["identifier"] = st.session_state.identifier
                                    
                                    st.success("Student Login Successful!")
                                    st.rerun()
                            else:
                                st.error("Access Denied! Roll number not registered or incorrect password.")
                        else:
                            st.error("Please enter Roll Number and Password.")
                    else:
                        st.error("Invalid Captcha code!")
                        st.session_state.captcha_val = str(random.randint(1000, 9999))

def show_student_dashboard():
    conn = sqlite3.connect('dsc_portal.db')
    cursor = conn.cursor()
    cursor.execute("SELECT photo, id_card_status FROM students WHERE roll_no = ?", (st.session_state.identifier,))
    res = cursor.fetchone()
    conn.close()
    
    if res and res[0]:
        st.sidebar.image(res[0], width=100)
    else:
        st.sidebar.image("https://img.icons8.com/color/96/student-male.png", width=90)

    st.sidebar.markdown(f"### **{st.session_state.username}**")
    st.sidebar.markdown(f"<p style='color: #d0d7de; font-size: 12px;'>Roll No: {st.session_state.identifier} | Student</p>", unsafe_allow_html=True)
    st.sidebar.markdown("---")
    
    selected_lang = st.sidebar.selectbox("🌐 Choose Language", ["English", "Hindi"])
    
    menu = st.sidebar.radio("Navigation", [
        "📌 Main Dashboard", 
        "📝 Personal Details & Documents",
        "💳 Fee Dues & Payments",
        "🆔 Apply For ID Card", 
        "📚 Academic Examinations", 
        "🎯 Practice Dashboard", 
        "🎙️ AI Interview", 
        "🗄️ Database/SQL", 
        "🌐 Web Tech", 
        "✍️ Essay Writing", 
        "😀 Face Registration", 
        "❓ Help Desk"
    ])
    
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Logout Securely"):
        st.session_state.logged_in = False
        st.session_state.user_role = ""
        st.session_state.username = ""
        st.session_state.identifier = ""
        st.query_params.clear()
        st.session_state.captcha_val = str(random.randint(1000, 9999))
        st.rerun()

    current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
    st.markdown(f"""
        <div class="dashboard-header-banner">
            <div>
                <h2 style="margin: 0; color: #ffffff; font-size: 22px; font-weight: 700;">Student Dashboard — {st.session_state.username}</h2>
                <p style="margin: 4px 0 0 0; color: #919eab; font-size: 13px;">University Roll Number: <b style="color: #4da6ff;">{st.session_state.identifier}</b></p>
            </div>
            <div style="text-align: right; background: rgba(0,0,0,0.3); padding: 8px 15px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.08);">
                <p style="margin: 0; color: #ffffff; font-size: 13px; font-weight: 600;">⏰ {current_time}</p>
                <p style="margin: 2px 0 0 0; color: #00e676; font-size: 11px; font-weight: bold;">🟢 Secure Proctor Active</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if menu == "📌 Main Dashboard":
        st.markdown(f"""
            <div class="hero-box">
                <h2>🎓 Welcome, {st.session_state.username}</h2>
                <p style="color: #c9d1d9; font-size: 14px; margin-top: 5px;">Track your academic assessments, verify documents, and explore learning tools securely on DSC Portal.</p>
            </div>
        """, unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown("""
                <div class="dash-card">
                    <h4 style="color: #4da6ff; margin-bottom: 5px; font-size: 13px;">Completed Exams</h4>
                    <h2 style="color: white; margin: 0; font-size: 20px;">0 / 0</h2>
                </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown("""
                <div class="dash-card">
                    <h4 style="color: #ffc107; margin-bottom: 5px; font-size: 13px;">Needs Attention</h4>
                    <h2 style="color: white; margin: 0; font-size: 20px;">0 Active</h2>
                </div>
            """, unsafe_allow_html=True)
        with c3:
            st.markdown("""
                <div class="dash-card">
                    <h4 style="color: #28a745; margin-bottom: 5px; font-size: 13px;">Upcoming Tests</h4>
                    <h2 style="color: white; margin: 0; font-size: 20px;">1 Scheduled</h2>
                </div>
            """, unsafe_allow_html=True)
        with c4:
            st.markdown("""
                <div class="dash-card">
                    <h4 style="color: #17a2b8; margin-bottom: 5px; font-size: 13px;">Practice Progress</h4>
                    <h2 style="color: white; margin: 0; font-size: 20px;">0.0%</h2>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        
        col_inf1, col_inf2 = st.columns(2)
        with col_inf1:
            st.markdown("""
                <div class="dash-card" style="text-align: left; padding: 22px;">
                    <h3 style="color: #4da6ff; margin-top: 0; font-size: 16px;">📌 Exam Journey & Guidelines</h3>
                    <p style="color: #d0d7de; font-size: 13px;">Your account is fully verified by the administration. All upcoming examinations and assignments will appear in your schedule on time. Ensure your biometrics and document verification are up to date.</p>
                </div>
            """, unsafe_allow_html=True)
        with col_inf2:
            st.markdown("""
                <div class="dash-card" style="text-align: left; padding: 22px;">
                    <h3 style="color: #28a745; margin-top: 0; font-size: 16px;">📜 Recent Activity History</h3>
                    <ul style="color: #d0d7de; font-size: 13px; padding-left: 18px; margin-bottom: 0;">
                        <li><b>Assessment :</b> Full Stack & DSA Evaluation — <span style="color: #28a745;">Completed</span></li>
                        <li><b>Coding Lab :</b> Array Manipulation — <span style="color: #28a745;">Passed</span></li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)

    elif menu == "📝 Personal Details & Documents":
        st.subheader("📝 Student Personal Details & Document Verification Portal")
        
        conn = sqlite3.connect('dsc_portal.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name, father_name, mother_name, student_mobile, mother_mobile, father_mobile, email, status_10th, status_12th, status_tc, status_photo FROM students WHERE roll_no = ?", (st.session_state.identifier,))
        st_data = cursor.fetchone()
        conn.close()

        def_name = st_data[0] if st_data else st.session_state.username
        def_fn = st_data[1] if st_data and st_data[1] else ""
        def_mn = st_data[2] if st_data and st_data[2] else ""
        def_sm = st_data[3] if st_data and st_data[3] else ""
        def_mom = st_data[4] if st_data and st_data[4] else ""
        def_fm = st_data[5] if st_data and st_data[5] else ""
        def_email = st_data[6] if st_data and st_data[6] else ""
        s_10 = st_data[7] if st_data and st_data[7] else "Pending"
        s_12 = st_data[8] if st_data and st_data[8] else "Pending"
        s_tc = st_data[9] if st_data and st_data[9] else "Pending"
        s_ph = st_data[10] if st_data and st_data[10] else "Pending"

        st.markdown("### 📊 Individual Document Verification Status:")
        sc1, sc2, sc3, sc4 = st.columns(4)
        sc1.write(f"**10th Marksheet:** `{s_10}`")
        sc2.write(f"**12th Marksheet:** `{s_12}`")
        sc3.write(f"**Transfer Cert (TC):** `{s_tc}`")
        sc4.write(f"**Student Photo:** `{s_ph}`")
        st.markdown("---")

        with st.form("personal_details_form"):
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                full_name = st.text_input("Full Name of Student", value=def_name)
                father_name = st.text_input("Father's Name", value=def_fn)
                mother_name = st.text_input("Mother's Name", value=def_mn)
                student_mob = st.text_input("Mobile Number of Student", value=def_sm)
            with col_d2:
                mother_mob = st.text_input("Mother's Mobile Number", value=def_mom)
                father_mob = st.text_input("Father's Mobile Number", value=def_fm)
                email_id = st.text_input("Email ID (Student/Parent)", value=def_email)

            st.markdown("---")
            st.markdown("### 📁 Document Uploads (10th/12th/TC in PDF, Photo in JPG/JPEG)")
            up_10th = st.file_uploader("Upload 10th Marksheet (PDF only)", type=["pdf"])
            up_12th = st.file_uploader("Upload 12th Marksheet (PDF only)", type=["pdf"])
            up_photo = st.file_uploader("Upload Student Photo (JPG / JPEG only)", type=["jpg", "jpeg"])
            up_tc = st.file_uploader("Upload Transfer Certificate - TC (PDF only)", type=["pdf"])

            submit_details = st.form_submit_button("Save & Submit Documents for Approval")

            if submit_details:
                try:
                    conn = sqlite3.connect('dsc_portal.db')
                    cursor = conn.cursor()
                    
                    m10_bytes = up_10th.read() if up_10th else None
                    m12_bytes = up_12th.read() if up_12th else None
                    photo_bytes = up_photo.read() if up_photo else None
                    tc_bytes = up_tc.read() if up_tc else None

                    if m10_bytes:
                        cursor.execute("UPDATE students SET marksheet_10th = ?, status_10th = 'Pending' WHERE roll_no = ?", (m10_bytes, st.session_state.identifier))
                    if m12_bytes:
                        cursor.execute("UPDATE students SET marksheet_12th = ?, status_12th = 'Pending' WHERE roll_no = ?", (m12_bytes, st.session_state.identifier))
                    if photo_bytes:
                        cursor.execute("UPDATE students SET photo = ?, status_photo = 'Pending' WHERE roll_no = ?", (photo_bytes, st.session_state.identifier))
                    if tc_bytes:
                        cursor.execute("UPDATE students SET tc = ?, status_tc = 'Pending' WHERE roll_no = ?", (tc_bytes, st.session_state.identifier))

                    cursor.execute("""
                        UPDATE students SET name = ?, father_name = ?, mother_name = ?, student_mobile = ?, mother_mobile = ?, father_mobile = ?, email = ?
                        WHERE roll_no = ?
                    """, (full_name.strip(), father_name.strip(), mother_name.strip(), student_mob.strip(), mother_mob.strip(), father_mob.strip(), email_id.strip(), st.session_state.identifier))

                    conn.commit()
                    conn.close()
                    st.success("Details and uploaded documents successfully submitted to Admin for verification!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error updating details: {e}")

    elif menu == "💳 Fee Dues & Payments":
        st.subheader("💳 Student Fee Dues & Breakdown Portal")
        
        conn = sqlite3.connect('dsc_portal.db')
        cursor = conn.cursor()
        cursor.execute("SELECT academic_fee, hostel_fee, mess_fee, bus_fee FROM students WHERE roll_no = ?", (st.session_state.identifier,))
        fee_row = cursor.fetchone()
        conn.close()

        acad = fee_row[0] if fee_row and fee_row[0] is not None else 0.0
        hostel = fee_row[1] if fee_row and fee_row[1] is not None else 0.0
        mess = fee_row[2] if fee_row and fee_row[2] is not None else 0.0
        bus = fee_row[3] if fee_row and fee_row[3] is not None else 0.0
        total_fee = acad + hostel + mess + bus

        fc1, fc2, fc3, fc4 = st.columns(4)
        with fc1:
            st.markdown(f"""
                <div class="dash-card">
                    <h4 style="color: #4da6ff; font-size: 13px;">Academic Fee</h4>
                    <h2 style="color: white; font-size: 20px;">₹ {acad:,.2f}</h2>
                </div>
            """, unsafe_allow_html=True)
        with fc2:
            st.markdown(f"""
                <div class="dash-card">
                    <h4 style="color: #ffc107; font-size: 13px;">Hostel Fee</h4>
                    <h2 style="color: white; font-size: 20px;">₹ {hostel:,.2f}</h2>
                </div>
            """, unsafe_allow_html=True)
        with fc3:
            st.markdown(f"""
                <div class="dash-card">
                    <h4 style="color: #28a745; font-size: 13px;">Mess Fee</h4>
                    <h2 style="color: white; font-size: 20px;">₹ {mess:,.2f}</h2>
                </div>
            """, unsafe_allow_html=True)
        with fc4:
            st.markdown(f"""
                <div class="dash-card">
                    <h4 style="color: #17a2b8; font-size: 13px;">Bus Fee</h4>
                    <h2 style="color: white; font-size: 20px;">₹ {bus:,.2f}</h2>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
            <div class="hero-box" style="text-align: left; padding: 20px;">
                <h3 style="margin: 0; color: #ffffff; font-size: 18px;">Total Outstanding Dues: <span style="color: #00e676;">₹ {total_fee:,.2f}</span></h3>
                <p style="margin: 5px 0 0 0; color: #919eab; font-size: 13px;">Please pay your pending dues before the upcoming semester examination deadline.</p>
            </div>
        """, unsafe_allow_html=True)

        if total_fee > 0:
            if st.button("Proceed to Online Fee Payment Gateway"):
                st.success("Redirecting to secure payment gateway... (Simulation: Payment Successful!)")
        else:
            st.success("🎉 All dues are fully cleared! No pending payments.")

    elif menu == "🆔 Apply For ID Card":
        st.subheader("🆔 Student Digital ID Card Application Portal")
        
        conn = sqlite3.connect('dsc_portal.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id_card_status, section, name FROM students WHERE roll_no = ?", (st.session_state.identifier,))
        student_info = cursor.fetchone()
        conn.close()
        
        current_id_status = student_info[0] if student_info else "Not Applied"
        student_section = student_info[1] if student_info else "Section AJ"
        
        st.write(f"**Current ID Card Status:** `{current_id_status}`")
        st.write(f"**Assigned Section:** `{student_section}`")
        
        if current_id_status == "Not Applied":
            if st.button("Submit Request for Official ID Card to Administration"):
                conn = sqlite3.connect('dsc_portal.db')
                cursor = conn.cursor()
                cursor.execute("UPDATE students SET id_card_status = 'Pending Approval' WHERE roll_no = ?", (st.session_state.identifier,))
                conn.commit()
                conn.close()
                st.success("ID Card request submitted successfully to Admin! Status changed to Pending.")
                st.rerun()
        elif current_id_status == "Pending Approval":
            st.warning("Your ID Card request is currently pending review by the administration.")
        elif current_id_status == "Approved":
            st.success("🎉 Your ID Card application has been APPROVED by the Admin! You can collect it from the department.")

    elif menu == "📚 Academic Examinations":
        st.subheader("📚 Academic Examinations & Quizzes")
        st.info("No active examinations are currently live for your ID.")

    elif menu == "🎯 Practice Dashboard":
        st.subheader("🎯 Practice Lab & Quiz Progress")
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Quiz Finished", "1")
            st.metric("Active Sessions", "0")
        with c2:
            st.metric("Waiting Quizzes", "4568")
            st.metric("Overall Completion", "0.0%")
        st.success("Your remaining quizzes are waiting — check availability and filters.")

    elif menu == "🎙️ AI Interview":
        st.subheader("🎙️ AI Interview Practice & Self Introduction")
        if st.button("Start AI Powered Analysis"):
            st.balloons()
            st.success("Voice sample analyzed! Confidence Score: 88/100, Fluency: Excellent.")

    elif menu == "🗄️ Database/SQL":
        st.subheader("🗄️ Database & SQL Query Editor")
        query = st.text_area("SQL Query", value=f"SELECT * FROM students WHERE roll_no = '{st.session_state.identifier}';")
        if st.button("Execute SQL Query"):
            st.code("Query executed successfully. 1 row returned.", language="sql")

    elif menu == "🌐 Web Tech":
        st.subheader("🌐 Web Tech HTML/CSS Compiler")
        html_code = st.text_area("HTML Code", value="<h2>Welcome to DSC Portal</h2><p>Live Preview Active.</p>")
        st.components.v1.html(html_code, height=120)

    elif menu == "✍️ Essay Writing":
        st.subheader("✍️ AI Essay Evaluation")
        st.text_area("Write your essay here:", height=150)
        if st.button("Evaluate Essay"):
            st.success("Grammar & Coherence Score: 92/100")

    elif menu == "😀 Face Registration":
        st.subheader("👤 AI Proctoring Face Recognition")
        st.success(f"Face biometrics verified and linked successfully with Roll No: {st.session_state.identifier}")

    elif menu == "❓ Help Desk":
        st.subheader("🛠️ Technical Exam Help Desk & Support")
        st.info("If you are facing any issues regarding the portal, login, or examinations, please feel free to reach out to the support desk below:")
        
        col_h1, col_h2 = st.columns(2)
        with col_h1:
            st.metric("Support Administrator", "RUDRAKSH AGRAWAL")
        with col_h2:
            st.metric("Helpline Contact Number", "9634350854")

def show_staff_dashboard():
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
    st.sidebar.markdown(f"<p style='color: #d0d7de; font-size: 12px;'>ID: {st.session_state.identifier} | Faculty</p>", unsafe_allow_html=True)
    st.sidebar.markdown("---")
    
    staff_menu = st.sidebar.radio("Teacher Panel", [
        "👥 Add & Manage Students",
        "💰 Manage Student Fees",
        "📊 Section-wise Student Records",
        "📂 Student Personal & Docs",
        "🆔 ID Card Requests",
        "⚙️ Admin Profile & Photo",
        "📊 Attendance Management",
        "📝 Quiz & Test Creator",
        "💻 Code Challenges Management"
    ])
    
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Logout Securely"):
        st.session_state.logged_in = False
        st.session_state.user_role = ""
        st.session_state.username = ""
        st.session_state.identifier = ""
        st.query_params.clear()
        st.session_state.captcha_val = str(random.randint(1000, 9999))
        st.rerun()

    st.markdown(f"""
        <div class="dashboard-header-banner">
            <div>
                <h2 style="margin: 0; color: #ffffff; font-size: 22px; font-weight: 700;">Faculty & Admin Control Center — {st.session_state.username}</h2>
                <p style="margin: 4px 0 0 0; color: #919eab; font-size: 13px;">Faculty ID: <b style="color: #4da6ff;">{st.session_state.identifier}</b></p>
            </div>
            <div style="text-align: right; background: rgba(0,0,0,0.3); padding: 8px 15px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.08);">
                <p style="margin: 0; color: #ffffff; font-size: 13px; font-weight: 600;">🔒 Secure Admin Mode</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if staff_menu == "👥 Add & Manage Students":
        st.subheader("➕ Register New Student & Manage Status (Block/Unblock/Update Photo)")
        
        conn = sqlite3.connect('dsc_portal.db')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM students")
        total_registered = cursor.fetchone()[0]
        conn.close()
        
        st.metric("Total Registered Students in Portal", total_registered)
        
        with st.form("add_student_form"):
            new_name = st.text_input("Student Full Name")
            new_roll = st.text_input("Student Roll Number")
            new_pass = st.text_input("Assign Password", type="password")
            student_section = st.selectbox("Assign University Section / Batch", ["Section AJ", "Section AW", "CSE Batch A", "Section B"])
            student_photo = st.file_uploader("Upload Student Photo", type=["jpg", "png", "jpeg"])
            
            submit_student = st.form_submit_button("Register Student in Local Database")
            if submit_student:
                if new_name.strip() and new_roll.strip() and new_pass.strip():
                    try:
                        photo_bytes = student_photo.read() if student_photo else None
                        conn = sqlite3.connect('dsc_portal.db')
                        cursor = conn.cursor()
                        hashed_password = hash_password(new_pass.strip())
                        cursor.execute("INSERT INTO students (roll_no, name, password, section, status, id_card_status, doc_status, status_10th, status_12th, status_tc, status_photo, photo) VALUES (?, ?, ?, ?, 'Active', 'Not Applied', 'Not Uploaded', 'Pending', 'Pending', 'Pending', 'Pending', ?)", 
                                       (new_roll.strip(), new_name.strip(), hashed_password, student_section, photo_bytes))
                        conn.commit()
                        conn.close()
                        st.success(f"Student '{new_name}' (Roll No: {new_roll}) successfully registered in {student_section}!")
                        st.rerun()
                    except sqlite3.IntegrityError:
                        st.error("Error: This Roll Number is already registered!")
                else:
                    st.error("Please fill all required fields.")

        st.markdown("### 🛡️ Manage Student Access & Update Photo")
        conn = sqlite3.connect('dsc_portal.db')
        cursor = conn.cursor()
        cursor.execute("SELECT roll_no, name, section, status FROM students")
        all_students = cursor.fetchall()
        conn.close()

        if all_students:
            for st_rec in all_students:
                r_no, s_name, s_sec, s_status = st_rec
                with st.expander(f"👤 {s_name} (Roll No: {r_no}) — Section: {s_sec} [Status: {s_status}]"):
                    col_p1, col_p2 = st.columns([1, 1])
                    with col_p1:
                        if s_status == 'Active':
                            if st.button(f"Block Student {r_no}", key=f"block_{r_no}"):
                                conn = sqlite3.connect('dsc_portal.db')
                                cursor = conn.cursor()
                                cursor.execute("UPDATE students SET status = 'Blocked' WHERE roll_no = ?", (r_no,))
                                conn.commit()
                                conn.close()
                                st.warning(f"Student {s_name} has been blocked.")
                                st.rerun()
                        else:
                            if st.button(f"Unblock Student {r_no}", key=f"unblock_{r_no}"):
                                conn = sqlite3.connect('dsc_portal.db')
                                cursor = conn.cursor()
                                cursor.execute("UPDATE students SET status = 'Active' WHERE roll_no = ?", (r_no,))
                                conn.commit()
                                conn.close()
                                st.success(f"Student {s_name} has been unblocked.")
                                st.rerun()
                    
                    with col_p2:
                        with st.form(f"update_photo_form_{r_no}"):
                            new_st_photo = st.file_uploader(f"Change Photo for {r_no}", type=["jpg", "png", "jpeg"], key=f"ph_up_{r_no}")
                            up_btn = st.form_submit_button("Update Student Photo")
                            if up_btn:
                                if new_st_photo:
                                    p_bytes = new_st_photo.read()
                                    conn = sqlite3.connect('dsc_portal.db')
                                    cursor = conn.cursor()
                                    cursor.execute("UPDATE students SET photo = ?, status_photo = 'Pending' WHERE roll_no = ?", (p_bytes, r_no))
                                    conn.commit()
                                    conn.close()
                                    st.success(f"Photo updated successfully for Roll No: {r_no}!")
                                    st.rerun()
                                else:
                                    st.error("Please upload an image file.")
        else:
            st.info("No students registered yet.")

    elif staff_menu == "💰 Manage Student Fees":
        st.subheader("💰 Assign / Update Student Fees (Academic, Hostel, Mess, Bus)")
        
        conn = sqlite3.connect('dsc_portal.db')
        cursor = conn.cursor()
        cursor.execute("SELECT roll_no, name, section, academic_fee, hostel_fee, mess_fee, bus_fee FROM students")
        fee_students = cursor.fetchall()
        conn.close()

        if fee_students:
            for fs in fee_students:
                r_no, name, sec, cur_acad, cur_hostel, cur_mess, cur_bus = fs
                with st.expander(f"💵 {name} (Roll No: {r_no}) — Section: {sec}"):
                    with st.form(f"fee_form_{r_no}"):
                        c_f1, c_f2 = st.columns(2)
                        with c_f1:
                            new_acad = st.number_input("Academic Fee (₹)", value=float(cur_acad), min_value=0.0, step=1000.0, key=f"acad_{r_no}")
                            new_hostel = st.number_input("Hostel Fee (₹)", value=float(cur_hostel), min_value=0.0, step=1000.0, key=f"hostel_{r_no}")
                        with c_f2:
                            new_mess = st.number_input("Mess Fee (₹)", value=float(cur_mess), min_value=0.0, step=500.0, key=f"mess_{r_no}")
                            new_bus = st.number_input("Bus Fee (₹)", value=float(cur_bus), min_value=0.0, step=500.0, key=f"bus_{r_no}")

                        submit_fee = st.form_submit_button("Update Student Fee Structure")
                        if submit_fee:
                            conn = sqlite3.connect('dsc_portal.db')
                            cursor = conn.cursor()
                            cursor.execute("""
                                UPDATE students SET academic_fee = ?, hostel_fee = ?, mess_fee = ?, bus_fee = ?
                                WHERE roll_no = ?
                            """, (new_acad, new_hostel, new_mess, new_bus, r_no))
                            conn.commit()
                            conn.close()
                            st.success(f"Fee details successfully updated for Roll No: {r_no}!")
                            st.rerun()
        else:
            st.info("No students available for fee management.")

    elif staff_menu == "📊 Section-wise Student Records":
        st.subheader("📊 Section-Wise Detailed Student Records & Filtering")
        
        selected_filter_section = st.selectbox("Filter Students by Section / Batch", ["All Sections", "Section AJ", "Section AW", "CSE Batch A", "Section B"])
        
        conn = sqlite3.connect('dsc_portal.db')
        cursor = conn.cursor()
        if selected_filter_section == "All Sections":
            cursor.execute("SELECT roll_no, name, section, status, id_card_status FROM students")
        else:
            cursor.execute("SELECT roll_no, name, section, status, id_card_status FROM students WHERE section = ?", (selected_filter_section,))
        
        filtered_students = cursor.fetchall()
        conn.close()
        
        st.markdown(f"### Total Students in `{selected_filter_section}`: **{len(filtered_students)}**")
        
        if filtered_students:
            for fs in filtered_students:
                with st.expander(f"Roll No: {fs[0]} — {fs[1]} ({fs[2]})"):
                    st.write(f"• **Full Name:** {fs[1]}")
                    st.write(f"• **University Roll Number:** {fs[0]}")
                    st.write(f"• **Assigned Section:** {fs[2]}")
                    st.write(f"• **Account Status:** `{fs[3]}`")
                    st.write(f"• **ID Card Status:** `{fs[4]}`")
        else:
            st.info("No student records found for this section.")

    elif staff_menu == "📂 Student Personal & Docs":
        st.subheader("📂 Student Personal Details & Individual Document Approval / Rejection")
        
        conn = sqlite3.connect('dsc_portal.db')
        cursor = conn.cursor()
        cursor.execute("SELECT roll_no, name, section, father_name, mother_name, student_mobile, father_mobile, email, marksheet_10th, marksheet_12th, tc, photo, status_10th, status_12th, status_tc, status_photo FROM students")
        all_st_docs = cursor.fetchall()
        conn.close()

        if all_st_docs:
            for sd in all_st_docs:
                r_no, name, sec, fn, mn, sm, fm, email, m10, m12, tc, ph, s_10, s_12, s_tc, s_ph = sd
                with st.expander(f"📋 {name} (Roll No: {r_no}) — {sec}"):
                    c_info1, c_info2 = st.columns(2)
                    with c_info1:
                        st.write(f"**Full Name:** {name}")
                        st.write(f"**Father's Name:** {fn if fn else 'Not Filled'}")
                        st.write(f"**Mother's Name:** {mn if mn else 'Not Filled'}")
                        st.write(f"**Student Mobile:** {sm if sm else 'Not Filled'}")
                    with c_info2:
                        st.write(f"**Father's Mobile:** {fm if fm else 'Not Filled'}")
                        st.write(f"**Email ID:** {email if email else 'Not Filled'}")
                        st.write(f"**Section:** {sec}")
                    
                    st.markdown("---")
                    st.markdown("### 📑 Document Review & Individual Approval/Rejection")

                    # 10th Marksheet
                    st.write(f"**10th Marksheet Status:** `{s_10}`")
                    col_10_a, col_10_b, col_10_c = st.columns([2, 1, 1])
                    if m10:
                        col_10_a.download_button("Download 10th PDF", m10, file_name=f"10th_{r_no}.pdf", mime="application/pdf", key=f"dl_10_{r_no}")
                    else:
                        col_10_a.write("❌ Not Uploaded")
                    if col_10_b.button(f"Approve 10th", key=f"app_10_{r_no}"):
                        conn = sqlite3.connect('dsc_portal.db')
                        cursor = conn.cursor()
                        cursor.execute("UPDATE students SET status_10th = 'Approved' WHERE roll_no = ?", (r_no,))
                        conn.commit()
                        conn.close()
                        st.success("10th Marksheet Approved!")
                        st.rerun()
                    if col_10_c.button(f"Reject 10th", key=f"rej_10_{r_no}"):
                        conn = sqlite3.connect('dsc_portal.db')
                        cursor = conn.cursor()
                        cursor.execute("UPDATE students SET status_10th = 'Rejected' WHERE roll_no = ?", (r_no,))
                        conn.commit()
                        conn.close()
                        st.warning("10th Marksheet Rejected!")
                        st.rerun()

                    st.markdown("---")
                    # 12th Marksheet
                    st.write(f"**12th Marksheet Status:** `{s_12}`")
                    col_12_a, col_12_b, col_12_c = st.columns([2, 1, 1])
                    if m12:
                        col_12_a.download_button("Download 12th PDF", m12, file_name=f"12th_{r_no}.pdf", mime="application/pdf", key=f"dl_12_{r_no}")
                    else:
                        col_12_a.write("❌ Not Uploaded")
                    if col_12_b.button(f"Approve 12th", key=f"app_12_{r_no}"):
                        conn = sqlite3.connect('dsc_portal.db')
                        cursor = conn.cursor()
                        cursor.execute("UPDATE students SET status_12th = 'Approved' WHERE roll_no = ?", (r_no,))
                        conn.commit()
                        conn.close()
                        st.success("12th Marksheet Approved!")
                        st.rerun()
                    if col_12_c.button(f"Reject 12th", key=f"rej_12_{r_no}"):
                        conn = sqlite3.connect('dsc_portal.db')
                        cursor = conn.cursor()
                        cursor.execute("UPDATE students SET status_12th = 'Rejected' WHERE roll_no = ?", (r_no,))
                        conn.commit()
                        conn.close()
                        st.warning("12th Marksheet Rejected!")
                        st.rerun()

                    st.markdown("---")
                    # Transfer Certificate (TC)
                    st.write(f"**Transfer Certificate (TC) Status:** `{s_tc}`")
                    col_tc_a, col_tc_b, col_tc_c = st.columns([2, 1, 1])
                    if tc:
                        col_tc_a.download_button("Download TC PDF", tc, file_name=f"TC_{r_no}.pdf", mime="application/pdf", key=f"dl_tc_{r_no}")
                    else:
                        col_tc_a.write("❌ Not Uploaded")
                    if col_tc_b.button(f"Approve TC", key=f"app_tc_{r_no}"):
                        conn = sqlite3.connect('dsc_portal.db')
                        cursor = conn.cursor()
                        cursor.execute("UPDATE students SET status_tc = 'Approved' WHERE roll_no = ?", (r_no,))
                        conn.commit()
                        conn.close()
                        st.success("TC Approved!")
                        st.rerun()
                    if col_tc_c.button(f"Reject TC", key=f"rej_tc_{r_no}"):
                        conn = sqlite3.connect('dsc_portal.db')
                        cursor = conn.cursor()
                        cursor.execute("UPDATE students SET status_tc = 'Rejected' WHERE roll_no = ?", (r_no,))
                        conn.commit()
                        conn.close()
                        st.warning("TC Rejected!")
                        st.rerun()

                    st.markdown("---")
                    # Student Photo
                    st.write(f"**Student Photo Status:** `{s_ph}`")
                    col_ph_a, col_ph_b, col_ph_c = st.columns([2, 1, 1])
                    if ph:
                        col_ph_a.image(ph, width=120, caption="Uploaded Photo")
                    else:
                        col_ph_a.write("❌ Not Uploaded")
                    if col_ph_b.button(f"Approve Photo", key=f"app_ph_{r_no}"):
                        conn = sqlite3.connect('dsc_portal.db')
                        cursor = conn.cursor()
                        cursor.execute("UPDATE students SET status_photo = 'Approved' WHERE roll_no = ?", (r_no,))
                        conn.commit()
                        conn.close()
                        st.success("Photo Approved!")
                        st.rerun()
                    if col_ph_c.button(f"Reject Photo", key=f"rej_ph_{r_no}"):
                        conn = sqlite3.connect('dsc_portal.db')
                        cursor = conn.cursor()
                        cursor.execute("UPDATE students SET status_photo = 'Rejected' WHERE roll_no = ?", (r_no,))
                        conn.commit()
                        conn.close()
                        st.warning("Portal Photo Rejected!")
                        st.rerun()
        else:
            st.info("No student personal records or documents uploaded yet.")

    elif staff_menu == "🆔 ID Card Requests":
        st.subheader("🆔 Student ID Card Requests & Approvals")
        
        conn = sqlite3.connect('dsc_portal.db')
        cursor = conn.cursor()
        cursor.execute("SELECT roll_no, name, section, id_card_status FROM students WHERE id_card_status != 'Not Applied'")
        id_requests = cursor.fetchall()
        conn.close()
        
        if id_requests:
            for req in id_requests:
                r_no, name, sec, id_status = req
                c1, c2, c3 = st.columns([3, 3, 2])
                c1.write(f"**{name}** ({r_no}) — {sec}")
                c2.write(f"Status: `{id_status}`")
                
                if id_status == 'Pending Approval':
                    if c3.button(f"Approve ID {r_no}", key=f"app_id_{r_no}"):
                        conn = sqlite3.connect('dsc_portal.db')
                        cursor = conn.cursor()
                        cursor.execute("UPDATE students SET id_card_status = 'Approved' WHERE roll_no = ?", (r_no,))
                        conn.commit()
                        conn.close()
                        st.success(f"ID Card approved for {name}!")
                        st.rerun()
                else:
                    c3.write("✅ Approved")
        else:
            st.info("No pending ID card applications found.")

    elif staff_menu == "⚙️ Admin Profile & Photo":
        st.subheader("⚙️ Faculty Profile Settings & Photo Update")
        st.write(f"Currently Logged in Faculty ID: **{st.session_state.identifier}** ({st.session_state.username})")
        
        with st.form("admin_photo_update_form"):
            new_admin_photo = st.file_uploader("Upload New Profile Photo for Faculty", type=["jpg", "png", "jpeg"])
            submit_admin_photo = st.form_submit_button("Update My Profile Photo")
            
            if submit_admin_photo:
                if new_admin_photo:
                    admin_photo_bytes = new_admin_photo.read()
                    conn = sqlite3.connect('dsc_portal.db')
                    cursor = conn.cursor()
                    cursor.execute("UPDATE admins SET photo = ? WHERE admin_id = ?", (admin_photo_bytes, st.session_state.identifier))
                    conn.commit()
                    conn.close()
                    st.success("Profile photo updated successfully! Refreshing...")
                    st.rerun()
                else:
                    st.error("Please select an image file first.")

    elif staff_menu == "📊 Attendance Management":
        st.subheader("📋 Student Attendance Management & Tracking")
        st.selectbox("Section Select", ["Section AJ", "Section AW"])
        if st.button("Export"):
            st.success("Exported!")

    elif staff_menu == "📝 Quiz & Test Creator":
        st.subheader("✍️ Quiz & Assessment Creator")
        st.text_input("Title")
        st.button("Publish")

    elif staff_menu == "💻 Code Challenges Management":
        st.subheader("⚡ Coding Challenges")
        st.text_input("Problem")
        st.button("Deploy")

if __name__ == "__main__":
    main()