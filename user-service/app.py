from app import create_app, db
from dotenv import load_dotenv
import os

load_dotenv()

app = create_app()

@app.route('/')
def index():
    return 'Welcome to the User Service API!'

@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
