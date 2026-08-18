
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

#------------------ USER ------------------
class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # 'admin', 'company', or 'student'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    is_active = db.Column(db.String(20), default="Active")  # New field to indicate if the user is active
    
    company_profile = db.relationship("Company", backref="user", uselist=False) 
    student_profile = db.relationship("Student", backref="user", uselist=False)

class Student(db.Model):
    __tablename__ = 'students'

    student_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), unique=True, nullable=False)  # Link to User table
    
    full_name = db.Column(db.String(100))
    branch = db.Column(db.String(50))
    year = db.Column(db.Integer)
    cgpa = db.Column(db.Float)
    phone = db.Column(db.String(20))
    college=db.Column(db.String(50))
    status=db.Column(db.String(20), default="Active")
    
    resume=db.relationship("Resume", backref="student", uselist=False)
    skills=db.relationship("Skill", backref="student", uselist=False)
    
class Interview(db.Model):
    __tablename__ = "interviews"

    interview_id=db.Column(db.Integer,primary_key=True)
    application_id=db.Column(db.Integer,db.ForeignKey("applications.id"),unique=True,nullable=False)
    interview_date=db.Column(db.Date,nullable=False)
    interview_time=db.Column(db.Time,nullable=False)
    interview_mode=db.Column(db.String(30),nullable=False)
    meeting_link=db.Column(db.String(500))
    location=db.Column(db.String(255))
    created_at=db.Column(db.DateTime,default=datetime.utcnow)
    
    application=db.relationship("Application",backref=db.backref("interview",uselist=False))
    
    status = db.Column(db.String(20), default="Scheduled")
    
class Skill(db.Model):
    __tablename__ = "sKills"
    skill_id = db.Column(db.Integer, primary_key=True)
    student_id=db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)
    skill=db.Column(db.String(200))

class Resume(db.Model):
    __tablename__ = "resume"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.student_id"),
        nullable=False
    )

    file_name = db.Column(db.String(255))
    stored_name = db.Column(db.String(255))
    file_path = db.Column(db.String(500))
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

class Company(db.Model):
    __tablename__ = 'companies'

    company_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False, unique=True)  # Link to User table
    company_name = db.Column(db.String(150), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    about_company = db.Column(db.Text, nullable=True)
    industry = db.Column(db.String(100), nullable=True)
    approval_status = db.Column(db.String(50), default="Pending")  # PENDING, APPROVED, REJECTED
    is_blocklisted = db.Column(db.Boolean, default=False)  # New field to indicate if the company is blocklisted
    
    job=db.relationship("Job", backref="company", lazy="select")

    
class Job(db.Model):
    __tablename__ = "jobs"

    job_id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(
        db.Integer,
        db.ForeignKey("companies.company_id"),
        nullable=False
    )

    title = db.Column(db.String(100), nullable=False)
    job_type = db.Column(db.String(50))
    location = db.Column(db.String(100))
    salary = db.Column(db.String(100))
    experience = db.Column(db.String(100))
    deadline = db.Column(db.Date)
    cgpa = db.Column(db.Float)
    vacancies = db.Column(db.Integer)
    skills = db.Column(db.Text)
    description = db.Column(db.Text)
    status=db.Column(db.String(20), default="Open")
    approve_status = db.Column(db.String(20), default="Pending")  # rejected, approved or pending by admin

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    
class Application(db.Model):
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(db.Integer, db.ForeignKey("students.student_id"), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.job_id"),nullable=False)
    status = db.Column(db.String(30), default="Applied")
    
    applied_at = db.Column(db.DateTime, server_default=db.func.now())

    student = db.relationship("Student", backref="applications")
    job = db.relationship("Job", backref="applications")
    
class Placement(db.Model):
    __tablename__="placements"
    id=db.Column(db.Integer,primary_key=True)
    student_id=db.Column(db.Integer,db.ForeignKey("students.student_id"),nullable=False)
    company_id=db.Column(db.Integer,db.ForeignKey("companies.company_id"),nullable=False)
    application_id=db.Column(db.Integer,db.ForeignKey("applications.id"),unique=True,nullable=False)
    package=db.Column(db.Integer,nullable=False)
    joining_date=db.Column(db.Date,nullable=False)
    student=db.relationship("Student",backref="placements")
    company=db.relationship("Company",backref="placements")
    application=db.relationship("Application",backref=db.backref("placement",uselist=False))
    
    
class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    message = db.Column(db.Text)
    read_status = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship("User", backref="notifications")

class ExportJob(db.Model):
    __tablename__ = "export_jobs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    export_type = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default="PENDING")
    filename = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
# #--------------------Audit Log(track every admin action)------------------
# class AuditLog(db.Model):
#     __tablename__ = "audit_logs"

#     log_id = db.Column(db.Integer, primary_key=True)

#     admin_id = db.Column(
#         db.Integer,
#         db.ForeignKey("admins.admin_id")
#     )

#     action = db.Column(db.Text)

#     created_at = db.Column(db.DateTime)

