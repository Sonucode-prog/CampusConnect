from datetime import timedelta
from datetime import date

from pathlib import Path #this is for handling file paths in a platform-independent way
from celery.result import AsyncResult

from flask_migrate import Migrate
from flask import Flask, request, jsonify, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename, send_from_directory
import os
import uuid #this is for generating unique identifiers for uploaded files
from models import *
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

from cache import cache
from cache_keys import job_cache_key
from cache_utils import refresh_cache
from cache_keys import student_job_cache_key

app = Flask(__name__) # Initialize Flask application

app.config["CACHE_TYPE"] = "RedisCache"
# app.config["CACHE_REDIS_URL"] = "redis://localhost:6379/0"
app.config["CACHE_REDIS_URL"] = os.getenv(
    "REDIS_URL",
    "redis://localhost:6379/0"
) #for render use the REDIS_URL environment variable, otherwise default to redis://localhost:6379/0
app.config["CACHE_DEFAULT_TIMEOUT"] = 300

cache.init_app(app)

migrate = Migrate(app, db)  # Initialize Flask-Migrate for database migrations

# Initialize the database with the Flask app context
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ppa.db'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'sqlite:///back_ppa.db'
)  #for render use the DATABASE_URL environment variable, otherwise default to sqlite:///back_ppa.db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=4)  # Set the expiration time for JWT tokens to 4 hours

frontend_url = os.getenv(
    "FRONTEND_URL",
    "http://localhost:5173"
)

CORS(
    app,
    resources={
        r"/*": {
            "origins": [frontend_url],
            "methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
        }
    }
)
 #CORS is for allowing cross-origin requests, which is necessary when the frontend and backend are on different domains or ports
jwt=JWTManager(app)

db.init_app(app) # Initialize the database with the Flask app context

# with app.app_context():  # Create the database tables based on the models defined in models.py
#     db.create_all()
#     admin=User.query.filter_by(username='admin').first()
#     print(admin)
#     if not admin:
#         admin_credential=User(
#             username='admin',
#             email='admin@example.com',
#             password=generate_password_hash('admin123'),
#             role='admin'
        
#     )
#         db.session.add(admin_credential)
#         db.session.commit()
        
