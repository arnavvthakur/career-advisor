from flask import Blueprint, render_template, current_app, jsonify, g, request, redirect, url_for
from . import auth, models
import datetime
import json

main_bp = Blueprint('main', __name__)

# --- Quiz Recommendation Details Library ---
def get_recommendation_details(category_name):
    """Returns a detailed dictionary for a given career category name."""
    details = {
        # Post-10th Categories
        'PCM': {"title": "Science (PCM) Pathway", "description": "This pathway is for students with strong interests in Physics, Chemistry, and Mathematics. It is a prerequisite for careers in engineering, technology, and architecture.", "career_paths": ["Engineering", "Architecture", "Pure Sciences", "Data Science"], "exams": ["JEE Main & Advanced", "BITSAT", "NATA"]},
        'PCB': {"title": "Science (PCB) Pathway", "description": "This pathway is designed for students passionate about Physics, Chemistry, and Biology. It's the primary route for careers in medicine and life sciences.", "career_paths": ["Medical Sciences", "Biotechnology", "Pharmacy", "Research"], "exams": ["NEET", "AIIMS Entrance", "CUET"]},
        'Commerce': {"title": "Commerce Pathway", "description": "Ideal for students interested in business, finance, and accounting. It provides a strong foundation for corporate and entrepreneurial careers.", "career_paths": ["B.Com", "BBA", "Chartered Accountancy (CA)", "Financial Analyst"], "exams": ["CUET", "IPMAT", "CA Foundation"]},
        'Arts': {"title": "Arts / Humanities Pathway", "description": "A diverse pathway for students with an interest in social sciences, languages, and creative fields. It prepares you for careers in civil services, law, and media.", "career_paths": ["Civil Services (IAS/IPS)", "Law", "Journalism", "Fine Arts", "Psychology"], "exams": ["UPSC Civil Services Exam", "CLAT", "CUET", "NID/NIFT Entrance"]},
        
        # Post-12th PCM Categories
        'Engineering': {"title": "Engineering (B.Tech)", "description": "Focuses on applying scientific principles to design and build machines, structures, and systems.", "career_paths": ["Software Engineer", "Mechanical Engineer", "Civil Engineer", "Data Scientist"], "exams": ["JEE Main & Advanced", "BITSAT", "State CETs"]},
        'B.Sc.': {"title": "Pure Sciences (B.Sc.)", "description": "A foundational degree for careers in research and academia, focusing on deep theoretical knowledge.", "career_paths": ["Research Scientist", "Academic Professor", "Lab Manager"], "exams": ["CUET", "University Entrance"]},
        'Architecture': {"title": "Architecture (B.Arch)", "description": "A creative field focused on the art and science of designing buildings and physical structures.", "career_paths": ["Architect", "Urban Planner", "Interior Designer"], "exams": ["NATA", "JEE Main (Paper 2)"]},
        
        # Post-12th PCB Categories
        'Medical': {"title": "Medical Sciences (MBBS/BDS)", "description": "Prepares you for a career as a doctor or dentist, focusing on human health, diagnosis, and treatment.", "career_paths": ["Doctor (General Physician)", "Surgeon", "Dentist"], "exams": ["NEET", "AIIMS Entrance"]},
        'Biotech/Pharmacy': {"title": "Biotechnology / Pharmacy", "description": "This field uses living systems to create products, from medicines to biofuels.", "career_paths": ["Biotechnologist", "Pharmacist", "Clinical Researcher"], "exams": ["NEET", "State CETs"]},
        
        # Post-12th Commerce Categories
        'B.A. in Economics': {"title": "B.A. (Hons.) in Economics", "description": "Studies the production, distribution, and consumption of goods and services for careers in data analysis and policy research.", "career_paths": ["Economist", "Market Researcher", "Data Analyst"], "exams": ["CUET", "University Entrance Exams"]},
        'B.Com': {"title": "Bachelor of Commerce (B.Com)", "description": "A fundamental course in commerce and accounting, providing a strong base for a career in finance and business.", "career_paths": ["Accountant", "Financial Analyst", "Tax Consultant"], "exams": ["CET", "CUET"]},
        'BBA': {"title": "Bachelor of Business Administration (BBA)", "description": "Focuses on business management and administration, preparing students for leadership roles in corporate careers.", "career_paths": ["Marketing Manager", "HR Manager", "Business Analyst"], "exams": ["DU JAT", "IPU CET"]},
        'BBA LLB': {"title": "Integrated Law (BBA LLB)", "description": "Combines business administration with law, ideal for corporate law, governance, and policy roles.", "career_paths": ["Corporate Lawyer", "Legal Advisor", "Compliance Officer"], "exams": ["CLAT", "LSAT India"]},

        # Post-12th Arts Categories
        'B.A. in History/Political Science': {"title": "B.A. in History / Political Science", "description": "A great foundation for careers in civil services, research, and public policy.", "career_paths": ["Civil Servant (IAS/IPS)", "Policy Analyst", "Archivist"], "exams": ["UPSC Civil Services Exam", "CUET"]},
        'B.A. in Psychology': {"title": "B.A. in Psychology", "description": "Focuses on understanding human behavior, ideal for careers in counseling, HR, and social work.", "career_paths": ["Counselor", "HR Specialist", "Clinical Psychologist (with further studies)"], "exams": ["CUET", "University Entrance"]},
        'BFA': {"title": "Bachelor of Fine Arts (BFA)", "description": "A degree focused on visual and performing arts, perfect for creative individuals.", "career_paths": ["Graphic Designer", "Artist", "Animator", "Art Director"], "exams": ["NID Entrance Exam", "NIFT Entrance Exam"]},
        'B.A. in Journalism & Mass Communication': {"title": "B.A. in Journalism & Mass Communication", "description": "Teaches news reporting, media ethics, and public relations for a career in the media industry.", "career_paths": ["Reporter", "Editor", "PR Specialist", "Content Writer"], "exams": ["IPU CET", "University Entrance Exams"]},

        # Common Category
        'Management': {"title": "Business Management (BBA)", "description": "Focuses on the principles of business administration, leadership, and strategic planning.", "career_paths": ["Marketing Manager", "HR Manager", "Business Consultant"], "exams": ["CUET", "IPMAT", "University Entrance"]},
        'Law': {"title": "Law (Integrated LLB)", "description": "Prepares you for a career in the legal profession, focusing on argumentation, justice, and ethics.", "career_paths": ["Corporate Lawyer", "Litigator", "Judge"], "exams": ["CLAT", "AILET"]},
    }
    return details.get(category_name)


