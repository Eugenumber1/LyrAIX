from ai_app import db
from ai_app import app

with app.app_context():
    db.create_all()