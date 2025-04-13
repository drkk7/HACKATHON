# App routes
from flask import Flask, render_template, request, url_for, redirect
from .models import *
from flask import current_app as app
from datetime import datetime
from sqlalchemy import func
from werkzeug.utils import secure_filename
import matplotlib.pyplot as plt
import io
import base64
from flask_login import login_user, logout_user, login_required
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend for Matplotlib

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        uname = request.form.get("user_name")
        pwd = request.form.get("password")
        usr = User_Info.query.filter_by(email=uname, password=pwd).first()
        if usr:
            login_user(usr)
            if usr.role == 0:  # Admin
                return redirect(url_for("admin_dashboard", name=uname))
            else:  # Normal user
                return redirect(url_for("user_dashboard", name=usr.full_name, id=usr.id))
        else:
            return render_template("login.html", msg="Invalid user credentials...")

    return render_template("login.html", msg="")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("signin"))


@app.route("/register", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        uname = request.form.get("user_name")
        pwd = request.form.get("password")
        full_name = request.form.get("full_name")
        address = request.form.get("location")
        pin_code = request.form.get("pin_code")
        usr = User_Info.query.filter_by(email=uname).first()
        if usr:
            return render_template("signup.html", msg="Sorry, this mail already registered!!!")
        new_usr = User_Info(email=uname, password=pwd, full_name=full_name, address=address, pin_code=pin_code)
        db.session.add(new_usr)
        db.session.commit()
        return render_template("login.html", msg="Registration successful, try login now")

    return render_template("signup.html", msg="")


# Admin dashboard
@app.route("/admin/<name>")
def admin_dashboard(name):
    subjects = Subject.query.all()
    user = User_Info.query.filter_by(email=name).first()  # Fetch the user object
    return render_template("admin_dashboard.html", name=name, subjects=subjects, user=user)


# User dashboard
@app.route("/user/<id>/<name>")
def user_dashboard(id, name):
    # Fetch all subjects from the database
    subjects = Subject.query.all()
    user = User_Info.query.get(id)  # Fetch the user object
    return render_template("user_dashboard.html", id=id, name=name, subjects=subjects, user=user)


# Add subject (admin only)
@app.route("/add_subject/<name>", methods=["GET", "POST"])
def add_subject(name):
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        subject = Subject(name=name, description=description)
        db.session.add(subject)
        db.session.commit()
        return redirect(url_for("admin_dashboard", name=name))
    return render_template("add_subject.html", name=name)


# Add chapter (admin only)
@app.route("/add_chapter/<subject_id>/<name>", methods=["GET", "POST"])
def add_chapter(subject_id, name):
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        chapter = Chapter(name=name, description=description, subject_id=subject_id)
        db.session.add(chapter)
        db.session.commit()
        return redirect(url_for("admin_dashboard", name=name))
    return render_template("add_chapter.html", subject_id=subject_id, name=name)


# Add quiz (admin only)
@app.route("/add_quiz/<chapter_id>/<name>", methods=["GET", "POST"])
def add_quiz(chapter_id, name):
    if request.method == "POST":
        name = request.form.get("name")
        date_of_quiz = request.form.get("date_of_quiz")
        time_duration = request.form.get("time_duration")
        quiz = Quiz(name=name, date_of_quiz=date_of_quiz, time_duration=time_duration, chapter_id=chapter_id)
        db.session.add(quiz)
        db.session.commit()
        return redirect(url_for("admin_dashboard", name=name))
    return render_template("add_quiz.html", chapter_id=chapter_id, name=name)


# Add question (admin only)
@app.route("/add_question/<quiz_id>/<name>", methods=["GET", "POST"])
def add_question(quiz_id, name):
    if request.method == "POST":
        question_statement = request.form.get("question_statement")
        option1 = request.form.get("option1")
        option2 = request.form.get("option2")
        option3 = request.form.get("option3")
        option4 = request.form.get("option4")
        correct_option = request.form.get("correct_option")
        question = Question(question_statement=question_statement, option1=option1, option2=option2, option3=option3, option4=option4, correct_option=correct_option, quiz_id=quiz_id)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for("admin_dashboard", name=name))
    return render_template("add_question.html", quiz_id=quiz_id, name=name)