# --- Page Serving Routes ---

@main_bp.route('/')
def page_root():
    return redirect(url_for('main.page_welcome'))

@main_bp.route('/welcome')
def page_welcome():
    return render_template('welcome.html')

@main_bp.route('/login')
def page_login():
    return render_template('login.html')

@main_bp.route('/signup')
def page_signup():
    return render_template('signup.html')

@main_bp.route('/forgot-password')
def page_forgot_password():
    return render_template('forgot_password.html')

@main_bp.route('/dashboard')
def page_dashboard():
    return render_template('dashboard.html')

@main_bp.route('/profile')
def page_profile():
    return render_template('profile.html')

@main_bp.route('/courses')
def page_courses():
    return render_template('courses.html')

@main_bp.route('/colleges')
def page_colleges():
    return render_template('colleges.html')

@main_bp.route('/quiz-and-recommendations')
def page_quiz_and_recommendations():
    return render_template('quiz_and_recommendations.html')

@main_bp.route('/timeline')
def page_timeline():
    return render_template('timeline.html')

@main_bp.route('/scholarships')
def page_scholarships():
    return render_template('scholarships.html')

@main_bp.route('/help-info')
def page_help_info():
    return render_template('help_info.html')


# --- API Routes ---

@main_bp.route("/api/profile", methods=["GET", "PUT"])
@auth.auth_required
def api_profile():
    user = g.current_user
    if request.method == "GET":
        user_dict = {key: user[key] for key in user.keys() if key != 'password_hash'}
        return jsonify({"profile": user_dict})
    
    elif request.method == "PUT":
        data = request.get_json()
        if not data: return jsonify({"error": "No data provided"}), 400
        
        models.execute_db(
            """UPDATE users SET 
                name=?, dob=?, education=?, passout_year=?, stream=?, 
                address=?, phone=?, gender=?, academic_interests=? 
                WHERE id=?""",
            (data.get("name"), data.get("dob"), data.get("education"), 
             data.get("passout_year"), data.get("stream"), data.get("address"), 
             data.get("phone"), data.get("gender"), data.get("academic_interests"), user['id'])
        )
        return jsonify({"message": "Profile updated successfully!"}), 200

