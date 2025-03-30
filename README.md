### User
- Register and log in with secure credentials.
- View progress and scores on the dashboard.

### Admin
- Manage users, decks, and cards.
- View user activity and performance.
- Perform administrative tasks like resetting user progress or deleting inactive accounts.

---

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: Jinja2, HTML, CSS, Bootstrap
- **Database**: SQLite
- **Libraries**:
  - Flask-SQLAlchemy: Database management.
  - Flask-RESTful: API handling.
  - Flask-Login: User session management.
  - Datetime: Timestamping operations.
  - Requests: Handling HTTP requests and responses.

---

## Database Schema Design

- **User**: One user can have many decks (many-to-many relationship).
- **Deck**: One deck can have many cards (one-to-many relationship).
- **Card**: Each card belongs to one deck.

### Attributes:
- **User**: `id` (Primary Key), `username`, `password`, etc.
- **Deck**: `id` (Primary Key), `name`, `score`, `last_reviewed`, `user_id` (Foreign Key).
- **Card**: `card_id` (Primary Key), `deck_id` (Foreign Key), `front`, `back`, etc.

---

## API Design

- **User API**:
  - `GET`: Fetch user details, related decks, and scores.
  - `POST`: Add new users to the database.
- **Deck API**:
  - `GET`: Retrieve decks for a user, including deck name, score, and last reviewed card.
  - `POST`: Add new decks.
- **Card API**:
  - `GET`: Fetch cards for a specific deck, including `card_id`, `front`, and `back`.
  - `POST`: Add new cards.
  - `PUT`: Update existing cards.

---

## Architecture and Features

The project is organized into the following structure:
- **Backend**:
  - `__init__.py`, `api.py`, `models.py`, `views.py`: Core Python files for app functionality.
  - SQLite database for persistent storage.
- **Frontend**:
  - Static folder: Contains images and CSS files.
  - Templates folder: Includes HTML files for the landing page, signup, login, dashboard, and review page.
- **App**:
  - `app.py`: Main application file.

### Key Routes:
- `/dashboard`: User dashboard.
- `/`: Landing page.
- `/review/<deck>`: Review cards in a deck.
- `/review/<deck>/<card_id>`: Review a specific card.
- `/login`: User login.
- `/register`: User registration.
- `/logout`: User logout.

---

## Installation

1. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Creating a VENV:
   ```bash
   python -m venv venv
   venv\scripts\activate
   ```
4. Run the application:
   ```bash
   python app.py
   ```

---

## Demo

- **Login/Signup**: Secure user authentication.
- **CRUD Operations**: Create, update, and delete decks and cards.
- **Dashboard**: View progress and scores.
- **Flashcard Review**: Hover over cards to see the back side.

---

## Author

**Student Name**: Karthik Kalleti  
**Roll Num**: 23f2001791  
**Email**: 23f2001791@ds.study.iitm.ac.in  

---

## Reflection

This project was an enjoyable learning experience. Overcoming challenges during development brought immense satisfaction. It helped me strengthen my skills in Flask, RESTful APIs, SQLAlchemy, and frontend technologies.
