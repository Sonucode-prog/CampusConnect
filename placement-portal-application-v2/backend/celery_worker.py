from celery import Celery, Task
from app import app
from celery.schedules import crontab
import os

# Create Celery app
# broker = where tasks are queued (Redis DB 1)
# backend = where results are stored (Redis DB 2)

redis_url = os.getenv(
    "REDIS_URL",
    "redis://localhost:6379/0"
)

celery_app = Celery(
    "tasks",
    broker=redis_url,
    backend=redis_url
)

# celery_app = Celery(
#     'tasks',
#     broker='redis://localhost:6379/1',
#     backend='redis://localhost:6379/2',
#     include=['tasks']  # tells Celery where to find task functions
# )

# This class ensures every task runs inside Flask's app context
# Without this, tasks can't use db.session, render_template, etc.
class FlaskTask(Task):  #The FlaskTask class wraps every task execution inside with app.app_context(), giving tasks access to Flask features.
                        #because Celery workers run in a separate process from Flask. They don't have Flask's application context by default.
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)
                        
celery_app.Task = FlaskTask

# Set timezone (important for scheduled tasks)
celery_app.conf.timezone = 'Asia/Kolkata'


# ---------- Beat Schedule (Periodic Tasks) ----------
celery_app.conf.beat_schedule = {
    'interview-reminder': {
        'task': 'tasks.check_interview_reminders',
        # 'schedule': 60,
        'schedule': crontab(hour=3, minute=30),
    },
    
}
print("CELERY TIMEZONE:", celery_app.conf.timezone)
print("CELERY NOW:", celery_app.now())