@main_bp.route("/api/recommendations", methods=["GET"])
@auth.auth_required
def api_recommendations():
    recs_json = models.query_db(
        "SELECT recommendations FROM quiz_recommendations WHERE user_id = ? ORDER BY created_at DESC LIMIT 1",
        [g.current_user['id']], one=True
    )
    if recs_json and recs_json['recommendations']:
        full_result = json.loads(recs_json['recommendations'])
        primary_recs = full_result.get("recommendations", {}).get("primary", [])
        return jsonify({"recommendations": primary_recs})
    return jsonify({"recommendations": []})

@main_bp.route("/api/courses", methods=["GET"])
@auth.auth_required
def api_courses():
    try:
        courses_data = json.loads(current_app.open_resource('data/courses.json').read())
        return jsonify(courses_data)
    except FileNotFoundError:
        return jsonify({"error": "Course data not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main_bp.route("/api/all_colleges", methods=["GET"])
@auth.auth_required
def api_all_colleges():
    """Fetches all college data."""
    try:
        all_colleges = json.loads(current_app.open_resource('data/colleges.json').read())
        return jsonify(all_colleges)
    except FileNotFoundError:
        return jsonify({"error": "College data file not found."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main_bp.route("/api/quiz-recommendations", methods=["POST"])
@auth.auth_required
def api_quiz_recommendations():
    data = request.get_json()
    answers = data.get('answers', {})
    user_id = g.current_user['id']
    education_level = data.get('education_level')

    if education_level == 'post10':
        score_categories = ['PCM', 'PCB', 'Commerce', 'Arts']
    else: # Post-12
        score_categories = [
            'Engineering', 'B.Sc.', 'Architecture', 'Management', 'Law', 'Medical', 
            'Biotech/Pharmacy', 'B.A. in Economics', 'B.Com', 'BBA', 'BBA LLB',
            'B.A. in History/Political Science', 'B.A. in Psychology', 'BFA',
            'B.A. in Journalism & Mass Communication'
        ]
    
    scores = {cat: 0 for cat in score_categories}
    
    for answer_category in answers.values():
        if answer_category in scores:
            scores[answer_category] += 1
    
    sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    
    recommendations = {"primary": [], "secondary": []}

    if sorted_scores and sorted_scores[0][1] > 0:
        top_score = sorted_scores[0][1]
        for stream, score in sorted_scores:
            if score == top_score:
                rec_detail = get_recommendation_details(stream)
                if rec_detail: recommendations["primary"].append(rec_detail)

    result_data = {"scores": scores, "recommendations": recommendations}

    if recommendations["primary"]:
        models.execute_db(
            "INSERT INTO quiz_recommendations (user_id, recommendations, created_at) VALUES (?, ?, ?)",
            (user_id, json.dumps(result_data), datetime.datetime.utcnow().isoformat())
        )
        
    return jsonify(result_data)


@main_bp.route("/api/last-quiz-result", methods=["GET"])
@auth.auth_required
def api_last_quiz_result():
    last_result = models.query_db(
        "SELECT recommendations FROM quiz_recommendations WHERE user_id = ? ORDER BY created_at DESC LIMIT 1",
        [g.current_user['id']], one=True
    )
    if last_result and last_result['recommendations']:
        return jsonify({"has_result": True, "result": json.loads(last_result['recommendations'])})
    else:
        return jsonify({"has_result": False})


@main_bp.route("/api/timeline/upcoming", methods=["GET"])
@auth.auth_required
def api_timeline_upcoming():
    timeline_data = models.query_db(
        "SELECT title, description, event_date FROM timelines WHERE user_id = ? AND event_date >= ? ORDER BY event_date ASC",
        (g.current_user['id'], datetime.date.today().isoformat())
    )
    return jsonify({"timeline": [dict(row) for row in timeline_data]})

@main_bp.route("/api/scholarships/search", methods=["GET"])
@auth.auth_required
def api_scholarships_search():
    query = request.args.get('q', '')
    search_term = f"%{query}%"
    scholarships_data = models.query_db(
        "SELECT title, eligibility, deadline, link FROM scholarships WHERE title LIKE ? OR eligibility LIKE ?",
        (search_term, search_term)
    )
    return jsonify({"scholarships": [dict(row) for row in scholarships_data]})

@main_bp.route("/api/feedback", methods=["POST"])
@auth.auth_required
def api_feedback():
    data = request.get_json()
    message = data.get('message')
    if not message: return jsonify({"error": "Message cannot be empty"}), 400
    
    models.execute_db(
        "INSERT INTO feedback (user_id, message, created_at) VALUES (?, ?, ?)",
        (g.current_user['id'], message, datetime.datetime.utcnow().isoformat())
    )
    return jsonify({"message": "Thank you for your feedback!"}), 201
