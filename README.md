# Quiz Application

## Features

### User
- Register and log in securely.
- Attempt quizzes and view results.
- View progress and scores on the dashboard.
- Redeem reward points for coupons in the wallet.

### Admin
- Add, edit, and delete subjects, chapters, quizzes, and questions.
- View user activity and performance.
- Search functionality for subjects and chapters.
- View summary charts for quiz scores.

---

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: Jinja2, HTML, CSS, Bootstrap
- **Database**: SQLite
- **Libraries**:
  - Flask-SQLAlchemy: Database management.
  - Flask-Login: User session management.
  - Flask-Migrate: Database migrations.
  - Matplotlib: Data visualization for quiz summaries.

---

## Database Schema Design

- **User_Info**: Stores user details, including reward points.
- **Subject**: Represents subjects with related chapters.
- **Chapter**: Represents chapters with related quizzes.
- **Quiz**: Represents quizzes with related questions and scores.
- **Question**: Stores quiz questions and options.
- **Score**: Tracks user scores for quizzes.

---

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run database migrations:
   ```bash
   flask db upgrade
   ```

5. Start the application:
   ```bash
   python app.py
   ```

---

## Key Routes

### User
- `/dashboard`: User dashboard.
- `/summary`: User quiz summary.
- `/wallet/<user_id>`: View and redeem reward points.

### Admin
- `/admin/<name>`: Admin dashboard.
- `/add_subject`, `/add_chapter`, `/add_quiz`, `/add_question`: Add entities.
- `/edit_subject`, `/edit_chapter`, `/edit_quiz`, `/edit_question`: Edit entities.
- `/admin_summary`: View quiz performance summary.

---

## Demo

- **Login/Signup**: Secure user authentication.
- **Quiz Attempt**: Answer questions and earn reward points.
- **Wallet**: Redeem points for coupons.
- **Admin Panel**: Manage subjects, chapters, quizzes, and questions.

---

## Reflection

This project provided an opportunity to learn and implement a full-stack web application. It strengthened skills in Flask, SQLAlchemy, and frontend technologies while integrating features like user authentication, data visualization, and reward systems.
