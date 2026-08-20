from app import app
from models import db, User
from werkzeug.security import generate_password_hash

with app.app_context():

    admin = User.query.filter_by(username="admin").first()

    if admin:
        print("Admin already exists.")
    else:
        admin = User(
            username="admin",
            email="admin@example.com",
            password=generate_password_hash("adminEternity@9336"),
            role="admin"
        )

        db.session.add(admin)
        db.session.commit()

        print("Admin created successfully.")