# Attempt quiz (user only)
@app.route("/quiz/<quiz_id>/<user_id>", methods=["GET", "POST"])
def attempt_quiz(quiz_id, user_id):
    quiz = Quiz.query.get(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    user = User_Info.query.get(user_id)  # Fetch the user object

    if request.method == "POST":
        total_score = 0
        reward_points = 0  # Initialize reward points
        for question in questions:
            selected_option = request.form.get(f"question_{question.id}")
            if selected_option == question.correct_option:
                total_score += 1
                reward_points += 100  # Each correct answer gives 10 reward points

        # Ensure reward_points is not None
        if user.reward_points is None:
            user.reward_points = 0

        user.reward_points += reward_points  # Add reward points to the user's wallet
        score = Score(user_id=user_id, quiz_id=quiz_id, total_scored=total_score, time_stamp_of_attempt=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        db.session.add(score)
        db.session.commit()
        return redirect(url_for("quiz_results", quiz_id=quiz_id, user_id=user_id, score=total_score, total=len(questions)))

    return render_template("quiz.html", quiz=quiz, questions=questions, user_id=user_id, user=user)


# Quiz results page
@app.route("/quiz_results/<quiz_id>/<user_id>/<score>/<total>")
def quiz_results(quiz_id, user_id, score, total):
    user = User_Info.query.get(user_id)  # Fetch the user object
    return render_template("quiz_results.html", quiz_id=quiz_id, user_id=user_id, score=score, total=total, user=user)


# Edit subject (admin only)
@app.route("/edit_subject/<subject_id>/<name>", methods=["GET", "POST"])
def edit_subject(subject_id, name):
    subject = Subject.query.get(subject_id)
    if request.method == "POST":
        subject.name = request.form.get("name")
        subject.description = request.form.get("description")
        db.session.commit()
        return redirect(url_for("admin_dashboard", name=name))
    return render_template("edit_subject.html", subject=subject, name=name)


# Edit chapter (admin only)
@app.route("/edit_chapter/<chapter_id>/<name>", methods=["GET", "POST"])
def edit_chapter(chapter_id, name):
    chapter = Chapter.query.get(chapter_id)
    if request.method == "POST":
        chapter.name = request.form.get("name")
        chapter.description = request.form.get("description")
        db.session.commit()
        return redirect(url_for("admin_dashboard", name=name))
    return render_template("edit_chapter.html", chapter=chapter, name=name)


# Edit quiz (admin only)
@app.route("/edit_quiz/<quiz_id>/<name>", methods=["GET", "POST"])
def edit_quiz(quiz_id, name):
    quiz = Quiz.query.get(quiz_id)
    if request.method == "POST":
        quiz.name = request.form.get("name")
        quiz.date_of_quiz = request.form.get("date_of_quiz")
        quiz.time_duration = request.form.get("time_duration")
        db.session.commit()
        return redirect(url_for("admin_dashboard", name=name))
    return render_template("edit_quiz.html", quiz=quiz, name=name)


# Edit question (admin only)
@app.route("/edit_question/<question_id>/<name>", methods=["GET", "POST"])
def edit_question(question_id, name):
    question = Question.query.get(question_id)
    if request.method == "POST":
        question.question_statement = request.form.get("question_statement")
        question.option1 = request.form.get("option1")
        question.option2 = request.form.get("option2")
        question.option3 = request.form.get("option3")
        question.option4 = request.form.get("option4")
        question.correct_option = request.form.get("correct_option")
        db.session.commit()
        return redirect(url_for("admin_dashboard", name=name))
    return render_template("edit_question.html", question=question, name=name)


# Delete subject (admin only)
@app.route("/delete_subject/<subject_id>/<name>", methods=["GET"])
def delete_subject(subject_id, name):
    subject = Subject.query.get(subject_id)
    db.session.delete(subject)
    db.session.commit()
    return redirect(url_for("admin_dashboard", name=name))


# Delete chapter (admin only)
@app.route("/delete_chapter/<chapter_id>/<name>", methods=["GET"])
def delete_chapter(chapter_id, name):
    chapter = Chapter.query.get(chapter_id)
    db.session.delete(chapter)
    db.session.commit()
    return redirect(url_for("admin_dashboard", name=name))


# Delete quiz (admin only)
@app.route("/delete_quiz/<quiz_id>/<name>", methods=["GET"])
def delete_quiz(quiz_id, name):
    quiz = Quiz.query.get(quiz_id)
    db.session.delete(quiz)
    db.session.commit()
    return redirect(url_for("admin_dashboard", name=name))


# Delete question (admin only)
@app.route("/delete_question/<question_id>/<name>", methods=["GET"])
def delete_question(question_id, name):
    question = Question.query.get(question_id)
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for("admin_dashboard", name=name))


# Search functionality (admin only)
@app.route("/search/<name>", methods=["GET", "POST"])
def search(name):
    if request.method == "POST":
        search_text = request.form.get("search_text")
        # Search for subjects
        subjects = Subject.query.filter(Subject.name.ilike(f"%{search_text}%")).all()
        # Search for chapters
        chapters = Chapter.query.filter(Chapter.name.ilike(f"%{search_text}%")).all()
        return render_template("admin_dashboard.html", name=name, subjects=subjects, chapters=chapters, search_text=search_text)
    return redirect(url_for("admin_dashboard", name=name))


# Search functionality (user only)
@app.route("/user_search/<id>/<name>", methods=["GET", "POST"])
def user_search(id, name):
    if request.method == "POST":
        search_text = request.form.get("search_text")
        # Search for quizzes and chapters
        chapters = Chapter.query.filter(Chapter.name.ilike(f"%{search_text}%")).all()
        quizzes = Quiz.query.filter(Quiz.name.ilike(f"%{search_text}%")).all()
        user = User_Info.query.get(id)  # Fetch the user object
        return render_template("user_dashboard.html", id=id, name=name, chapters=chapters, quizzes=quizzes, search_text=search_text, user=user)
    return redirect(url_for("user_dashboard", id=id, name=name))


# Summary page (admin only)
@app.route("/admin_summary")
def admin_summary():
    # Fetch all scores from the database
    scores = Score.query.all()

    if not scores:
        return render_template("admin_summary.html", plot_url=None)

    # Prepare data for the bar graph
    quiz_ids = [score.quiz_id for score in scores]
    total_scores = [score.total_scored for score in scores]

    # Create a bar graph
    plt.figure(figsize=(10, 6))
    plt.bar(quiz_ids, total_scores, color='blue')
    plt.xlabel("Quiz ID")
    plt.ylabel("Total Score")
    plt.title("Quiz ID vs Total Score")
    plt.xticks(quiz_ids)

    # Save the plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    plt.close()

    # Render the summary page with the graph
    return render_template("admin_summary.html", plot_url=plot_url)


# User summary page
@app.route("/user_summary/<user_id>")
def user_summary(user_id):
    # Fetch scores for the specific user
    scores = Score.query.filter_by(user_id=user_id).all()
    user = User_Info.query.get(user_id)  # Fetch the user object

    if not scores:
        # Generate a placeholder graph if no data is available
        plt.figure(figsize=(10, 6))
        plt.text(0.5, 0.5, "No performance data available", fontsize=18, ha='center', va='center')
        plt.axis('off')

        # Save the placeholder graph to a BytesIO object
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode('utf8')
        plt.close()

        print("DEBUG: No scores available. Placeholder graph generated.")
        return render_template("user_summary.html", plot_url=plot_url, user=user)

    # Prepare data for the bar graph
    quiz_ids = [score.quiz_id for score in scores]
    user_scores = [score.total_scored for score in scores]

    print(f"DEBUG: Quiz IDs: {quiz_ids}")
    print(f"DEBUG: User Scores: {user_scores}")

    # Create a bar graph
    plt.figure(figsize=(10, 6))
    plt.bar(quiz_ids, user_scores, color='green')
    plt.xlabel("Quiz ID")
    plt.ylabel("Your Score")
    plt.title("Quiz ID vs Your Score")
    plt.xticks(quiz_ids)

    # Save the plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    plt.close()

    print("DEBUG: Graph generated successfully.")
    return render_template("user_summary.html", plot_url=plot_url, user=user)

@app.route("/wallet/<user_id>")
@login_required
def wallet(user_id):
    user = User_Info.query.get(user_id)
    return render_template("wallet.html", reward_points=user.reward_points)

@app.route("/redeem_points/<user_id>", methods=["POST"])
@login_required
def redeem_points(user_id):
    user = User_Info.query.get(user_id)
    if user.reward_points is None:
        user.reward_points = 0

    coupons = []  # Initialize an empty list for coupons

    if user.reward_points >= 100:  # Set a minimum threshold for redemption
        user.reward_points -= 100  # Deduct 100 points for redemption
        db.session.commit()
        message = "Successfully redeemed 100 points!"

        # Fetch available coupons based on remaining points
        if user.reward_points >= 200:
            coupons.append("10% off on Amazon purchases")
        if user.reward_points >= 500:
            coupons.append("₹100 Flipkart voucher")
        if user.reward_points >= 1000:
            coupons.append("₹50 mobile recharge coupon")
    else:
        message = "Not enough points to redeem. You need at least 100 points."

    return render_template("wallet.html", reward_points=user.reward_points, message=message, coupons=coupons)

@app.route("/redeem_coupon/<user_id>/<coupon>", methods=["POST"])
@login_required
def redeem_coupon(user_id, coupon):
    user = User_Info.query.get(user_id)
    if user.reward_points is None:
        user.reward_points = 0

    # Define the points required for each coupon
    coupon_points = {
        "amazon": 1000,
        "flipkart": 500,
        "recharge": 750,
        "shopping": 3000
    }

    if coupon in coupon_points:
        required_points = coupon_points[coupon]
        if user.reward_points >= required_points:
            user.reward_points -= required_points
            db.session.commit()
            message = f"Successfully redeemed {coupon.capitalize()} coupon!"
        else:
            message = f"Not enough points to redeem {coupon.capitalize()} coupon. You need {required_points} points."
    else:
        message = "Invalid coupon selected."

    return redirect(url_for("wallet", user_id=user_id, message=message))