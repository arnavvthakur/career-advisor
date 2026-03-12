import sqlite3
import os
import datetime
import json
from werkzeug.security import generate_password_hash
from flask import current_app, g

# --- Database Connection and Helpers ---

def get_db():
    if 'db' not in g:
        db_path = current_app.config['DB_PATH']
        g.db = sqlite3.connect(db_path)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    db = get_db()
    cur = db.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def execute_db(query, args=()):
    db = get_db()
    cur = db.execute(query, args)
    db.commit()
    return cur.lastrowid

# --- Database Initialization and Seeding ---

def seed_data(db):
    """Seeds the database with general data like courses and scholarships."""
    current_app.logger.info("--- Checking for data to seed... ---")

    # Seed Courses
    if not db.execute('SELECT 1 FROM courses LIMIT 1').fetchone():
        current_app.logger.info("--- Seeding course data. ---")
        try:
            courses_data = json.loads(current_app.open_resource('data/courses.json').read())
            for pathway, sub_pathways in courses_data.items():
                for sub_pathway, courses_list in sub_pathways.items():
                    for course in courses_list:
                        db.execute(
                            'INSERT INTO courses (pathway, sub_pathway, stream, title, description, career_paths, exams) VALUES (?, ?, ?, ?, ?, ?, ?)',
                            (pathway, sub_pathway, sub_pathway, course['title'], course['description'], json.dumps(course.get('career_paths', [])), json.dumps(course.get('exams', [])))
                        )
        except Exception as e:
            current_app.logger.error(f"Could not seed courses: {e}")

    # Seed Scholarships with realistic data
    if not db.execute('SELECT 1 FROM scholarships LIMIT 1').fetchone():
        current_app.logger.info("--- Seeding scholarship data. ---")
        today = datetime.date.today()
        scholarships = [
            # National Scholarships
            ('National Scholarship Portal (NSP)', 'For students of all categories and states across India. Central Sector Schemes and UGC/AICTE Schemes.', (today + datetime.timedelta(days=60)).strftime('%Y-%m-%d'), 'https://scholarships.gov.in/'),
            ('Central Sector Scheme of Scholarship for College and University Students', 'National-level merit-based scholarship for students with a family income below ₹8 lakh per annum.', (today + datetime.timedelta(days=90)).strftime('%Y-%m-%d'), 'https://scholarships.gov.in/'),
            ('Merit-cum-Means Scholarship for Professional and Technical Courses', 'For minority communities (Muslims, Sikhs, Christians, etc.) across India with family income not exceeding ₹2.5 lakh.', (today + datetime.timedelta(days=75)).strftime('%Y-%m-%d'), 'https://scholarships.gov.in/'),
            ('Sitaram Jindal Scholarship Scheme', 'National-level scholarship for meritorious students from various streams, including ITI, Diploma, and Graduation.', (today + datetime.timedelta(days=120)).strftime('%Y-%m-%d'), 'https://www.sitaramjindalfoundation.org/scholarships.php'),
            ('AICTE Pragati Scholarship Scheme for Girls', 'National-level scholarship for meritorious girls pursuing technical education.', (today + datetime.timedelta(days=150)).strftime('%Y-%m-%d'), 'https://www.aicte-india.org/schemes/students-development-schemes/Pragati-Scholarship-Scheme-Girls'),

            # State-specific Scholarships
            ('Prime Minister\'s Special Scholarship Scheme (PMSSS)', 'For students from J&K and Ladakh pursuing higher education in other parts of India.', (today + datetime.timedelta(days=60)).strftime('%Y-%m-%d'), 'https://www.aicte-jk-scholarship-gov.in/'),
            ('E-PASS Scholarship (Andhra Pradesh)', 'For students from Andhra Pradesh belonging to SC, ST, BC, EBC, Differently Abled categories. Family income must be low.', (today + datetime.timedelta(days=75)).strftime('%Y-%m-%d'), 'https://jnanabhumi.ap.gov.in/'),
            ('Post Matric Scholarship for OBC Students (Uttar Pradesh)', 'For OBC students who are domiciles of Uttar Pradesh and have passed Class 10 or 12.', (today + datetime.timedelta(days=90)).strftime('%Y-%m-%d'), 'https://scholarship.up.gov.in/'),
            ('Post-Matric Scholarship Scheme (West Bengal)', 'For students of West Bengal who have passed the matriculation or higher secondary examination.', (today + datetime.timedelta(days=105)).strftime('%Y-%m-%d'), 'https://oasis.gov.in/'),
            ('Mukhyamantri Medhavi Vidyarthi Yojana (Madhya Pradesh)', 'For meritorious students of Madhya Pradesh who have secured good marks in Class 12.', (today + datetime.timedelta(days=120)).strftime('%Y-%m-%d'), 'https://scholarshipportal.mp.nic.in/'),
            ('Minority Scholarship (Maharashtra)', 'For minority students (Muslim, Christian, Sikh, etc.) who are domiciles of Maharashtra.', (today + datetime.timedelta(days=135)).strftime('%Y-%m-%d'), 'https://mahadbtmahait.gov.in/'),
            ('Karnataka State Scholarship Portal', 'For students of Karnataka belonging to various categories including SC/ST/OBC.', (today + datetime.timedelta(days=150)).strftime('%Y-%m-%d'), 'https://ssp.postmatric.karnataka.gov.in/'),
            ('Chief Minister\'s Scholarship Scheme (Tamil Nadu)', 'For students from Tamil Nadu based on merit and financial need.', (today + datetime.timedelta(days=165)).strftime('%Y-%m-%d'), 'https://www.tn.gov.in/scheme/123'),
            ('Bihar Post Matric Scholarship', 'For SC, ST, and BC/EBC students who are permanent residents of Bihar.', (today + datetime.timedelta(days=180)).strftime('%Y-%m-%d'), 'https://pmsonline.bih.nic.in/'),
            ('Gujarat E-Kalyan Scholarship', 'For SC/ST/OBC students of Gujarat, administered through the Digital Gujarat Portal.', (today + datetime.timedelta(days=195)).strftime('%Y-%m-%d'), 'https://www.digitalgujarat.gov.in/'),
            ('Kerala State Scholarship Portal', 'For meritorious students from various categories residing in Kerala.', (today + datetime.timedelta(days=210)).strftime('%Y-%m-%d'), 'http://dcescholarship.kerala.gov.in/'),
            ('Punjab Scholarship Scheme', 'For SC/ST students who are residents of Punjab, pursuing professional or technical courses.', (today + datetime.timedelta(days=225)).strftime('%Y-%m-%d'), 'http://www.scholarship.punjab.gov.in/')
        ]
        db.executemany('INSERT INTO scholarships (title, eligibility, deadline, link) VALUES (?, ?, ?, ?)', scholarships)
    
    db.commit()

