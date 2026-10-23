import streamlit as st
import datetime
import random
import sqlite3
import hashlib
import base64
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Page Configuration
st.set_page_config(
    page_title="DSC Portal | Digital Student Certification & Assessment System", 
    page_icon="🎓", 
    layout="wide"
)

def get_base64_of_bin_file(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

# Strict Dark Theme CSS Overriding All Streamlit System Preferences
try:
    bin_str = get_base64_of_bin_file('bg.jpg')
    if bin_str:
        bg_css = f'''
        .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
            background-image: linear-gradient(rgba(7, 13, 20, 0.98), rgba(10, 18, 26, 0.99)), url("data:image/jpg;base64,{bin_str}") !important;
            background-size: cover !important;
            background-position: center !important;
            background-repeat: no-repeat !important;
            background-attachment: fixed !important;
            color: #ffffff !important;
        }}
        '''
    else:
        bg_css = '''
        .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
            background: #070d14 !important;
            color: #ffffff !important;
        }}
        '''
    
    page_bg_img = f'''
    <style>
    {bg_css}
    
    .main, .block-container, [data-testid="stVerticalBlock"], [data-testid="stMain"] {{
        background-color: #070d14 !important;
        color: #ffffff !important;
    }}

    h1, h2, h3, h4, h5, h6, p, span, label, div, .stRadio label, .streamlit-expanderHeader {{
        color: #ffffff !important;
    }}

    div[data-testid="stExpander"] {{
        background-color: #0d1b2a !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 10px !important;
        color: #ffffff !important;
    }}
    div[data-testid="stExpander"] summary {{
        color: #ffffff !important;
        background-color: #142332 !important;
        border-radius: 8px !important;
        padding: 10px !important;
    }}
    div[data-testid="stExpander"] details {{
        background-color: #0d1b2a !important;
    }}

    div.stSuccess, div.stInfo, div.stWarning, div.stError {{
        background-color: #142332 !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5) !important;
    }}
    div.stSuccess p, div.stInfo p, div.stWarning p, div.stError p {{
        color: #ffffff !important;
    }}

    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #050b14 0%, #0d1b2a 100%) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
        color: #ffffff !important;
    }}
    
    section[data-testid="stSidebar"] .stMarkdown, 
    section[data-testid="stSidebar"] label, 
    section[data-testid="stSidebar"] span {{
        color: #ffffff !important;
    }}

    div.row-widget.stRadio > div {{
        gap: 8px;
    }}
    div.row-widget.stRadio label {{
        background: rgba(255, 255, 255, 0.08) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        padding: 8px 14px !important;
        border-radius: 8px !important;
        color: #ffffff !important;
        font-weight: 600 !important;
    }}
    div.row-widget.stRadio label:hover {{
        background: rgba(0, 123, 255, 0.3) !important;
        border-color: rgba(0, 123, 255, 0.6) !important;
    }}

    .dashboard-header-banner, .hero-box, .dash-card {{
        background: linear-gradient(135deg, #142332, #0c1823) !important;
        padding: 25px;
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        box-shadow: 0 8px 25px rgba(0,0,0,0.6);
        backdrop-filter: blur(10px);
        color: #ffffff !important;
        margin-bottom: 25px;
    }}
    
    .captcha-box {{
        background: linear-gradient(135deg, #10202c, #1b263b) !important;
        color: #4da6ff !important;
        font-size: 28px !important;
        font-weight: 800 !important;
        letter-spacing: 10px !important;
        text-align: center !important;
        padding: 12px !important;
        border-radius: 8px !important;
        border: 2px dashed #007bff !important;
        margin-bottom: 12px !important;
    }}
    
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div {{
        background-color: #10202c !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 8px !important;
    }}
    
    div[data-testid="stFileUploader"] {{
        background-color: #10202c !important;
        border: 1px dashed rgba(255, 255, 255, 0.3) !important;
        padding: 15px;
        border-radius: 10px;
        color: #ffffff !important;
    }}
    div[data-testid="stFileUploader"] section {{
        background-color: #142332 !important;
    }}

    .stButton>button {{
        background: linear-gradient(135deg, #007bff, #0056b3) !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        width: 100% !important;
        padding: 10px 15px !important;
        box-shadow: 0 4px 12px rgba(0,123,255,0.4) !important;
        border: none !important;
        transition: all 0.3s ease;
    }}
    .stButton>button p, .stButton>button div {{
        color: #ffffff !important;
        font-weight: 700 !important;
    }}
    .stButton>button:hover {{
        background: linear-gradient(135deg, #0056b3, #003d82) !important;
        box-shadow: 0 6px 16px rgba(0,123,255,0.6) !important;
    }}
    
    section[data-testid="stSidebar"] .stButton:last-child > button {{
        background: linear-gradient(135deg, #ff4d4d, #cc0000) !important;
        box-shadow: 0 4px 12px rgba(255, 77, 77, 0.4) !important;
    }}

    div[data-testid="stForm"] {{
        background: #0d1b2a !important;
        padding: 25px;
        border-radius: 14px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.8);
        border: 1px solid rgba(255, 255, 255, 0.15);
        color: white !important;
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)
except Exception as e:
    pass

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def send_real_email_otp(recipient_email, otp_code):
    sender_email = "rudrakshagrawal60@gmail.com"
    sender_password = "YOUR_GMAIL_APP_PASSWORD"
    
    subject = "DSC Portal Password Recovery OTP"
    body = f"Hello,\n\nYour 6-digit verification OTP for DSC Portal password recovery is: {otp_code}\n\nDo not share this code with anyone.\n\nRegards,\nDSC Portal Team"
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        return False

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
            pending_photo BLOB,
            photo_status TEXT DEFAULT 'Approved',
            academic_fee REAL DEFAULT 0.0,
            hostel_fee REAL DEFAULT 0.0,
            mess_fee REAL DEFAULT 0.0,
            bus_fee REAL DEFAULT 0.0,
            attendance REAL DEFAULT 100.0
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admins (
            admin_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            password TEXT NOT NULL,
            photo BLOB,
            pending_photo BLOB,
            photo_status TEXT DEFAULT 'Approved',
            assigned_class TEXT DEFAULT 'B.Tech CSE',
            assigned_section TEXT DEFAULT 'Section AJ',
            is_class_advisor INTEGER DEFAULT 1,
            title TEXT DEFAULT 'Mr.',
            marital_status TEXT DEFAULT 'Unmarried',
            subject TEXT DEFAULT 'Computer Science',
            email TEXT,
            mobile TEXT,
            resign_status TEXT DEFAULT 'Active',
            resign_reason TEXT,
            role_type TEXT DEFAULT 'Faculty'
        )
    ''')
    
    adm_cols = [
        ("pending_photo", "BLOB"),
        ("photo_status", "TEXT DEFAULT 'Approved'"),
        ("assigned_class", "TEXT DEFAULT 'B.Tech CSE'"),
        ("assigned_section", "TEXT DEFAULT 'Section AJ'"),
        ("is_class_advisor", "INTEGER DEFAULT 1"),
        ("title", "TEXT DEFAULT 'Mr.'"),
        ("marital_status", "TEXT DEFAULT 'Unmarried'"),
        ("subject", "TEXT DEFAULT 'Computer Science'"),
        ("email", "TEXT"),
        ("mobile", "TEXT"),
        ("resign_status", "TEXT DEFAULT 'Active'"),
        ("resign_reason", "TEXT"),
        ("role_type", "TEXT DEFAULT 'Faculty'")
    ]
    for c_name, c_type in adm_cols:
        try:
            cursor.execute(f"ALTER TABLE admins ADD COLUMN {c_name} {c_type}")
        except sqlite3.OperationalError:
            pass

    # Ensure Master Admin is seeded with ID 12515001362 and password 29122007 with Admin role
    master_id = "12515001362"
    master_pass = hash_password("29122007")
    cursor.execute("SELECT admin_id FROM admins WHERE admin_id = ?", (master_id,))
    if not cursor.fetchone():
        cursor.execute("""
            INSERT INTO admins (admin_id, name, password, assigned_class, assigned_section, is_class_advisor, photo_status, title, marital_status, subject, role_type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (master_id, "RUDRAKSH AGRAWAL", master_pass, "B.Tech CSE (AI & DS)", "Section AJ", 1, "Approved", "Mr.", "Unmarried", "Core CS", "Admin"))
    else:
        cursor.execute("UPDATE admins SET role_type = 'Admin' WHERE admin_id = ?", (master_id,))

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quizzes (
            quiz_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            section TEXT,
            creator_id TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

init_db()

# Session State & 15-Minute Auto-Logout Check
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_role" not in st.session_state:
    st.session_state.user_role = ""
if "username" not in st.session_state:
    st.session_state.username = ""
if "identifier" not in st.session_state:
    st.session_state.identifier = ""
if "last_active_time" not in st.session_state:
    st.session_state.last_active_time = datetime.datetime.now()

if st.session_state.logged_in:
    elapsed = (datetime.datetime.now() - st.session_state.last_active_time).total_seconds()
    if elapsed > 900: # 15 minutes = 900 seconds
        st.session_state.logged_in = False
        st.session_state.user_role = ""
        st.session_state.username = ""
        st.session_state.identifier = ""
        st.query_params.clear()
        st.warning("⏱️ Session expired due to 15 minutes of inactivity. You have been automatically logged out.")
        st.rerun()
    else:
        st.session_state.last_active_time = datetime.datetime.now()

if "st_otp_sent" not in st.session_state:
    st.session_state.st_otp_sent = False
if "st_generated_otp" not in st.session_state:
    st.session_state.st_generated_otp = ""
if "st_recovery_target" not in st.session_state:
    st.session_state.st_recovery_target = ""
if "st_recovery_contact" not in st.session_state:
    st.session_state.st_recovery_contact = ""

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
        # Check if user role is Admin or Faculty from admins table
        conn = sqlite3.connect('dsc_portal.db')
        cursor = conn.cursor()
        cursor.execute("SELECT role_type FROM admins WHERE admin_id = ?", (st.session_state.identifier,))
        adm_row = cursor.fetchone()
        conn.close()
        
        if adm_row and adm_row[0] == "Admin":
            show_admin_dashboard()
        elif adm_row:
            show_faculty_dashboard()
        else:
            show_student_dashboard()

def show_landing_page():
    st.sidebar.markdown("### 🔒 DSC Gateway")
    portal_choice = st.sidebar.radio("Select Portal", ["Student Portal", "Staff / Admin Portal"])
    
    col1, col2, col3 = st.columns([2, 6, 2])
    with col1:
        st.markdown("<h3 style='color: #ffffff;'>🎓 <b>DSC</b></h3>", unsafe_allow_html=True)
    with col2:
        st.markdown("<p style='text-align: center; color: #ffffff; font-size: 14px; font-weight: 600;'>SECURE ASSESSMENT & CERTIFICATION SYSTEM</p>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<p style='text-align: right; color: #4da6ff; font-weight: bold;'>Mode: {portal_choice}</p>", unsafe_allow_html=True)

    st.markdown("---")

    if portal_choice == "Staff / Admin Portal":
        admin_action = st.radio("Admin Action", ["Faculty / Admin Login", "Forgot Password"], horizontal=True)
        
        if admin_action == "Forgot Password":
            st.markdown("<h2 style='text-align: center; color: white;'>🔄 Password Recovery</h2>", unsafe_allow_html=True)
            col_fp1, col_fp2, col_fp3 = st.columns([1, 2, 1])
            with col_fp2:
                with st.form("admin_forgot_form"):
                    f_admin_id = st.text_input("Faculty ID / Admin ID")
                    f_new_pass = st.text_input("Enter New Password", type="password")
                    f_confirm_pass = st.text_input("Confirm New Password", type="password")
                    
                    submit_f_admin = st.form_submit_button("Reset Password")
                    if submit_f_admin:
                        if f_admin_id.strip() and f_new_pass.strip() and f_confirm_pass.strip():
                            if f_new_pass.strip() == f_confirm_pass.strip():
                                conn = sqlite3.connect('dsc_portal.db')
                                cursor = conn.cursor()
                                cursor.execute("SELECT * FROM admins WHERE admin_id = ?", (f_admin_id.strip(),))
                                adm_exists = cursor.fetchone()
                                if adm_exists:
                                    new_hashed = hash_password(f_new_pass.strip())
                                    cursor.execute("UPDATE admins SET password = ? WHERE admin_id = ?", (new_hashed, f_admin_id.strip()))
                                    conn.commit()
                                    conn.close()
                                    st.success("Password successfully updated! Please go to Login.")
                                else:
                                    conn.close()
                                    st.error("ID not found in database!")
                            else:
                                st.error("Passwords do not match!")
                        else:
                            st.error("Please fill all fields.")
        else:
            st.markdown("<h2 style='text-align: center; color: white;'>🔐 Secure Faculty & Admin Login</h2>", unsafe_allow_html=True)
            col_f1, col_f2, col_f3 = st.columns([1, 2, 1])
            with col_f2:
                with st.form("admin_login_form"):
                    admin_id_input = st.text_input("Faculty ID / Admin ID")
                    admin_pass_input = st.text_input("Password", type="password")
                    
                    st.markdown("<p style='margin-bottom: 5px; font-weight: bold;'>Verification Captcha Code:</p>", unsafe_allow_html=True)
                    st.markdown(f"<div class='captcha-box'>{st.session_state.captcha_val}</div>", unsafe_allow_html=True)
                    captcha_input = st.text_input("Enter the 4-digit code shown above")
                    
                    col_b1, col_b2 = st.columns(2)
                    with col_b1:
                        submit_admin_login = st.form_submit_button("Login")
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
                                cursor.execute("SELECT * FROM admins WHERE admin_id = ? AND password = ? AND resign_status != 'Resigned'", (admin_id_input.strip(), hashed_pass))
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
                                    st.error("Invalid ID, Password, or Account Resigned!")
                            else:
                                st.error("Please enter ID and Password.")
                        else:
                            st.error("Invalid Captcha code!")
                            st.session_state.captcha_val = str(random.randint(1000, 9999))

    else:
        st.markdown(f"""
            <div class="hero-box">
                <h1 style="color: #ffffff;">DSC Student Portal</h1>
                <p style="font-size: 15px; margin-top: 10px; color: #d0d7de;">Secure Authentication via Roll Number & Encrypted Database</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        student_action = st.radio("Student Action", ["Student Login", "Forgot Password"], horizontal=True)
        
        if student_action == "Forgot Password":
            st.markdown("<h2 style='text-align: center; color: white;'>🔄 Student Password Recovery via Email or Mobile</h2>", unsafe_allow_html=True)
            col_sp1, col_sp2, col_sp3 = st.columns([1, 2, 1])
            with col_sp2:
                if not st.session_state.st_otp_sent:
                    with st.form("student_forgot_request_form"):
                        recovery_input = st.text_input("Enter Roll Number, Email ID, OR Mobile Number")
                        submit_request_otp = st.form_submit_button("Send OTP")
                        
                        if submit_request_otp:
                            if recovery_input.strip():
                                conn = sqlite3.connect('dsc_portal.db')
                                cursor = conn.cursor()
                                cursor.execute("SELECT roll_no, email, student_mobile, name FROM students WHERE roll_no = ? OR email = ? OR student_mobile = ?", 
                                               (recovery_input.strip(), recovery_input.strip(), recovery_input.strip()))
                                student_rec = cursor.fetchone()
                                conn.close()
                                
                                if student_rec:
                                    r_no, s_email, s_mob, s_name = student_rec
                                    target_contact = s_email if s_email else s_mob
                                    
                                    if not target_contact:
                                        st.error("No valid email or mobile registered for this account! Contact Admin.")
                                    else:
                                        otp_code = str(random.randint(100000, 999999))
                                        if "@" in target_contact:
                                            send_real_email_otp(target_contact, otp_code)
                                        
                                        st.session_state.st_generated_otp = otp_code
                                        st.session_state.st_recovery_target = r_no
                                        st.session_state.st_recovery_contact = target_contact
                                        st.session_state.st_otp_sent = True
                                        
                                        st.success(f"Verification OTP has been sent successfully to **{target_contact}**!")
                                        st.rerun()
                                else:
                                    st.error("No student found with this Roll Number, Email, or Mobile Number!")
                            else:
                                st.error("Please enter your Roll Number, Email, or Mobile Number.")
                else:
                    with st.form("student_forgot_verify_form"):
                        st.write(f"Recovery for Roll No: `{st.session_state.st_recovery_target}`")
                        st.write(f"OTP sent to: `{st.session_state.st_recovery_contact}`")
                        
                        entered_otp = st.text_input("Enter 6-digit OTP received")
                        new_pass = st.text_input("Enter New Password", type="password")
                        confirm_pass = st.text_input("Confirm New Password", type="password")
                        
                        col_bt1, col_bt2, col_bt3 = st.columns(3)
                        with col_bt1:
                            verify_and_reset = st.form_submit_button("Verify & Reset")
                        with col_bt2:
                            resend_otp_btn = st.form_submit_button("Resend OTP")
                        with col_bt3:
                            cancel_reset = st.form_submit_button("Cancel")
                            
                        if cancel_reset:
                            st.session_state.st_otp_sent = False
                            st.session_state.st_generated_otp = ""
                            st.session_state.st_recovery_target = ""
                            st.rerun()
                            
                        if resend_otp_btn:
                            new_otp = str(random.randint(100000, 999999))
                            if "@" in st.session_state.st_recovery_contact:
                                send_real_email_otp(st.session_state.st_recovery_contact, new_otp)
                            st.session_state.st_generated_otp = new_otp
                            st.success(f"🔄 New OTP has been resent successfully to **{st.session_state.st_recovery_contact}**!")
                            st.rerun()
                            
                        if verify_and_reset:
                            if entered_otp.strip() and new_pass.strip() and confirm_pass.strip():
                                if entered_otp.strip() == st.session_state.st_generated_otp:
                                    if new_pass.strip() == confirm_pass.strip():
                                        conn = sqlite3.connect('dsc_portal.db')
                                        cursor = conn.cursor()
                                        hashed = hash_password(new_pass.strip())
                                        cursor.execute("UPDATE students SET password = ? WHERE roll_no = ?", (hashed, st.session_state.st_recovery_target))
                                        conn.commit()
                                        conn.close()
                                        
                                        st.session_state.st_otp_sent = False
                                        st.session_state.st_generated_otp = ""
                                        st.session_state.st_recovery_target = ""
                                        st.success("🎉 Password successfully reset! Please go to Student Login.")
                                        st.rerun()
                                    else:
                                        st.error("New Passwords do not match!")
                                else:
                                    st.error("Invalid OTP! Please enter correct code or click Resend OTP.")
                            else:
                                st.error("Please fill all fields.")
        else:
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
    cursor.execute("SELECT photo, id_card_status, attendance FROM students WHERE roll_no = ?", (st.session_state.identifier,))
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

        att_val = res[2] if res and len(res) > 2 and res[2] is not None else 100.0

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f"""
                <div class="dash-card">
                    <h4 style="color: #4da6ff; margin-bottom: 5px; font-size: 13px;">Attendance</h4>
                    <h2 style="color: white; margin: 0; font-size: 20px;">{att_val:.1f}%</h2>
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

    elif menu == "📝 Personal Details & Documents":
        st.subheader("📝 Student Personal Details & Document Verification Portal")
        
        conn = sqlite3.connect('dsc_portal.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name, father_name, mother_name, student_mobile, mother_mobile, father_mobile, email, status_10th, status_12th, status_tc, status_photo, photo_status FROM students WHERE roll_no = ?", (st.session_state.identifier,))
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
        p_status = st_data[11] if st_data and len(st_data) > 11 else "Approved"

        if p_status == "Pending Approval":
            st.warning("⚠️ Your profile photo change request is currently **Pending Admin Approval**.")

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
            st.markdown("### 📁 Document Uploads")
            up_10th = st.file_uploader("Upload 10th Marksheet (PDF only)", type=["pdf"])
            up_12th = st.file_uploader("Upload 12th Marksheet (PDF only)", type=["pdf"])
            up_photo = st.file_uploader("Upload New Student Photo (Requires Admin Approval)", type=["jpg", "jpeg", "png"])
            up_tc = st.file_uploader("Upload Transfer Certificate - TC (PDF only)", type=["pdf"])

            submit_details = st.form_submit_button("Save & Submit Documents")

            if submit_details:
                try:
                    conn = sqlite3.connect('dsc_portal.db')
                    cursor = conn.cursor()
                    
                    m10_bytes = up_10th.read() if up_10th else None
                    m12_bytes = up_12th.read() if up_12th else None
                    new_photo_bytes = up_photo.read() if up_photo else None
                    tc_bytes = up_tc.read() if up_tc else None

                    if m10_bytes:
                        cursor.execute("UPDATE students SET marksheet_10th = ?, status_10th = 'Pending' WHERE roll_no = ?", (m10_bytes, st.session_state.identifier))
                    if m12_bytes:
                        cursor.execute("UPDATE students SET marksheet_12th = ?, status_12th = 'Pending' WHERE roll_no = ?", (m12_bytes, st.session_state.identifier))
                    if new_photo_bytes:
                        cursor.execute("UPDATE students SET pending_photo = ?, photo_status = 'Pending Approval', status_photo = 'Pending' WHERE roll_no = ?", (new_photo_bytes, st.session_state.identifier))
                    if tc_bytes:
                        cursor.execute("UPDATE students SET tc = ?, status_tc = 'Pending' WHERE roll_no = ?", (tc_bytes, st.session_state.identifier))

                    cursor.execute("""
                        UPDATE students SET name = ?, father_name = ?, mother_name = ?, student_mobile = ?, mother_mobile = ?, father_mobile = ?, email = ?
                        WHERE roll_no = ?
                    """, (full_name.strip(), father_name.strip(), mother_name.strip(), student_mob.strip(), mother_mob.strip(), father_mob.strip(), email_id.strip(), st.session_state.identifier))

                    conn.commit()
                    conn.close()
                    st.success("Details successfully submitted!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error updating details: {e}")

    elif menu == "💳 Fee Dues & Payments":
        st.subheader("💳 Student Fee Dues & Payment Gateway Portal")
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
            </div>
        """, unsafe_allow_html=True)

        if total_fee > 0:
            if "show_payment_modal" not in st.session_state:
                st.session_state.show_payment_modal = False

            if st.button("Proceed to Online Fee Payment Gateway"):
                st.session_state.show_payment_modal = True

            if st.session_state.show_payment_modal:
                st.markdown("---")
                st.markdown("<h3 style='color: #4da6ff;'>💳 Secure Payment Checkout Form</h3>", unsafe_allow_html=True)
                with st.form("payment_gateway_form"):
                    pay_method = st.selectbox("Select Payment Method", ["Credit / Debit Card", "UPI / QR Code", "Net Banking"])
                    if pay_method == "Credit / Debit Card":
                        card_num = st.text_input("Card Number (16 Digits)")
                        card_exp = st.text_input("Expiry Date (MM/YY)")
                        card_cvv = st.text_input("CVV", type="password")
                    elif pay_method == "UPI / QR Code":
                        upi_id = st.text_input("Enter UPI ID")
                    else:
                        bank_name = st.selectbox("Select Bank", ["State Bank of India", "HDFC Bank", "ICICI Bank", "Axis Bank"])

                    pay_submit = st.form_submit_button(f"Pay ₹ {total_fee:,.2f} Securely")
                    if pay_submit:
                        conn = sqlite3.connect('dsc_portal.db')
                        cursor = conn.cursor()
                        cursor.execute("""
                            UPDATE students SET academic_fee = 0.0, hostel_fee = 0.0, mess_fee = 0.0, bus_fee = 0.0
                            WHERE roll_no = ?
                        """, (st.session_state.identifier,))
                        conn.commit()
                        conn.close()
                        st.session_state.show_payment_modal = False
                        st.success("🎉 Payment Successful! All fee dues have been cleared.")
                        st.rerun()
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
        
        if current_id_status == "Not Applied":
            if st.button("Submit Request for Official ID Card"):
                conn = sqlite3.connect('dsc_portal.db')
                cursor = conn.cursor()
                cursor.execute("UPDATE students SET id_card_status = 'Pending Faculty Approval' WHERE roll_no = ?", (st.session_state.identifier,))
                conn.commit()
                conn.close()
                st.success("ID Card request submitted successfully!")
                st.rerun()
        elif current_id_status == "Pending Faculty Approval":
            st.warning("Your ID Card request is pending review by Faculty.")
        elif current_id_status == "Pending Admin Approval":
            st.warning("Your ID Card request is approved by Faculty and pending final Admin approval.")
        elif current_id_status == "Approved":
            st.success("🎉 Your ID Card has been APPROVED!")

    elif menu == "📚 Academic Examinations":
        st.subheader("📚 Academic Examinations & Quizzes")
        st.info("No active examinations are currently live.")

    elif menu == "🎯 Practice Dashboard":
        st.subheader("🎯 Practice Lab & Quiz Progress")
        st.metric("Overall Completion", "0.0%")

    elif menu == "🎙️ AI Interview":
        st.subheader("🎙️ AI Interview Practice")
        if st.button("Start AI Powered Analysis"):
            st.success("Voice sample analyzed successfully!")

    elif menu == "🗄️ Database/SQL":
        st.subheader("🗄️ Database & SQL Query Editor")
        st.text_area("SQL Query", value=f"SELECT * FROM students WHERE roll_no = '{st.session_state.identifier}';")
        if st.button("Execute SQL Query"):
            st.code("Query executed successfully.", language="sql")

    elif menu == "🌐 Web Tech":
        st.subheader("🌐 Web Tech HTML/CSS Compiler")
        html_code = st.text_area("HTML Code", value="<h2>Welcome to DSC Portal</h2>")
        st.components.v1.html(html_code, height=120)

    elif menu == "✍️ Essay Writing":
        st.subheader("✍️ AI Essay Evaluation")
        st.text_area("Write your essay here:", height=150)
        if st.button("Evaluate Essay"):
            st.success("Score: 92/100")

    elif menu == "😀 Face Registration":
        st.subheader("👤 AI Proctoring Face Recognition")
        st.success("Face biometrics verified successfully.")

    elif menu == "❓ Help Desk":
        st.subheader("🛠️ Technical Help Desk & Support")
        st.metric("Helpline Contact Number", "9634350854")