#------------------------------------------------------------------------------------------------------------------------------------------------------

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data:
        return jsonify({"message": "No data received"}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    
    if not user:
        return jsonify({"message": "Invalid credentials"}), 401

    if not check_password_hash(user.password, data["password"]):
        return jsonify({"message": "Invalid credentials"}), 401

    if user.role == "student":
        student=Student.query.filter_by(user_id=user.user_id).first()
        if not student:
            return jsonify({"message": "Student profile not found"}), 404
        if student.status == "Deactivated":
            return jsonify({
                "message": "Your account has been deactivated."
            }), 403

        if student.status == "Blacklisted":
            return jsonify({
                "message": "Your account has been blacklisted."
            }), 403
    
    if user.role == "company":
        company = Company.query.filter_by(user_id=user.user_id).first()

        if not company:
            return jsonify({"message": "Company not found"}), 404

        if company.approval_status == "Pending":
            return jsonify({
                "message": "Your account is waiting for admin approval."
            }), 403

        if company.approval_status == "Rejected":
            return jsonify({
                "message": "Your company registration has been rejected."
            }), 403
            
        if company.approval_status == "Blocked":
            return jsonify({
                "message": "Your company registration has been blocked."
            }), 403

    access_token = create_access_token(
            identity=str(user.user_id), 
            additional_claims={
                "role": user.role
            }
        )
        
    return jsonify({
        'message': 'Login successful',
        "access_token": access_token,
        "user": {
            "user_id": user.user_id,
            "username": user.username,
            "role": user.role
        }
        }), 200

    
@app.route('/company/register', methods=['POST'])
def company_register():
    try:
        # Try to get parsed JSON first
        data = request.get_json()
        
        if not data:
            return jsonify({'message': 'No data receied'}), 400

        if User.query.filter_by(username=data['username']).first():
            return jsonify({'message': 'Username already exists'}), 400
        elif User.query.filter_by(email=data['email']).first():
            return jsonify({'message': 'email already exists'}), 400

        # Create the base User record first
        user = User(
            username=data['username'],
            email=data['email'],
            password=generate_password_hash(data['password']),
            role=data.get('role', 'company') #role defaults to 'company' if not provided
        )
        db.session.add(user)
        db.session.commit()

        # Create the company profile linked to the user
        company = Company(
            user_id=user.user_id,
            company_name=data.get('company_name', ''),
            location=data.get('location', ''),
            about_company=data.get('about_company',''),
            industry=data.get('industry', '')
            
        )
        db.session.add(company)
        db.session.commit()

        return jsonify({'message': 'User registered successfully'}), 200
    except Exception:
        app.logger.exception('Error in /company/register')
        return jsonify({'message': 'Internal server error'}), 500
    
    
@app.route('/student/register', methods=['POST'])
def register():
    try:
        # Try to get parsed JSON first
        data = request.get_json()
        
        if not data:
            return jsonify({'message': 'No data receied'}), 400

        if User.query.filter_by(username=data['username']).first():
            return jsonify({'message': 'Username already exists'}), 400
        elif User.query.filter_by(email=data['email']).first():
            return jsonify({'message': 'Email already exists'}), 400

        # Create the base User record first
        user = User(
            username=data['username'],
            email=data['email'],
            password=generate_password_hash(data['password']),
            role=data.get('role', 'student') #role defaults to 'company' if not provided
        )
        db.session.add(user)
        db.session.commit()  # commit to get user.user_id

        # Create the company profile linked to the user
        student = Student(
            user_id=user.user_id,
            full_name=data.get('full_name',''),
            branch=data.get('branch', ''),
            year=data.get('year',''),
            cgpa=data.get('cgpa',''),
            college=data.get('college', ''),
            phone=data.get('phone','')
        )
        db.session.add(student)
        db.session.commit()
        
        skills=Skill(
            student_id=student.student_id,
            skill=data.get('skill', '')
        )
        
        db.session.add(skills)
        db.session.commit()

        return jsonify({'message': 'User registered successfully'}), 200
    except Exception:
        app.logger.exception('Error in /student/register')
        return jsonify({'message': 'Internal server error'}), 500
    
#----------------------------------------------------------Admin-----------------------------------------------------------------------
@app.route("/api/admin/dashboard", methods=["GET"])
@jwt_required()
def admin_dashboard():

    students = Student.query.count()
    companies = Company.query.count()
    jobs = Job.query.count()
    applications = Application.query.count()
    placements = Application.query.filter_by(status="Selected").count()

    recent = []

    users = User.query.order_by(User.user_id.desc()).limit(10).all()

    for user in users:
        if user.role == "admin":
            continue  # Skip admin users
        recent.append({
            "id": user.user_id,
            "name": user.username,
            "role": user.role,
            "date": user.created_at.strftime("%d %b %Y"),
            "is_activated": user.is_active
        })

    return jsonify({
        "students": students,
        "companies": companies,
        "jobs": jobs,
        "applications": applications,
        "placements": placements,
        "recent_registrations": recent
    })
    
@app.route("/api/admin/companies", methods=["GET"])
@jwt_required()
def get_companies():

    companies = Company.query.all()

    return jsonify([
        {
            "company_id": company.company_id,
            "company_name": company.company_name,
            "email": company.user.email,
            "status": company.approval_status
        }
        for company in companies
    ])

@app.route("/api/admin/students", methods=["GET"])
@jwt_required()
def get_students():

    students = Student.query.all()

    return jsonify([
        {
            "student_id": student.student_id,
            "student_name": student.full_name,
            "email": student.user.email,
            
        }
        for student in students
    ])

@app.route("/api/admin/student/<int:student_id>", methods=["GET"])
@jwt_required()
def get_student(student_id):

    student = Student.query.get_or_404(student_id)

    user = User.query.get(student.user_id)

    resume = Resume.query.filter_by(student_id=student.student_id).first()

    applications = Application.query.filter_by(student_id=student.student_id).count()

    selected = Application.query.filter_by(
        student_id=student.student_id,
        status="Selected"
    ).count()

    interview = Application.query.filter_by(
        student_id=student.student_id,
        status="Interview"
    ).count()

    rejected = Application.query.filter_by(
        student_id=student.student_id,
        status="Rejected"
    ).count()

    return jsonify({
        "student_id": student.student_id,
        "username": user.username,
        "full_name": student.full_name,
        "email": user.email,
        "phone": student.phone,
        "branch": student.branch,
        "skills": student.skills.skill,
        "college":student.college,
        "year": student.year,
        "cgpa": student.cgpa,
        "status": student.status,
        "stats": {
            "applications": applications,
            "selected": selected,
            "interview": interview,
            "rejected": rejected
        }
    }), 200  
    
     
@app.route("/api/admin/student/<int:student_id>/status", methods=["PUT"])
@jwt_required()
def update_student_status(student_id):

    student = Student.query.get_or_404(student_id)

    data = request.get_json()

    status = data.get("status")

    valid_status = [
        "Active",
        "Deactivated",
        "Blacklisted"
    ]

    if status not in valid_status:
        return jsonify({
            "message": "Invalid status."
        }), 400

    student.status = status

    db.session.commit()

    return jsonify({
        "message": "Student status updated successfully."
    }), 200

@app.route("/api/admin/company/<int:company_id>", methods=["GET"])
@jwt_required()
def get_company(company_id):

    company = Company.query.get(company_id)

    if not company:
        return jsonify({
            "message": "Company not found"
        }), 404

    jobs = Job.query.filter_by(company_id=company.company_id).all()

    return jsonify({

        "company_id": company.company_id,
        "company_name": company.company_name,
        "email": company.user.email,
        "industry": company.industry,
        "location": company.location,
        "about_company": company.about_company,
        "status": company.approval_status,
        "jobs": [
            {
                "id": job.job_id,
                "title": job.title,
                "job_type": job.job_type,
                "salary": job.salary
            }
            for job in jobs
        ]

    }), 200
    
@app.route("/api/admin/company/<int:company_id>/status", methods=["PUT"])
@jwt_required()
def update_company_status(company_id):

    company = Company.query.get(company_id)

    if not company:
        return jsonify({
            "message": "Company not found"
        }), 404

    data = request.get_json()

    status = data.get("status")

    valid_status = [
        "Pending",
        "Approved",
        "Rejected",
        "Blocked"
    ]

    if status not in valid_status:
        return jsonify({
            "message": "Invalid Status"
        }), 400

    company.approval_status = status

    db.session.commit()

    return jsonify({
        "message": "Company status updated successfully."
    }), 200

#-----------------------------------------------------------User---------------------------------------------------------------------------
@app.route("/api/company/dashboard", methods=["GET"])
@jwt_required()
def company_dashboard():
    try:
        user_id = get_jwt_identity()

        company = Company.query.filter_by(user_id=user_id).first()
        if not company:
            return jsonify({"message": "Company not found"}), 404

        active_jobs = Job.query.filter_by(company_id=company.company_id).count()

        total_applications = Application.query.join(Job).filter(
            Job.company_id == company.company_id
        ).count()

        interviews = Application.query.join(Job).filter(
            Job.company_id == company.company_id,
            Application.status == "Interview"
        ).count()

        selected = Application.query.join(Job).filter(
            Job.company_id == company.company_id,
            Application.status == "Selected"
        ).count()

        applicants = (
            Application.query.join(Job).filter(Job.company_id == company.company_id)
            .order_by(Application.id.desc())   # or Application.created_at.desc()
            .limit(10)
            .all()
        )  #order them by the most recent application first:

        return jsonify({
            "company": {
                "id": company.company_id,
                "company_name": company.company_name,
                "email": company.user.email
            },
            "cards": {
                "active_jobs": active_jobs,
                "applications": total_applications,
                "interviews": interviews,
                "selected": selected
            },
            "applicants": [
                {
                    "id": application.student.student_id,
                    "name": application.student.full_name,
                    "college": application.student.college,
                    "status": application.status
                }
                for application in applicants
            ]
        })
    except Exception as e:
        app.logger.exception("Error in /api/company/dashboard")
        return jsonify({"error": str(e)}), 400
    
    
@app.route("/api/company/profile", methods=["GET"])
@jwt_required()
def get_company_profile():
    try:
        user_id = get_jwt_identity()

        company = Company.query.filter_by(user_id=user_id).first()

        if not company:
            return jsonify({"message": "Company not found"}), 404

        jobs = Job.query.filter_by(company_id=company.company_id).all()
        
        return jsonify({
            "company_id": company.company_id,
        "company_name": company.company_name,
        "email": company.user.email,
        "username": company.user.username,
        "industry": company.industry,
        "location": company.location,
        "about_company": company.about_company,
        "status": company.approval_status,
        "jobs": [
            {
                "id": job.job_id,
                "title": job.title,
                "job_type": job.job_type,
                "salary": job.salary
            }
            for job in jobs
        ]
        }), 200
    except Exception as e:
        app.logger.exception("Error in /api/company/profile GET")
        return jsonify({"error": str(e)}), 400


@app.route("/api/company/jobs", methods=["POST"])
@jwt_required()
def post_job():

    user_id = get_jwt_identity()
    company = Company.query.filter_by(user_id=user_id).first()

    if not company:
        return jsonify({
            "message": "Company not found."
        }), 404

    data = request.get_json()

    job = Job(
        company_id=company.company_id,
        title=data["title"],
        job_type=data["job_type"],
        location=data["location"],
        salary=data["salary"],
        experience=data["experience"],
        deadline=datetime.strptime(data["deadline"], "%Y-%m-%d").date(),
        cgpa=data["cgpa"],
        vacancies=data["vacancies"],
        skills=data["skills"],
        description=data["description"],
        status="Open",
        approve_status="Pending"  # Set the initial approval status to "Pending"
    )

    db.session.add(job)
    db.session.commit()
    
    refresh_cache("jobs") #this is for Refresh when job data changes 

    return jsonify({
        "message": "Job posted successfully."
    }), 201

#------------------------------------------------------Jobs----------------------------------------------------
@app.route("/api/jobs", methods=["GET"])
@jwt_required()
@cache.cached(timeout=300, make_cache_key=job_cache_key)
def get_jobs():

    user_id = get_jwt_identity()
    role = (User.query.filter_by(user_id=user_id).first()).role
    
    if role == "company":
        company = Company.query.filter_by(user_id=user_id).first()

        if not company:
            return jsonify({"message":"Company not found"}),404

        jobs = Job.query.filter_by(
            company_id=company.company_id
        ).order_by(Job.job_id.desc()).all()

    elif role == "admin":
        jobs = Job.query.order_by(Job.job_id.desc()).all()
        
    else:
        return jsonify({
            "message": "Unauthorized role"
        }), 403
    
    return jsonify([
        {
            "job_id":job.job_id,
            "company":job.company.company_name,
            "title":job.title,
            "job_type":job.job_type,
            "location":job.location,
            "vacancies":job.vacancies,
            "deadline":job.deadline,
            "status":job.status,
            "approve_status":job.approve_status
        }
        for job in jobs
    ]),200

@app.route("/api/jobs/<int:job_id>/close", methods=["PUT"])
@jwt_required()
def close_job(job_id):

    user_id = get_jwt_identity()
    role=(User.query.filter_by(user_id=user_id).first()).role
    
    if role == "company":
        company = Company.query.filter_by(user_id=user_id).first()

        if not company:
            return jsonify({"message":"Company not found"}),404

        job = Job.query.filter_by(
            job_id=job_id,
            company_id=company.company_id
        ).first()
        
        if not job:
            return jsonify({"message":"Job not found"}),404


    elif role == "admin":
        job = Job.query.get_or_404(job_id)
    
    job.status = "Closed"

    db.session.commit()
    refresh_cache("jobs") #this is for Refresh when job data changes

    return jsonify({
        "message":"Job closed successfully."
    }),200
    
@app.route("/api/jobs/<int:job_id>/open", methods=["PUT"])
@jwt_required()
def open_job(job_id):

    user_id = get_jwt_identity()
    role=(User.query.filter_by(user_id=user_id).first()).role

    if role == "company":
        company = Company.query.filter_by(user_id=user_id).first()

        if not company:
            return jsonify({"message":"Company not found"}),404

        job = Job.query.filter_by(
            job_id=job_id,
            company_id=company.company_id
        ).first()

        if not job:
            return jsonify({"message":"Job not found"}),404

    elif role == "admin":
        job = Job.query.get_or_404(job_id)
    job.status = "Open"

    db.session.commit()
    
    refresh_cache("jobs") #this is for Refresh when job data changes

    return jsonify({
        "message":"Job reopened successfully."
    }),200
    
@app.route("/api/jobs/<int:job_id>", methods=["DELETE"])
@jwt_required()
def delete_job(job_id):

    user_id = get_jwt_identity()
    role = (User.query.filter_by(user_id=user_id).first()).role

    if role == "company":
        company = Company.query.filter_by(user_id=user_id).first()

        if not company:
            return jsonify({"message":"Company not found"}),404

        job = Job.query.filter_by(
            job_id=job_id,
            company_id=company.company_id
        ).first()

        if not job:
            return jsonify({"message":"Job not found"}),404
        
    if role == "admin":
        job = Job.query.get_or_404(job_id)

    applications = Application.query.filter_by(job_id=job.job_id).count()
    

    if applications > 0:
        return jsonify({
            "message":"Job has applications. Close it instead of deleting."
        }),400

    db.session.delete(job)
    db.session.commit()
    
    refresh_cache("jobs") #this is for Refresh when job data changes

    return jsonify({
        "message":"Job deleted successfully."
    }),200
    
@app.route("/api/admin/jobs/<int:job_id>/approve",methods=["PUT"])
@jwt_required()
def approve_job(job_id):

    job = Job.query.get_or_404(job_id)

    job.approve_status = "Approved"

    db.session.commit()
    
    refresh_cache("jobs") #this is for Refresh when job data changes

    return jsonify({
        "message":"Job approved successfully."
    }),200
    
@app.route("/api/admin/jobs/<int:job_id>/reject",methods=["PUT"])
@jwt_required()
def reject_job(job_id):

    job = Job.query.get_or_404(job_id)

    job.approve_status = "Rejected"

    db.session.commit()
    
    refresh_cache("jobs") #this is for Refresh when job data changes

    return jsonify({
        "message":"Job rejected."
    }),200
    

@app.route("/api/applicants", methods=["GET"])
@jwt_required()
def get_applicants():

    user_id = get_jwt_identity()
    user = User.query.filter_by(user_id=user_id).first()
    
    # user_id = claims.get("user_id")
    role = user.role

    if role == "company":
        company = Company.query.filter_by(user_id=user_id).first()

        if not company:
            return jsonify({"message": "Company not found"}), 404

        jobs = Job.query.filter_by(company_id=company.company_id).all()

        applications = (
            Application.query
            .join(Job)
            .join(Student)
            .filter(Job.company_id == company.company_id)
            .order_by(Application.id.desc())
            .all()
        )

    elif role == "admin":

        jobs = Job.query.all()

        applications = (
            Application.query
            .join(Job)
            .join(Student)
            .join(Company)
            .order_by(Application.id.desc())
            .all()
        )

    else:
        return jsonify({
            "message": "Unauthorized"
        }), 403

    return jsonify({

        "jobs":[
            {
                "job_id":job.job_id,
                "title":job.title
            }
            for job in jobs
        ],

        "applicants":[
            {
                "application_id":application.id,
                "student_id":application.student.student_id,
                "student_name":application.student.full_name,
                "job_title":application.job.title,
                "company":application.job.company.company_name,
                "cgpa":application.student.cgpa,
                "applied_at":application.applied_at.strftime("%d-%m-%Y"),
                "status":application.status
            }
            for application in applications
        ]

    }),200
    

    
@app.route("/api/student/jobs", methods=["GET"])
@jwt_required()
@cache.cached(timeout=300, make_cache_key=student_job_cache_key)
def browse_jobs():

    user_id = get_jwt_identity()

    student = Student.query.filter_by(user_id=user_id).first()

    if not student:
        return jsonify({"message":"Student not found"}),404
    jobs = Job.query.filter_by(
    status="Open",
    approve_status="Approved"
    ).all()

    job_list = []

    for job in jobs:

        company = Company.query.get(job.company_id)

        application = Application.query.filter_by(
            student_id=student.student_id,
            job_id=job.job_id
        ).first()

        job_list.append({
            "job_id":job.job_id,
            "title":job.title,
            "company":company.company_name,
            "location":job.location,
            "job_type":job.job_type,
            "salary":job.salary,
            "cgpa":job.cgpa,
            "vacancies":job.vacancies,
            "deadline":job.deadline.strftime("%d-%m-%Y"),
            "description":job.description,
            "status":job.status,
            "deadline_passed":job.deadline < date.today(),
            "already_applied":True if application else False
        })

    return jsonify(job_list),200

@app.route("/api/student/apply/<int:job_id>", methods=["POST"])
@jwt_required()
def apply_job(job_id):

    user_id = get_jwt_identity()

    student = Student.query.filter_by(user_id=user_id).first()

    if not student:
        return jsonify({"message":"Student not found"}),404

    job = Job.query.get_or_404(job_id)

    # Company has closed the job
    if job.status == "Closed":
        return jsonify({"message":"This job is closed."}),400
    
    # Admin has not approved the job
    if job.approve_status != "Approved":
        return jsonify({
            "message":"This job is waiting for admin approval."
        }),400

    # Deadline check
    if job.deadline < date.today():
        return jsonify({"message":"Application deadline has passed."}),400

    already = Application.query.filter_by(
        student_id=student.student_id,
        job_id=job.job_id
    ).first()

    if already:
        return jsonify({"message":"You have already applied for this job."}),400

    application = Application(
        student_id=student.student_id,
        job_id=job.job_id,
        status="Pending"
    )

    db.session.add(application)
    db.session.commit()
    
    refresh_cache("applications")
    
    notification = Notification(
    user_id=student.user_id,
    message=f"You successfully applied for '{job.title}'."
    )

    db.session.add(notification)
    db.session.commit()

    return jsonify({
        "message":"Application submitted successfully."
    }),201
    
@app.route("/api/applicant/<int:application_id>", methods=["GET"])
@jwt_required()
def applicant_profile(application_id):
    application=Application.query.get_or_404(application_id)
    student=Student.query.get(application.student_id)
    user=User.query.get(student.user_id)
    job=Job.query.get(application.job_id)
    resume=Resume.query.filter_by(student_id=student.student_id).first()
    interview=Interview.query.filter_by(application_id=application.id).first()

    return jsonify({
        "application_id":application.id,
        "student_id":student.student_id,
        "full_name":student.full_name,
        "email":user.email,
        "phone":student.phone,
        "skills":student.skills.skill,
        "college":student.college,
        "branch":student.branch,
        "year":student.year,
        "cgpa":student.cgpa,
        "resume_name":resume.file_name if resume else "",
        "job_title":job.title,
        "job_type":job.job_type,
        "location":job.location,
        "status":application.status,
        "interview":{
            "interview_date":interview.interview_date.strftime("%d-%m-%Y"),
            "interview_time":interview.interview_time.strftime("%I:%M %p"),
            "interview_mode":interview.interview_mode,
            "meeting_link":interview.meeting_link,
            "location":interview.location
        } if interview else None,
        "placement":{
            "package":application.placement.package,
            "joining_date":application.placement.joining_date.strftime("%d-%m-%Y")
        } if application.placement else None
    }),200
    
@app.route("/api/application/<int:application_id>/status", methods=["PUT"])
@jwt_required()
def update_application_status(application_id):

    application = Application.query.get_or_404(application_id)

    data = request.get_json()

    status = data.get("status")

    valid_status = [
        "Pending",
        "Shortlisted",
        "Interview",
        "Selected",
        "Rejected"
    ]

    if status not in valid_status:
        return jsonify({
            "message":"Invalid Status"
        }),400

    if status == "Shortlisted":

        notification = Notification(
            user_id=application.student.user_id,
            message=f"You have been shortlisted for '{application.job.title}'."
        )

        db.session.add(notification)
    
    if status == "Interview":

        notification = Notification(
            user_id=application.student.user_id,
            message=f"You have been shortlisted for an interview for '{application.job.title}'."
        )

        db.session.add(notification)
    
    if status == "Selected":

        notification = Notification(
            user_id=application.student.user_id,
            message=f"Congratulations! You have been selected for '{application.job.title}'. Offer Letter sent you on your email "
        )

        db.session.add(notification)
    
    if status == "Rejected":

        notification = Notification(
            user_id=application.student.user_id,
            message=f"Your application for '{application.job.title}' has been rejected."
        )

        db.session.add(notification)
    
    application.status = status

    db.session.commit()
    
    

    return jsonify({
        "message":"Application status updated successfully."
    }),200
    
@app.route("/api/application/<int:application_id>/resume", methods=["GET"])
@jwt_required()
def company_download_resume(application_id):

    application = Application.query.get_or_404(application_id)

    resume = Resume.query.filter_by(student_id=application.student_id).first()

    if not resume:
        return jsonify({
            "message":"Resume not found."
        }),404

    return send_file(
        resume.file_path,
        as_attachment=True,
        download_name=resume.file_name
    )
    
@app.route("/api/company/applications/<int:application_id>/interview",methods=["POST"])
@jwt_required()
def schedule_interview(application_id):
    user_id=get_jwt_identity()
    company=Company.query.filter_by(user_id=user_id).first()
    if not company:
        return jsonify({"message":"Company not found"}),404
    application=Application.query.join(Job).filter(
        Application.id==application_id,
        Job.company_id==company.company_id
    ).first()
    if not application:
        return jsonify({"message":"Application not found"}),404
    if application.status not in ["Shortlisted","Interview"]:
        return jsonify({"message":"Student must be shortlisted before scheduling interview"}),400
    data=request.get_json()
    if not data.get("interview_date") or not data.get("interview_time") or not data.get("interview_mode"):
        return jsonify({"message":"Date, time and mode are required"}),400
    interview=Interview.query.filter_by(application_id=application.id).first()
    if interview:
        return jsonify({"message":"Interview already scheduled"}),400
    interview=Interview(
        application_id=application.id,
        interview_date=datetime.strptime(data["interview_date"],"%Y-%m-%d").date(),
        interview_time=datetime.strptime(data["interview_time"],"%H:%M").time(),
        interview_mode=data["interview_mode"],
        meeting_link=data.get("meeting_link"),
        location=data.get("location")
    )
    application.status="Interview"
    notification=Notification(
        user_id=application.student.user_id,
        message=f"Your interview for '{application.job.title}' has been scheduled."
    )
    db.session.add(interview)
    db.session.add(notification)
    db.session.commit()
    return jsonify({"message":"Interview scheduled successfully"}),201


@app.route("/api/student/dashboard", methods=["GET"])
@jwt_required()
def student_dashboard():
    
    try:

        user_id = get_jwt_identity()

        student = Student.query.filter_by(user_id=user_id).first()

        if not student:
            return jsonify({"message": "Student not found"}), 404

        total_jobs = Job.query.filter_by(approve_status="Approved").count()

        applied_jobs = Application.query.filter_by(
            student_id=student.student_id
        ).count()

        shortlisted = Application.query.filter_by(
            student_id=student.student_id,
            status="Shortlisted"
        ).count()

        interviews = Application.query.filter_by(
            student_id=student.student_id,
            status="Interview"
        ).count()

        jobs = Job.query.order_by(Job.job_id.desc()).limit(10).all()

        return jsonify({
            "student": {
                "id": student.student_id,
                "name": student.full_name,
                "email": student.user.email
            },
            "cards": [
                        {
                            "id": 1,
                            "title": "Applied Jobs",
                            "value": applied_jobs
                        },
                        {
                            "id": 2,
                            "title": "Interviews",
                            "value": interviews
                        },
                        {
                            "id": 3,
                            "title": "Shortlisted",
                            "value": shortlisted
                        },
                        {
                            "id": 4,
                            "title": "Total Jobs",
                            "value": total_jobs
                        }
                    ],
            "jobs": [
                {
                    "id": job.job_id,
                    "title": job.title,
                    "company": job.company.company_name,
                    "location": job.location,
                    "salary": job.salary,
                    "approve_status": job.approve_status,
                    "deadline": job.deadline.strftime("%d-%m-%Y"),
                }
                for job in jobs
            ]
        })
    except Exception as e:
        app.logger.exception("Error in /api/student/dashboard")
        return jsonify({"error": str(e)}), 400
    
@app.route("/api/student/profile", methods=["GET"])
@jwt_required()
def get_student_profile():
    try:
        user_id = get_jwt_identity()

        student = Student.query.filter_by(user_id=user_id).first()

        if not student:
            return jsonify({"message": "Student not found"}), 404

        return jsonify({
            "username": student.user.username,
            "email": student.user.email,
            "full_name": student.full_name,
            "branch": student.branch,
            "year": student.year,
            "cgpa": student.cgpa,
            "college": student.college,
            "skill": student.skills.skill,
            "phone": student.phone
        }), 200
    except Exception as e:
        app.logger.exception("Error in /api/student/profile GET")
        return jsonify({"error": str(e)}), 400
    
@app.route("/api/student/profile",methods=["PUT"])
@jwt_required()
def update_profile():
    
    try:

        user_id = get_jwt_identity()

        student = Student.query.filter_by(user_id=user_id).first()

        user = User.query.filter_by(user_id=user_id).first()

        if not student:
            return jsonify({"message":"Student not found"}),404

        data = request.get_json()

        data = request.get_json()

        if "full_name" in data:
            student.full_name = data["full_name"]

        if "branch" in data:
            student.branch = data["branch"]

        if "year" in data:
            student.year = data["year"]

        if "cgpa" in data:
            student.cgpa = data["cgpa"]

        if "phone" in data:
            student.phone = data["phone"]

        if "email" in data:
            email = data["email"].strip()

            if email and email != user.email:
                existing = User.query.filter_by(email=email).first()
                if existing:
                    return jsonify({"message": "Email already exists"}), 400

                user.email = email

        db.session.commit()

        return jsonify({
            "message":"Profile Updated Successfully"
        })
    except Exception as e:
        app.logger.exception("Error in /api/student/profile PUT")
        return jsonify({"error": str(e)}), 400
    
@app.route("/api/student/applications", methods=["GET"])
@jwt_required()
def student_applications():

    user_id = get_jwt_identity()

    student = Student.query.filter_by(user_id=user_id).first()

    if not student:
        return jsonify({
            "message":"Student not found."
        }),404

    applications = Application.query.filter_by(student_id=student.student_id).order_by(Application.applied_at.desc()).all()

    result = []

    for application in applications:

        job = Job.query.get(application.job_id)
        company = Company.query.get(job.company_id)

        result.append({
            "application_id":application.id,
            "company":company.company_name,
            "job_title":job.title,
            "job_type":job.job_type,
            "location":job.location,
            "salary":job.salary,
            "status":application.status,
            "applied_at":application.applied_at.strftime("%d-%m-%Y")
        })

    return jsonify(result),200

@app.route("/api/student/application/<int:application_id>", methods=["GET"])
@jwt_required()
def application_details(application_id):

    user_id = get_jwt_identity()

    student = Student.query.filter_by(user_id=user_id).first()

    application = Application.query.filter_by(
        id=application_id,
        student_id=student.student_id
    ).first()

    if not application:
        return jsonify({
            "message":"Application not found."
        }),404

    job = Job.query.get(application.job_id)
    company = Company.query.get(job.company_id)

    return jsonify({
        "application_id":application.id,
        "company_name":company.company_name,
        "industry":company.industry,
        "location":company.location,
        "job_title":job.title,
        "job_type":job.job_type,
        "salary":job.salary,
        "experience":job.experience,
        "description":job.description,
        "skills":job.skills,
        "deadline":job.deadline.strftime("%d-%m-%Y"),
        "applied_at":application.applied_at.strftime("%d-%m-%Y"),
        "status":application.status
    }),200

        
#----------------------------------------------------RESUME-----------------------------------------------------
@app.route("/api/student/resume", methods=["GET"])
@jwt_required()
def get_resume():

    user_id = get_jwt_identity()

    student = Student.query.filter_by(user_id=user_id).first()

    if not student:
        return jsonify({"message": "Student not found"}), 404

    resume = Resume.query.filter_by(student_id=student.student_id).first()

    if not resume:
        return jsonify({
            "file_name": None,
            "uploaded_at": None
        }), 200

    return jsonify({
        "file_name": resume.file_name,
        "uploaded_at": resume.uploaded_at
    }), 200
    
UPLOAD_FOLDER = "uploads/resumes"

ALLOWED_EXTENSIONS = {"pdf", "doc", "docx"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
# Create folder if it doesn't exist
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


def allowed_file(filename):
    return "." in filename and \
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/api/admin/student/<int:student_id>/resume", methods=["GET"])
@jwt_required()
def admin_download_resume(student_id):

    resume = Resume.query.filter_by(student_id=student_id).first()

    if not resume:
        return jsonify({
            "message": "Resume not found."
        }), 404

    return send_file(
        resume.file_path,
        as_attachment=True,
        download_name=resume.file_name
    )

@app.route("/api/student/resume", methods=["POST"])
@jwt_required()
def upload_resume():

    user_id = get_jwt_identity()

    student = Student.query.filter_by(user_id=user_id).first()

    if not student:
        return jsonify({"message": "Student not found"}), 404

    if "resume" not in request.files:
        return jsonify({"message": "No file selected"}), 400

    file = request.files["resume"]

    if file.filename == "":
        return jsonify({"message": "No file selected"}), 400

    if not allowed_file(file.filename):
        return jsonify({"message": "Invalid file type"}), 400

    extension = file.filename.rsplit(".", 1)[1].lower()

    stored_name = f"{uuid.uuid4()}.{extension}"

    file.save(os.path.join(app.config["UPLOAD_FOLDER"], stored_name))

    resume = Resume.query.filter_by(student_id=student.student_id).first()

    if resume:

        old_file = os.path.join(app.config["UPLOAD_FOLDER"], resume.stored_name)

        if os.path.exists(old_file):
            os.remove(old_file)

        resume.file_name = secure_filename(file.filename)
        resume.stored_name = stored_name
        resume.file_path = os.path.join(app.config["UPLOAD_FOLDER"], stored_name)

    else:

        resume = Resume(
            student_id=student.student_id,
            file_name=secure_filename(file.filename),
            stored_name=stored_name,
            file_path=os.path.join(app.config["UPLOAD_FOLDER"], stored_name)
        )

        db.session.add(resume)

    db.session.commit()

    return jsonify({
        "message": "Resume uploaded successfully"
    }), 201
    
from flask import send_file

@app.route("/api/student/resume/download", methods=["GET"])
@jwt_required()
def download_resume():
    
    try:

        user_id = get_jwt_identity()

        student = Student.query.filter_by(user_id=user_id).first()

        if not student:
            return jsonify({"message": "Student not found"}), 404

        resume = Resume.query.filter_by(student_id=student.student_id).first()

        if not resume:
            return jsonify({"message": "Resume not found"}), 404

        return send_file(
            resume.file_path,
            as_attachment=True,
            download_name=resume.file_name
        ) # return is not JSON it's sends the actual PDF bytes(raw binary data) becaouse PDF is not JSON
    except Exception as e:
        app.logger.exception("Error in /api/student/resume/download")
        return jsonify({"error": str(e)}), 400
    
#---------------------------------------------Notification-----------------------------------------------------


@app.route("/api/student/notifications", methods=["GET"])
@jwt_required()
def get_notifications():

    user_id = get_jwt_identity()

    notifications = Notification.query.filter_by(user_id=user_id).order_by(Notification.created_at.desc()).all()

    return jsonify([
        {
            "id":notification.id,
            "message":notification.message,
            "read_status":notification.read_status,
            "created_at":notification.created_at.strftime("%d-%m-%Y %I:%M %p")
        }
        for notification in notifications
    ]),200
    
@app.route("/api/student/notifications/<int:id>", methods=["PUT"])
@jwt_required()
def mark_as_read(id):

    notification = Notification.query.get_or_404(id)

    notification.read_status = True

    db.session.commit()

    return jsonify({
        "message":"Notification marked as read."
    }),200
    
@app.route("/api/student/notifications/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_notification(id):

    notification = Notification.query.get_or_404(id)

    db.session.delete(notification)

    db.session.commit()

    return jsonify({
        "message":"Notification deleted."
    }),200

@app.route("/api/student/notifications/read-all",methods=["PUT"])
@jwt_required()
def mark_all_notifications():

    user_id=get_jwt_identity()

    notifications=Notification.query.filter_by(
        user_id=user_id,
        read_status=False
    ).all()

    for notification in notifications:
        notification.read_status=True

    db.session.commit()

    return jsonify({
        "message":"All notifications marked as read."
    }),200

#-------------------------------------------------------------------------------------Generate Placement Report(Celery and Redis)-------------------------------------------------------------

@app.route("/api/company/report", methods=["POST"])
@jwt_required()
def generate_report():

    from tasks import Placementreport  # Import the Celery task
    user_id = int(get_jwt_identity())

    company = Company.query.filter_by(
        user_id=user_id
    ).first()

    if not company:
        return jsonify({
            "message": "Company not found"
        }), 404

    task = Placementreport.delay(company.company_id)

    return jsonify({
        "message": "Report generation started",
        "task_id": task.id
    }), 202


@app.route("/api/task/<task_id>", methods=["GET"])
@jwt_required()
def task_status(task_id):
    
    #local import to reduce circular import problem
    from celery_worker import celery_app
    task = AsyncResult(
        task_id,
        app=celery_app
    )

    return {
        "task_id": task_id,
        "status": task.status
    }

@app.route("/api/company/report/download", methods=["GET"])
@jwt_required()
def download_report():

    user_id = int(get_jwt_identity())

    company = Company.query.filter_by(
        user_id=user_id
    ).first()

    if not company:
        return jsonify({
            "message": "Company not found"
        }), 404

    company_id = company.company_id

    BASE_DIR = Path(__file__).resolve().parent

    file_path = (
        BASE_DIR
        / "reports"
        / f"company_{company_id}_report.html"
    )

    if not file_path.exists():
        return jsonify({
            "message": "Report not found"
        }), 404

    return send_file(
        file_path,
        as_attachment=True,
        download_name="placement_report.html"
    )


#---------------------------------------------------------------------For Placement--------------------------------------------------------------

@app.route("/api/company/application/<int:application_id>/placement",methods=["POST"])
@jwt_required()
def create_placement(application_id):
    user_id=get_jwt_identity()
    company=Company.query.filter_by(user_id=user_id).first()
    if not company:
        return jsonify({"message":"Company not found"}),404
    application=Application.query.join(Job).filter(
        Application.id==application_id,
        Job.company_id==company.company_id
    ).first()
    if not application:
        return jsonify({"message":"Application not found"}),404
    if application.status!="Selected":
        return jsonify({"message":"Student must be selected first"}),400
    existing=Placement.query.filter_by(application_id=application.id).first()
    if existing:
        return jsonify({"message":"Placement already exists"}),400
    data=request.get_json()
    if not data:
        return jsonify({"message":"No data received"}),400
    if not data.get("package") or not data.get("joining_date"):
        return jsonify({"message":"Package and joining date are required"}),400
    try:
        package=int(data["package"])
        joining_date=datetime.strptime(data["joining_date"],"%Y-%m-%d").date()
    except ValueError:
        return jsonify({"message":"Invalid package or joining date"}),400
    placement=Placement(
        student_id=application.student_id,
        company_id=company.company_id,
        application_id=application.id,
        package=package,
        joining_date=joining_date
    )
    db.session.add(placement)
    db.session.commit()
    return jsonify({"message":"Placement confirmed successfully"}),201

#-----------------------------------------------------------------Export CSV------------------------------------------------------------



@app.route("/api/export-history", methods=["POST"])
@jwt_required()
def export_history():
    from tasks import export_history_csv
    user_id = int(get_jwt_identity())

    student = Student.query.filter_by(
        user_id=user_id
    ).first()

    company = Company.query.filter_by(
        user_id=user_id
    ).first()

    if student:
        export_type = "STUDENT_HISTORY"

    elif company:
        export_type = "COMPANY_HISTORY"

    else:
        return jsonify({
            "message": "Invalid user"
        }), 404

    export_job = ExportJob(
        user_id=user_id,
        export_type=export_type,
        status="PENDING"
    )

    db.session.add(export_job)
    db.session.commit()

    export_history_csv.delay(export_job.id)

    return jsonify({
        "message": "CSV export started",
        "export_id": export_job.id
    }), 202
    
@app.route("/api/export-history/<int:export_id>/status",methods=["GET"])
@jwt_required()
def export_status(export_id):

    user_id = int(get_jwt_identity())

    export_job = ExportJob.query.filter_by(
        id=export_id,
        user_id=user_id
    ).first()

    if not export_job:
        return jsonify({
            "message": "Export not found"
        }), 404

    return jsonify({
        "export_id": export_job.id,
        "status": export_job.status
    }), 200
    
from flask import send_from_directory


@app.route("/api/export-history/<int:export_id>/download", methods=["GET"])
@jwt_required()
def download_export(export_id):

    user_id = int(get_jwt_identity())

    export_job = ExportJob.query.filter_by(
        id=export_id,
        user_id=user_id
    ).first()

    if not export_job:
        return jsonify({
            "message": "Export not found"
        }), 404

    if export_job.status != "COMPLETED":
        return jsonify({
            "message": "Export is not ready"
        }), 400

    return send_from_directory(
        os.path.abspath("exports"),
        export_job.filename,
        as_attachment=True
    )
if __name__ == "__main__":
    app.run(debug=True)