def seed_default_timeline_for_user(db, user_id):
    """Seeds the database with a default set of timeline events for a new user."""
    current_app.logger.info(f"--- Seeding default timeline data for user_id: {user_id} ---")
    today = datetime.date.today()
    timeline_events = [
        (user_id, 'CLAT 2026 Application Deadline', 'For admission to National Law Universities (NLUs).', (today + datetime.timedelta(days=45)).strftime('%Y-%m-%d')),
        (user_id, 'JEE Main 2026 (Session 1) Registration Starts', 'For engineering, architecture, and planning undergraduate admissions.', (today + datetime.timedelta(days=55)).strftime('%Y-%m-%d')),
    ]
    db.executemany('INSERT INTO timelines (user_id, title, description, event_date) VALUES (?, ?, ?, ?)', timeline_events)

def create_or_get_mock_user(db):
    """Creates a mock user for testing and seeds their specific data."""
    email = current_app.config['MOCK_USER_EMAIL']
    user = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    
    if not user:
        current_app.logger.info(f"--- Creating mock user: {email} ---")
        pw_hash = generate_password_hash(current_app.config['MOCK_USER_PASSWORD'])
        
        user_id = db.execute(
            """INSERT INTO users (name, email, password_hash, created_at, education, stream, 
                                 gender, academic_interests, dob, current_class, phone, address, passout_year) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            ('Mock Student', email, pw_hash, datetime.datetime.utcnow().isoformat(), '12th Grade', 'Science',
             'Male', 'Physics, Computer Science', '2008-05-15', '12th', '9876543210', 'Hyderabad', '2026')
        ).lastrowid
    else:
        current_app.logger.info(f"--- Found existing mock user: {email} ---")
        user_id = user['id']
    
    # Make timeline seeding robust for development
    db.execute('DELETE FROM timelines WHERE user_id = ?', [user_id])
    current_app.logger.info(f"--- Cleared old timeline data for user_id: {user_id} ---")
    seed_default_timeline_for_user(db, user_id)
        
    db.commit()
    return user_id

def init_db(db):
    """Initializes the database using the schema.sql file and seeds it."""
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
    current_app.logger.info("--- Initialized database with schema. ---")
    seed_data(db)

def init_app(app):
    """Register database functions with the Flask app."""
    app.teardown_appcontext(close_db)

    with app.app_context():
        db = get_db()
        try:
            db.execute("SELECT 1 FROM users LIMIT 1").fetchone()
        except sqlite3.OperationalError:
            current_app.logger.info("--- 'users' table not found. Initializing database schema. ---")
            init_db(db)
        
        if app.config.get('MOCK_USER_MODE'):
            create_or_get_mock_user(db)