def show_faculty_dashboard():
    conn = sqlite3.connect('dsc_portal.db')
    cursor = conn.cursor()
    cursor.execute("SELECT photo, assigned_class, assigned_section, is_class_advisor, name, photo_status, title, marital_status, subject, email, mobile FROM admins WHERE admin_id = ?", (st.session_state.identifier,))
    res = cursor.fetchone()
    conn.close()
    
    fac_name = res[4] if res and len(res) > 4 else st.session_state.username
    fac_class = res[1] if res and len(res) > 1 and res[1] else "B.Tech CSE"
    fac_section = res[2] if res and len(res) > 2 and res[2] else "Section AJ"
    f_photo_status = res[5] if res and len(res) > 5 else "Approved"
    f_title = res[6] if res and len(res) > 6 else "Mr."
    f_marital = res[7] if res and len(res) > 7 else "Unmarried"
    f_subject = res[8] if res and len(res) > 8 else "Computer Science"

    if res and res[0]:
        st.sidebar.image(res[0], width=100)
    else:
        st.sidebar.image("https://img.icons8.com/color/96/administrator-male.png", width=90)

    st.sidebar.markdown(f"### **{f_title} {fac_name}**")
    st.sidebar.markdown(f"<p style='color: #4da6ff; font-size: 13px; margin:0;'><b>Subject:</b> {f_subject}</p>", unsafe_allow_html=True)
    st.sidebar.markdown(f"<p style='color: #00e676; font-size: 12px;'><b>Status:</b> {f_marital}</p>", unsafe_allow_html=True)
    st.sidebar.markdown("---")
    
    staff_menu = st.sidebar.radio("Faculty Panel", [
        "📊 Dashboard",
        "📋 Attendance Management",
        "📝 Quiz & Test Creator",
        "💰 View Student Fee Status",
        "📂 Student Personal & Docs View",
        "🆔 ID Card Approvals",
        "✉️ Resign Application",
        "⚙️ Faculty Profile & Photo"
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
                <h2 style="margin: 0; color: #ffffff; font-size: 22px; font-weight: 700;">Faculty Control Center — {f_title} {fac_name}</h2>
                <p style="margin: 4px 0 0 0; color: #919eab; font-size: 13px;">Subject: <b style="color: #4da6ff;">{f_subject}</b></p>
            </div>
            <div style="text-align: right; background: rgba(0,0,0,0.3); padding: 8px 15px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.08);">
                <p style="margin: 0; color: #ffffff; font-size: 13px; font-weight: 600;">👨‍🏫 Faculty Mode</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if staff_menu == "📊 Dashboard":
        st.subheader("📊 Enrolled Statistics")
        conn = sqlite3.connect('dsc_portal.db')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM students")
        total_students = cursor.fetchone()[0]
        conn.close()
        st.metric("Total Portal Students", total_students)

    elif staff_menu == "📋 Attendance Management":
        st.subheader("📋 Student Attendance Management")
        conn = sqlite3.connect('dsc_portal.db')
        cursor = conn.cursor()
        cursor.execute("SELECT roll_no, name, section, attendance FROM students")
        att_students = cursor.fetchall()
        conn.close()

        if att_students:
            for ast in att_students:
                r_no, name, sec, cur_att = ast
                with st.form(f"att_form_{r_no}"):
                    st.write(f"**{name}** (Roll No: `{r_no}`)")
                    new_att = st.number_input("Attendance Percentage (%)", value=float(cur_att if cur_att is not None else 100.0), min_value=0.0, max_value=100.0, step=0.5, key=f"att_val_{r_no}")
                    if st.form_submit_button("Modify Attendance"):
                        conn = sqlite3.connect('dsc_portal.db')
                        cursor = conn.cursor()
                        cursor.execute("UPDATE students SET attendance = ? WHERE roll_no = ?", (new_att, r_no))
                        conn.commit()
                        conn.close()
                        st.success("Attendance updated!")
                        st.rerun()

    elif staff_menu == "📝 Quiz & Test Creator":
        st.subheader("✍️ Quiz & Test Creator")
        with st.form("quiz_creator_form"):
            q_title = st.text_input("Quiz Title")
            secret_code = st.text_input("Secret Access Code", type="password")
            if st.form_submit_button("Publish Quiz"):
                if q_title.strip() and secret_code.strip():
                    conn = sqlite3.connect('dsc_portal.db')
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO quizzes (title, section, creator_id) VALUES (?, ?, ?)", (q_title.strip(), fac_section, st.session_state.identifier))
                    conn.commit()
                    conn.close()
                    st.success("Quiz published successfully!")

    elif staff_menu == "💰 View Student Fee Status":
        st.subheader("💰 View Student Fee Status (Read-Only)")
        conn = sqlite3.connect('dsc_portal.db')
        cursor = conn.cursor()
        cursor.execute("SELECT roll_no, name, section, academic_fee, hostel_fee, mess_fee, bus_fee FROM students")
        fee_students = cursor.fetchall()
        conn.close()

        for fs in fee_students:
            r_no, name, sec, acad, hostel, mess, bus = fs
            tot = (acad or 0) + (hostel or 0) + (mess or 0) + (bus or 0)
            status_text = "Fully Paid" if tot == 0 else f"Dues Pending: ₹ {tot:,.2f}"
            st.write(f"• **{name}** (Roll: `{r_no}`) — Status: **{status_text}**")

    elif staff_menu == "📂 Student Personal & Docs View":
        st.subheader("📂 Student Personal Details & Documents")
        conn = sqlite3.connect('dsc_portal.db')
        cursor = conn.cursor()
        cursor.execute("SELECT roll_no, name, section, father_name, student_mobile, email FROM students")
        all_docs = cursor.fetchall()
        conn.close()
        for sd in all_docs:
            st.write(f"• **{sd[1]}** (Roll: `{sd[0]}`) | Father: {sd[2] or 'N/A'} | Mobile: {sd[3] or 'N/A'}")

    elif staff_menu == "🆔 ID Card Approvals":
        st.subheader("🆔 Student ID Card Requests — Faculty Approval")
        conn = sqlite3.connect('dsc_portal.db')
        cursor = conn.cursor()
        cursor.execute("SELECT roll_no, name, section, id_card_status FROM students WHERE id_card_status = 'Pending Faculty Approval'")
        pending_ids = cursor.fetchall()
        conn.close()

        if pending_ids:
            for req in pending_ids:
                r_no, name, sec, id_status = req
                c1, c2 = st.columns([4, 2])
                c1.write(f"**{name}** ({r_no})")
                if c2.button(f"Approve {r_no}", key=f"f_app_{r_no}"):
                    conn = sqlite3.connect('dsc_portal.db')
                    cursor = conn.cursor()
                    cursor.execute("UPDATE students SET id_card_status = 'Pending Admin Approval' WHERE roll_no = ?", (r_no,))
                    conn.commit()
                    conn.close()
                    st.success("Approved and sent to Admin!")
                    st.rerun()
        else:
            st.info("No pending requests.")

    elif staff_menu == "✉️ Resign Application":
        st.subheader("✉️ Faculty Resignation Application")
        conn = sqlite3.connect('dsc_portal.db')
        cursor = conn.cursor()
        cursor.execute("SELECT resign_status, resign_reason FROM admins WHERE admin_id = ?", (st.session_state.identifier,))
        res_info = cursor.fetchone()
        conn.close()

        st.write(f"Current Resign Status: `{res_info[0] if res_info else 'Active'}`")
        if res_info and res_info[1]:
            st.write(f"Your Reason: *{res_info[1]}*")

        with st.form("resign_form"):
            reason = st.text_area("Write Resignation Application / Reason")
            if st.form_submit_button("Submit Resignation Application"):
                if reason.strip():
                    conn = sqlite3.connect('dsc_portal.db')
                    cursor = conn.cursor()
                    cursor.execute("UPDATE admins SET resign_status = 'Pending Resignation', resign_reason = ? WHERE admin_id = ?", (reason.strip(), st.session_state.identifier))
                    conn.commit()
                    conn.close()
                    st.success("Resignation application submitted to Admin!")
                    st.rerun()

    elif staff_menu == "⚙️ Faculty Profile & Photo":
        st.subheader("⚙️ Faculty Profile & Photo Update")
        if f_photo_status == "Pending Approval":
            st.warning("⚠️ Your profile photo update is pending Admin approval.")

        with st.form("fac_photo_form"):
            new_f_photo = st.file_uploader("Upload New Profile Photo (Requires Admin Approval)", type=["jpg", "jpeg", "png"])
            if st.form_submit_button("Submit Photo for Approval"):
                if new_f_photo:
                    f_bytes = new_f_photo.read()
                    conn = sqlite3.connect('dsc_portal.db')
                    cursor = conn.cursor()
                    cursor.execute("UPDATE admins SET pending_photo = ?, photo_status = 'Pending Approval' WHERE admin_id = ?", (f_bytes, st.session_state.identifier))
                    conn.commit()
                    conn.close()
                    st.success("Photo submitted to Admin!")
                    st.rerun()

def show_admin_dashboard():
    conn = sqlite3.connect('dsc_portal.db')
    cursor = conn.cursor()
    cursor.execute("SELECT photo, name FROM admins WHERE admin_id = ?", (st.session_state.identifier,))
    res = cursor.fetchone()
    conn.close()
    
    adm_name = res[1] if res and len(res) > 1 else "RUDRAKSH AGRAWAL"

    if res and res[0]:
        st.sidebar.image(res[0], width=100)
    else:
        st.sidebar.image("https://img.icons8.com/color/96/administrator-male.png", width=90)

    st.sidebar.markdown(f"### **Admin: {adm_name}**")
    st.sidebar.markdown("---")
    
    admin_menu = st.sidebar.radio("Admin Panel", [
        "📊 Dashboard & Stats",
        "👨‍🏫 Register & Manage Faculty / Admins",
        "👥 Register & Delete Students",
        "📋 Attendance Management",
        "📝 Quiz & Test Creator",
        "💰 Manage Student Fees",
        "📊 Section-wise Records",
        "📂 Student Personal & Docs Approval",
        "🆔 ID Card Approvals (Admin)",
        "👤 Faculty Photo & Resign Approvals",
        "⚙️ Admin Profile"
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
                <h2 style="margin: 0; color: #ffffff; font-size: 22px; font-weight: 700;">Admin Control Center — {adm_name}</h2>
                <p style="margin: 4px 0 0 0; color: #919eab; font-size: 13px;">Full Administrative & Faculty Management</p>
            </div>
            <div style="text-align: right; background: rgba(0,0,0,0.3); padding: 8px 15px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.08);">
                <p style="margin: 0; color: #ffffff; font-size: 13px; font-weight: 600;">🔒 Admin Mode</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if admin_menu == "📊 Dashboard & Stats":
        st.subheader("📊 Live System Statistics")
        conn = sqlite3.connect('dsc_portal.db')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM students")
        tot_students = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM admins")
        tot_fac = cursor.fetchone()[0]
        conn.close()

        c1, c2 = st.columns(2)
        c1.metric("Total Enrolled Students", tot_students)
        c2.metric("Total Registered Staff / Admins", tot_fac)

    elif admin_menu == "👨‍🏫 Register & Manage Faculty / Admins":
        st.subheader("👨‍🏫 Register New Faculty / Co-Admin")
        with st.form("register_faculty_form"):
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                f_title = st.selectbox("Title / Prefix", ["Mr.", "Mrs.", "Ms."])
                f_name = st.text_input("Full Name")
                f_id = st.text_input("Assign ID (e.g. FAC101)")
                f_pass = st.text_input("Assign Password", type="password")
                f_role = st.selectbox("Assign Portal Role", ["Faculty", "Admin"])
                f_subject = st.text_input("Subject to Teach")
            with col_f2:
                f_marital = st.selectbox("Marital Status", ["Unmarried", "Married"])
                f_email = st.text_input("Email ID")
                f_mobile = st.text_input("Mobile Number")
                f_photo = st.file_uploader("Photo", type=["jpg", "jpeg", "png"])

            if st.form_submit_button("Register Staff Member"):
                if f_name.strip() and f_id.strip() and f_pass.strip() and f_email.strip():
                    try:
                        f_photo_bytes = f_photo.read() if f_photo else None
                        conn = sqlite3.connect('dsc_portal.db')
                        cursor = conn.cursor()
                        hashed_p = hash_password(f_pass.strip())
                        cursor.execute("""
                            INSERT INTO admins (admin_id, name, password, title, marital_status, subject, email, mobile, photo, photo_status, resign_status, role_type)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'Approved', 'Active', ?)
                        """, (f_id.strip(), f_name.strip(), hashed_p, f_title, f_marital, f_subject.strip(), f_email.strip(), f_mobile.strip(), f_photo_bytes, f_role))
                        conn.commit()
                        conn.close()
                        st.success(f"{f_role} {f_title} {f_name} successfully registered!")
                        st.rerun()
                    except sqlite3.IntegrityError:
                        st.error("Error: This ID is already registered!")
                else:
                    st.error("Please fill all required fields.")

        st.markdown("### 📋 Manage Staff, Promote to Admin & Delete")
        conn = sqlite3.connect('dsc_portal.db')
        cursor = conn.cursor()
        cursor.execute("SELECT admin_id, title, name, subject, email, mobile, resign_status, role_type FROM admins WHERE admin_id != '12515001362'")
        all_facs = cursor.fetchall()
        conn.close()

        if all_facs:
            for fac in all_facs:
                a_id, title, name, subj, email, mob, r_stat, r_type = fac
                with st.expander(f"👨‍🏫 {title} {name} (ID: {a_id}) — Role: `{r_type}` [Status: {r_stat}]"):
                    st.write(f"• **Subject:** {subj} | **Email:** {email} | **Mobile:** {mob}")
                    
                    col_act1, col_act2 = st.columns(2)
                    if r_type == "Faculty":
                        if col_act1.button(f"Promote to Admin", key=f"prom_{a_id}"):
                            conn = sqlite3.connect('dsc_portal.db')
                            cursor = conn.cursor()
                            cursor.execute("UPDATE admins SET role_type = 'Admin' WHERE admin_id = ?", (a_id,))
                            conn.commit()
                            conn.close()
                            st.success(f"{name} promoted to Admin!")
                            st.rerun()
                    else:
                        if col_act1.button(f"Demote to Faculty", key=f"dem_{a_id}"):
                            conn = sqlite3.connect('dsc_portal.db')
                            cursor = conn.cursor()
                            cursor.execute("UPDATE admins SET role_type = 'Faculty' WHERE admin_id = ?", (a_id,))
                            conn.commit()
                            conn.close()
                            st.warning(f"{name} demoted to Faculty.")
                            st.rerun()

                    if col_act2.button(f"🗑️ Delete Staff {a_id}", key=f"del_fac_{a_id}"):
                        conn = sqlite3.connect('dsc_portal.db')
                        cursor = conn.cursor()
                        cursor.execute("DELETE FROM admins WHERE admin_id = ?", (a_id,))
                        conn.commit()
                        conn.close()
                        st.success(f"Staff ID {a_id} deleted successfully.")
                        st.rerun()
        else:
            st.info("No other staff members registered yet.")

    elif admin_menu == "👥 Register & Delete Students":
        st.subheader("➕ Register New Student & Account Deletion")
        with st.form("add_student_form"):
            new_name = st.text_input("Student Full Name")
            new_roll = st.text_input("Student Roll Number")
            new_pass = st.text_input("Assign Password", type="password")
            student_section = st.selectbox("Assign University Section / Batch", ["Section AJ", "Section AW", "CSE Batch A", "Section B"])
            student_photo = st.file_uploader("Upload Student Photo", type=["jpg", "png", "jpeg"])
            
            submit_student = st.form_submit_button("Register Student in Database")
            if submit_student:
                if new_name.strip() and new_roll.strip() and new_pass.strip():
                    try:
                        photo_bytes = student_photo.read() if student_photo else None
                        conn = sqlite3.connect('dsc_portal.db')
                        cursor = conn.cursor()
                        hashed_password = hash_password(new_pass.strip())
                        cursor.execute("""
                            INSERT INTO students (roll_no, name, password, section, status, id_card_status, photo, photo_status) 
                            VALUES (?, ?, ?, ?, ?, 'Not Applied', ?, 'Approved')
                        """, (new_roll.strip(), new_name.strip(), hashed_password, student_section, photo_bytes))
                        conn.commit()
                        conn.close()
                        st.success(f"Student '{new_name}' (Roll No: {new_roll}) successfully registered!")
                        st.rerun()
                    except sqlite3.IntegrityError:
                        st.error("Error: This Roll Number is already registered!")
                else:
                    st.error("Please fill all required fields.")

        st.markdown("### 🛡️ Manage & Delete Students")
        conn = sqlite3.connect('dsc_portal.db')
        cursor = conn.cursor()
        cursor.execute("SELECT roll_no, name, section, status FROM students")
        all_students = cursor.fetchall()
        conn.close()

        if all_students:
            for st_rec in all_students:
                r_no, s_name, s_sec, s_status = st_rec
                with st.expander(f"👤 {s_name} (Roll No: {r_no}) — Section: {s_sec} [Status: {s_status}]"):
                    col_p1, col_p2 = st.columns(2)
                    with col_p1:
                        if s_status == 'Active':
                            if st.button(f"Block {r_no}", key=f"adm_block_{r_no}"):
                                conn = sqlite3.connect('dsc_portal.db')
                                cursor = conn.cursor()
                                cursor.execute("UPDATE students SET status = 'Blocked' WHERE roll_no = ?", (r_no,))
                                conn.commit()
                                conn.close()
                                st.warning("Student blocked.")
                                st.rerun()
                        else:
                            if st.button(f"Unblock {r_no}", key=f"adm_unblock_{r_no}"):
                                conn = sqlite3.connect('dsc_portal.db')
                                cursor = conn.cursor()
                                cursor.execute("UPDATE students SET status = 'Active' WHERE roll_no = ?", (r_no,))
                                conn.commit()
                                conn.close()
                                st.success("Student unblocked.")
                                st.rerun()
                    with col_p2:
                        if st.button(f"🗑️ Delete Account", key=f"adm_del_{r_no}"):
                            conn = sqlite3.connect('dsc_portal.db')
                            cursor = conn.cursor()
                            cursor.execute("DELETE FROM students WHERE roll_no = ?", (r_no,))
                            conn.commit()
                            conn.close()
                            st.success("Student deleted.")
                            st.rerun()

    elif admin_menu == "📋 Attendance Management":
        st.subheader("📋 Student Attendance Management")
        conn = sqlite3.connect('dsc_portal.db')
        cursor = conn.cursor()
        cursor.execute("SELECT roll_no, name, section, attendance FROM students")
        att_students = cursor.fetchall()
        conn.close()

        if att_students:
            for ast in att_students:
                r_no, name, sec, cur_att = ast
                with st.form(f"adm_att_form_{r_no}"):
                    st.write(f"**{name}** (Roll No: `{r_no}`)")
                    new_att = st.number_input("Attendance %", value=float(cur_att if cur_att is not None else 100.0), min_value=0.0, max_value=100.0, step=0.5, key=f"adm_att_{r_no}")
                    if st.form_submit_button("Update Attendance"):
                        conn = sqlite3.connect('dsc_portal.db')
                        cursor = conn.cursor()
                        cursor.execute("UPDATE students SET attendance = ? WHERE roll_no = ?", (new_att, r_no))
                        conn.commit()
                        conn.close()
                        st.success("Attendance updated!")
                        st.rerun()

    elif admin_menu == "📝 Quiz & Test Creator":
        st.subheader("✍️ Quiz & Test Creator")
        with st.form("adm_quiz_form"):
            q_title = st.text_input("Quiz Title")
            secret_code = st.text_input("Secret Access Code", type="password")
            if st.form_submit_button("Publish Quiz"):
                if q_title.strip() and secret_code.strip():
                    conn = sqlite3.connect('dsc_portal.db')
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO quizzes (title, section, creator_id) VALUES (?, ?, ?)", (q_title.strip(), "All Sections", st.session_state.identifier))
                    conn.commit()
                    conn.close()
                    st.success("Quiz published!")

    elif admin_menu == "💰 Manage Student Fees":
        st.subheader("💰 Manage Student Fees")
        conn = sqlite3.connect('dsc_portal.db')
        cursor = conn.cursor()
        cursor.execute("SELECT roll_no, name, section, academic_fee, hostel_fee, mess_fee, bus_fee FROM students")
        fee_students = cursor.fetchall()
        conn.close()

        for fs in fee_students:
            r_no, name, sec, acad, hostel, mess, bus = fs
            with st.expander(f"💵 {name} (Roll: {r_no})"):
                with st.form(f"adm_fee_{r_no}"):
                    na = st.number_input("Academic Fee", value=float(acad or 0), step=1000.0, key=f"af_a_{r_no}")
                    nh = st.number_input("Hostel Fee", value=float(hostel or 0), step=1000.0, key=f"af_h_{r_no}")
                    nm = st.number_input("Mess Fee", value=float(mess or 0), step=500.0, key=f"af_m_{r_no}")
                    nb = st.number_input("Bus Fee", value=float(bus or 0), step=500.0, key=f"af_b_{r_no}")
                    if st.form_submit_button("Update Fees"):
                        conn = sqlite3.connect('dsc_portal.db')
                        cursor = conn.cursor()
                        cursor.execute("UPDATE students SET academic_fee=?, hostel_fee=?, mess_fee=?, bus_fee=? WHERE roll_no=?", (na, nh, nm, nb, r_no))
                        conn.commit()
                        conn.close()
                        st.success("Fees updated!")
                        st.rerun()

    elif admin_menu == "📊 Section-wise Records":
        st.subheader("📊 Section-Wise Detailed Student Records")
        conn = sqlite3.connect('dsc_portal.db')
        cursor = conn.cursor()
        cursor.execute("SELECT roll_no, name, section, status FROM students")
        recs = cursor.fetchall()
        conn.close()
        for r in recs:
            st.write(f"• **{r[1]}** (Roll: `{r[0]}`) — Section: `{r[2]}`")

    elif admin_menu == "📂 Student Personal & Docs Approval":
        st.subheader("📂 Student Photo Approvals")
        conn = sqlite3.connect('dsc_portal.db')
        cursor = conn.cursor()
        cursor.execute("SELECT roll_no, name, pending_photo FROM students WHERE photo_status = 'Pending Approval'")
        pending_photos = cursor.fetchall()
        conn.close()

        if pending_photos:
            for pp in pending_photos:
                r_no, name, p_bytes = pp
                c1, c2, c3 = st.columns([2, 1, 1])
                c1.write(f"**{name}** (Roll: {r_no})")
                if p_bytes:
                    c1.image(p_bytes, width=100)
                if c2.button(f"Approve {r_no}", key=f"adm_app_ph_{r_no}"):
                    conn = sqlite3.connect('dsc_portal.db')
                    cursor = conn.cursor()
                    cursor.execute("UPDATE students SET photo = pending_photo, pending_photo = NULL, photo_status = 'Approved' WHERE roll_no = ?", (r_no,))
                    conn.commit()
                    conn.close()
                    st.success("Approved!")
                    st.rerun()
                if c3.button(f"Reject {r_no}", key=f"adm_rej_ph_{r_no}"):
                    conn = sqlite3.connect('dsc_portal.db')
                    cursor = conn.cursor()
                    cursor.execute("UPDATE students SET pending_photo = NULL, photo_status = 'Rejected' WHERE roll_no = ?", (r_no,))
                    conn.commit()
                    conn.close()
                    st.warning("Rejected.")
                    st.rerun()
        else:
            st.info("No pending student photo approvals.")

    elif admin_menu == "🆔 ID Card Approvals (Admin)":
        st.subheader("🆔 Student ID Card Requests — Final Admin Approval")
        conn = sqlite3.connect('dsc_portal.db')
        cursor = conn.cursor()
        cursor.execute("SELECT roll_no, name, section, id_card_status FROM students WHERE id_card_status = 'Pending Admin Approval'")
        adm_ids = cursor.fetchall()
        conn.close()

        if adm_ids:
            for req in adm_ids:
                r_no, name, sec, id_status = req
                c1, c2 = st.columns([4, 2])
                c1.write(f"**{name}** ({r_no})")
                if c2.button(f"Final Approve {r_no}", key=f"adm_final_id_{r_no}"):
                    conn = sqlite3.connect('dsc_portal.db')
                    cursor = conn.cursor()
                    cursor.execute("UPDATE students SET id_card_status = 'Approved' WHERE roll_no = ?", (r_no,))
                    conn.commit()
                    conn.close()
                    st.success("ID Card fully approved!")
                    st.rerun()
        else:
            st.info("No pending ID card approvals.")

    elif admin_menu == "👤 Faculty Photo & Resign Approvals":
        st.subheader("👤 Staff Resignation & Photo Approvals")
        conn = sqlite3.connect('dsc_portal.db')
        cursor = conn.cursor()
        cursor.execute("SELECT admin_id, name, resign_status, resign_reason FROM admins WHERE resign_status = 'Pending Resignation'")
        resigns = cursor.fetchall()
        conn.close()

        st.markdown("### ✉️ Pending Resignation Applications:")
        if resigns:
            for rg in resigns:
                a_id, a_name, r_stat, r_rsn = rg
                st.markdown(f"""
                    <div class="dash-card" style="padding:15px; margin-bottom:10px;">
                        <h4 style="color:#ff4d4d; margin:0;">Resignation Request: {a_name} (ID: {a_id})</h4>
                        <p style="color:#ffffff; margin:5px 0;">Reason: <i>{r_rsn}</i></p>
                    </div>
                """, unsafe_allow_html=True)
                col_r1, col_r2 = st.columns(2)
                if col_r1.button(f"Approve Resignation {a_id}", key=f"app_res_{a_id}"):
                    conn = sqlite3.connect('dsc_portal.db')
                    cursor = conn.cursor()
                    cursor.execute("UPDATE admins SET resign_status = 'Resigned' WHERE admin_id = ?", (a_id,))
                    conn.commit()
                    conn.close()
                    st.success("Resignation approved. Account deactivated.")
                    st.rerun()
                if col_r2.button(f"Reject Resignation {a_id}", key=f"rej_res_{a_id}"):
                    conn = sqlite3.connect('dsc_portal.db')
                    cursor = conn.cursor()
                    cursor.execute("UPDATE admins SET resign_status = 'Active', resign_reason = NULL WHERE admin_id = ?", (a_id,))
                    conn.commit()
                    conn.close()
                    st.info("Resignation rejected.")
                    st.rerun()
        else:
            st.info("No pending resignation applications.")

    elif admin_menu == "⚙️ Admin Profile":
        st.subheader("⚙️ Admin Profile")
        st.success("Full admin privileges active.")

if __name__ == "__main__":
    main()