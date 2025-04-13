# 🎓 Quiz-to-Earn Web Application

---

## 📤 SUBMISSION GUIDELINES

- **Project Title**: Quiz-to-Earn: Learning Reward System  
- **Selected Domain**: EdTech + Blockchain  
- **Problem Statement / Use Case**:  
  Create a gamified online quiz platform that incentivizes learning by rewarding users with Aptos tokens for successful quiz completion. Users can redeem these tokens for gift cards, vouchers, or premium content.

![Demo Interface](image-url)

- **Abstract / Problem Description**:  
  Traditional learning platforms often lack motivational tools to keep learners engaged. Our solution introduces a blockchain-integrated quiz system that offers Aptos tokens as rewards for correct answers. These tokens can be stored in the user wallet and redeemed for gift cards and vouchers. This ensures increased user engagement, learning retention, and practical value from digital learning platforms. The application also includes an admin dashboard to manage quizzes, track performance, and control educational content efficiently.

- **Tech Stack Used**:
  - **Backend**: Flask (Python)
  - **Frontend**: HTML, CSS, Jinja2, Bootstrap
  - **Database**: SQLite
  - **Blockchain**: Aptos Network (wallet integration & reward system)
  - **Libraries**:  
    - Flask-SQLAlchemy  
    - Flask-Login  
    - Flask-Migrate  
    - Matplotlib

- **Project Explanation**: (Also detailed in the README below)
  - The app allows users to take quizzes and earn Aptos tokens based on performance.
  - A digital wallet allows users to redeem tokens for real-world rewards.
  - Admins can add/edit content and view summary charts.
  - Data visualization helps admins monitor quiz performance.
  - All features are integrated with a responsive frontend UI.


---

## 🚀 Features

### 👤 User Features
- Secure login & registration
- View available quizzes
- Attempt quizzes and view real-time results
- Earn Aptos tokens upon successful quiz attempts
- Access wallet and redeem tokens for gift cards

### 👨‍💼 Admin Features
- Add/Edit/Delete subjects, chapters, quizzes, and questions
- View user quiz activities and scores
- Access analytical charts to monitor user progress
- Search functionality for easier content management

---

## 🗃️ Database Schema

- **User_Info** – Stores user credentials, profile, and rewards.
- **Subject** – Course subjects (e.g., Java, DBMS).
- **Chapter** – Chapters under each subject.
- **Quiz** – Quizzes per chapter with meta-data.
- **Question** – Quiz questions, options, correct answers.
- **Score** – Stores quiz performance of users.

---

## ⚙️ Installation Instructions

```bash
# Clone the repo
git clone <repository-url>
cd <repository-folder>

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
flask db upgrade

# Run the app
python app.py
