import os
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from backend.models import db, User_Info, Subject
from flask_migrate import Migrate

# Initialize the Flask app
app = Flask(__name__)

# Configure the app
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'quiz_show.sqlite3')}"  # Absolute path to the database file
app.config["SECRET_KEY"] = "your_secret_key"  # Required for Flask-Login
app.secret_key = 'your_secret_key'  # Replace with a secure key
app.debug = True  # Enable debug mode

# Initialize the database
db.init_app(app)
app.app_context().push()  # Push the app context for database access

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # Redirect to login page if not authenticated

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Make `user` globally available in templates
app.jinja_env.globals['user'] = current_user

# User loader callback for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User_Info, int(user_id))  # Fetch user from the database using the new API

print("quiz_master_application is started...")

# Import controllers (ensure this module exists and is correctly implemented)
from backend.controllers import *

# Add a route for the dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    # Fetch all subjects dynamically from the database
    subjects = Subject.query.all()
    return render_template('user_dashboard.html', subjects=subjects)

# Add a route for the summary page
@app.route('/summary')
@login_required
def summary():
    # Redirect to the user summary page with the current user's ID
    return redirect(url_for('user_summary', user_id=current_user.id))

# Add a route for login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Replace this with your actual authentication logic
        username = request.form.get('username')
        password = request.form.get('password')

        # Mock authentication (replace with database lookup)
        if username == "test" and password == "password":
            user = User_Info.query.filter_by(username=username).first()
            if user and user.check_password(password):
                login_user(user)
                flash("Logged in successfully!", "success")
                return redirect(url_for('dashboard'))
            else:
                flash("Invalid username or password", "danger")
    return render_template('login.html')

# Main entry point
if __name__ == "__main__":
    app.run()