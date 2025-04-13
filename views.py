from flask import flash, redirect, url_for, render_template, request
from backend.models import Quiz, db, Subject

def get_user_points():
    # Replace with actual logic to fetch user points
    return 50  # Example: Returning a default value for demonstration

@app.route('/redeem', methods=['POST'])
def redeem():
    user_points = get_user_points()  # Replace with actual logic to fetch user points
    required_points = 100  # Example: Points required for redemption

    if user_points < required_points:
        flash("You don't have enough points to redeem.")  # Set error message
        return redirect(url_for('redemption'))  # Redirect to redemption page

    # Redemption logic if points are sufficient
    flash("Successfully redeemed!")  # Set success message
    return redirect(url_for('redemption'))

@app.route('/dashboard', methods=['GET', 'POST'])
def user_dashboard():
    search_text = request.form.get('search') if request.method == 'POST' else None
    subjects = []
    quizzes = []

    if search_text:
        # Query the database for subjects matching the search term
        subjects = Subject.query.filter(Subject.name.ilike(f"%{search_text}%")).all()
        quizzes = Quiz.query.filter(Quiz.name.ilike(f"%{search_text}%")).all()

    return render_template('user_dashboard.html', search_text=search_text, subjects=subjects, quizzes=quizzes)
