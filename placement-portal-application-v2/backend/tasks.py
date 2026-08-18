from datetime import date, timedelta
from zoneinfo import ZoneInfo
from celery_worker import celery_app
from flask import render_template
from datetime import datetime
from pathlib import Path
import csv
import os
from models import *


@celery_app.task
def Placementreport(company_id):

    company_id = int(company_id)  # Convert company_id to an integer
    company = Company.query.get(company_id)

    if not company:
        return {
            "message": "Company not found"
        }

    jobs = Job.query.filter_by(
        company_id=company_id
    ).all()

    job_ids = [job.job_id for job in jobs]

    applications = Application.query.filter(
        Application.job_id.in_(job_ids)
    ).all() if job_ids else []

    total_jobs = len(jobs)
    total_applications = len(applications)

    selected = sum(
        1 for app in applications
        if app.status == "Selected"
    )

    rejected = sum(
        1 for app in applications
        if app.status == "Rejected"
    )

    pending = sum(
        1 for app in applications
        if app.status == "Pending"
    )

    placement_rate = (
        selected / total_applications * 100
        if total_applications > 0
        else 0
    )

    html = render_template(
        "reports/placement_report.html",
        company=company,
        report_month=datetime.now().strftime("%B %Y"),
        total_jobs=total_jobs,
        total_applications=total_applications,
        selected=selected,
        rejected=rejected,
        pending=pending,
        placement_rate=round(placement_rate, 2)
    )

    # backend folder absolute path
    BASE_DIR = Path(__file__).resolve().parent

    # if tasks.py is directly inside backend
    report_folder = BASE_DIR / "reports"

    report_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    file_name = f"company_{company_id}_report.html"

    file_path = report_folder / file_name

    print("REPORT SAVING AT:", file_path)

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(html)

    return {
        "message": "Report generated",
        "file": str(file_path)
    }



@celery_app.task
def check_interview_reminders():
    india_time = datetime.now(
        ZoneInfo("Asia/Kolkata")
    )
    today = india_time.date()
    tomorrow = today + timedelta(days=1)

    print("INDIA TIME:", india_time)
    print("TODAY:", today)
    print("TOMORROW:", tomorrow)
    interviews=Interview.query.filter_by(
        interview_date=tomorrow
    ).all()
    for interview in interviews:
        student=interview.application.student
        send_interview_email(student,interview)
    return f"{len(interviews)} interview reminders sent"



#Interview reminder by Celery Beat
import smtplib
from email.message import EmailMessage

def send_interview_email(student, interview):
    message = EmailMessage()

    #Email header
    message["Subject"] = "Interview Reminder"
    message["From"] = "campusconnect@test.com"
    message["To"] = student.user.email

    #Email body 
    message.set_content(f"""
Hello {student.full_name},

I hope you doing well. This is a reminder for your scheduled interview.

Job: {interview.application.job.title}
Interview Date: {interview.interview_date}
Interview Time: {interview.interview_time}
Interview Mode: {interview.interview_mode}
Please be prepared and join on time.

CampusConnect Team
""")

    with smtplib.SMTP("localhost", 1025) as server:
        server.send_message(message)
        


@celery_app.task
def export_history_csv(export_id):

    export_job = db.session.get(
        ExportJob,
        export_id
    )
    if not export_job:
        return
    try:
        export_job.status = "PROCESSING"
        db.session.commit()
        user_id = export_job.user_id
        os.makedirs("exports", exist_ok=True)
        filename = f"history_{user_id}_{export_id}.csv"
        filepath = os.path.join(
            "exports",
            filename
        )

        # STUDENT EXPORT
        if export_job.export_type == "STUDENT_HISTORY":
            student = Student.query.filter_by(
                user_id=user_id
            ).first()
            applications = Application.query.filter_by(
                student_id=student.student_id
            ).all()
            # Because your Placement.student_id
            # references students.user_id
            placements = Placement.query.join(
            Application,
            Placement.application_id == Application.id
                ).filter_by(
                student_id=student.student_id
            ).all()
            with open(
                filepath,
                "w",
                newline="",
                encoding="utf-8"
            ) as file:
                writer = csv.writer(file)
                writer.writerow([
                    "APPLICATION HISTORY"
                ])
                writer.writerow([
                    "Application ID",
                    "Job",
                    "Company",
                    "Status",
                    "Applied At"
                ])
                for application in applications:
                    writer.writerow([
                        application.id,
                        application.job.title,
                        application.job.company.company_name,
                        application.status,
                        application.applied_at
                    ])
                writer.writerow([])
                writer.writerow([
                    "PLACEMENT HISTORY"
                ])
                writer.writerow([
                    "Placement ID",
                    "Company",
                    "Package",
                    "Joining Date"
                ])
                for placement in placements:
                    writer.writerow([
                        placement.id,
                        placement.company.company_name,
                        placement.package,
                        placement.joining_date
                    ])
        # COMPANY EXPORT

        elif export_job.export_type == "COMPANY_HISTORY":
            company = Company.query.filter_by(
                user_id=user_id
            ).first()

            applications = (
                Application.query
                .join(Job)
                .filter(
                    Job.company_id == company.company_id
                )
                .all()
            )
            placements = Placement.query.filter_by(
                company_id=company.company_id
            ).all()

            with open(
                filepath,
                "w",
                newline="",
                encoding="utf-8"
            ) as file:
                writer = csv.writer(file)
                writer.writerow([
                    "APPLICATION HISTORY"
                ])
                writer.writerow([
                    "Application ID",
                    "Student",
                    "Branch",
                    "CGPA",
                    "Job",
                    "Status",
                    "Applied At"
                ])
                for application in applications:

                    writer.writerow([
                        application.id,
                        application.student.full_name,
                        application.student.branch,
                        application.student.cgpa,
                        application.job.title,
                        application.status,
                        application.applied_at
                    ])

                writer.writerow([])

                writer.writerow([
                    "PLACEMENT HISTORY"
                ])
                writer.writerow([
                    "Placement ID",
                    "Student",
                    "Package",
                    "Joining Date"
                ])
                for placement in placements:

                    writer.writerow([
                        placement.id,
                        placement.student.full_name,
                        placement.package,
                        placement.joining_date
                    ])
        export_job.status = "COMPLETED"
        export_job.filename = filename
        export_job.completed_at = datetime.utcnow()

        notification = Notification(
            user_id=user_id,
            message="Your CSV export is ready to download."
        )
        db.session.add(notification)
        db.session.commit()
        return {
            "export_id": export_id,
            "status": "COMPLETED"
        }
    except Exception as error:
        db.session.rollback()
        print("CSV EXPORT ERROR:", error)
        export_job = db.session.get(  #Finds the export request using its primary key.
            ExportJob,
            export_id
        )
        if export_job:
            export_job.status = "FAILED"
            notification = Notification(
                user_id=export_job.user_id,
                message="CSV export failed."
            )
            db.session.add(notification)
            db.session.commit()
        raise error