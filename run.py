from app import app
from db import db

db.init_app(app)

@app.before_first_request # decorator allowing to run function before first use of application
def create_tables():
    db.create_all()