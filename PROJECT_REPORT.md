# Library Management System Project Report

## Index

1. Introduction
2. Objectives
3. Problem Statement
4. System Requirements
5. System Design
6. Modules Description
7. Algorithm
8. Database Design
9. Project Explanation
10. How the Project Works
11. Python Concepts and OOP Topics Used
12. Advantages and Limitations
13. Conclusion
14. References

---

## 1. Introduction

This project is a Flask-based Library Management System designed to manage books, users, book issuance, and returns. It includes role-based access for Admin and Student users, input validation, secure session handling, and audit logging.

The system is implemented as a web application using Python, Flask, SQLite, Flask-Session, Flask-WTF, and environment variable management via `python-dotenv`.

## 2. Objectives

- Build a secure and functional library management web application.
- Allow Admin users to manage books, users, and audit trails.
- Allow Student users to browse, issue, and return books.
- Use SQLite for persistent storage.
- Implement security features including input validation, CSRF protection, session security, and parameterized SQL queries.
- Provide clear documentation and quick start scripts.

## 3. Problem Statement

Many small libraries and educational institutions rely on manual tracking of books and user transactions. This increases the risk of lost records, incorrect issue/return status, and poor oversight of usage.

The project solves this by offering an online system to store book records, user information, issue history, and audit logs in a centralized database.

## 4. System Requirements

### Software Requirements

- Python 3.x
- Flask
- Flask-Session
- Flask-WTF
- python-dotenv
- SQLite

### Functional Requirements

- Register and authenticate users.
- Support Admin and Student roles.
- Add, delete, issue, and return books.
- Enforce rate limiting on concurrent logins.
- Record audit logs for important actions.
- Protect forms with CSRF.

### Non-functional Requirements

- Secure session cookies.
- Input validation for usernames, emails, passwords, and book details.
- Prevent SQL injection through parameterized queries.
- Maintain a responsive web UI with templates.
- Separate configuration secrets from application code.

## 5. System Design

The application follows a simple MVC-style structure:

- `app.py` contains the Flask application, routes, security, and database logic.
- `templates/` contains HTML templates for Admin and Student interfaces.
- `static/` contains CSS and upload directories.
- `library.db` is the SQLite database file.
- `.env` stores secret keys and runtime configuration.

The system uses controllers in `app.py` to handle requests, database functions for persistence, and templates to render views.

## 6. Modules Description

### Core Application

- `app.py`
  - Main Flask application file.
  - Loads environment variables and configures sessions.
  - Defines route handlers and helper functions.

### Setup & Documentation

- `requirements.txt` — Python dependencies.
- `run.bat` / `run.sh` — Quick start scripts.
- `setup.bat` — Setup script for Windows.
- `README.md`, `QUICKSTART.md`, `SECURITY.md`, `IMPLEMENTATION_SUMMARY.md` — project documentation.

### Templates

- `templates/base.html` — Base layout used by all pages.
- `templates/login.html` / `register.html` — Authentication pages.
- `templates/admin_*` — Admin dashboard, user and book management, logs.
- `templates/student_*` — Student dashboard, book browse, issue and return pages.

### Utility and Security

- `.env` — Secret configuration.
- `verify_security.py` — Security verification helper.
- `copy_files.py`, `setup_files.py` — utility scripts for file operations.

## 7. Algorithm

### User Authentication Flow

1. User submits login form.
2. Server validates credentials.
3. If valid, login is recorded in `active_sessions`.
4. Rate limiting is enforced by checking active session counts.
5. User is redirected to Admin or Student dashboard.

### Book Issue Flow

1. Student or Admin selects a book to issue.
2. Server checks that the book is available.
3. If valid, the book record is updated with issue details.
4. A record is saved in `issue_history`.
5. Book status changes to `Issued`.

### Book Return Flow

1. User selects an issued book to return.
2. Server validates return request.
3. Book status is updated to `Available`.
4. `issued_to`, `issue_date`, and `return_date` fields are cleared or updated.
5. The issue history record is updated to `Returned`.

### Rate Limiting Logic

- Count active sessions in `active_sessions` by role.
- Reject login when:
  - Admin count >= 2 and role is Admin.
  - Student count >= 3 and role is Student.
  - Total active sessions >= 5.

### Input Validation

- Username: 3-20 chars, alphanumeric or underscore.
- Email: RFC-style format.
- Password: 6-128 characters.
- Book title and author: non-empty text.
- File uploads: validated by extension and filename.

## 8. Database Design

The project uses SQLite with the following main tables:

### `users`
- `id` INTEGER PRIMARY KEY
- `username` TEXT UNIQUE
- `email` TEXT UNIQUE
- `password_hash` TEXT
- `role` TEXT (`Admin` or `Student`)
- `full_name`, `department`, `programme`, `semester`, `academic_year`
- `contact_number`, `gender`, `caste`
- `profile_completed`, `profile_edit_allowed`, `is_restricted`
- `restriction_reason`, `restricted_at`, `created_at`

### `books`
- `id` INTEGER PRIMARY KEY
- `title` TEXT
- `author` TEXT
- `status` TEXT (`Available` or `Issued`)
- `issued_to` TEXT
- `issue_date` TEXT
- `return_date` TEXT

### `issue_history`
- `id` INTEGER PRIMARY KEY
- `book_id` INTEGER
- `book_title` TEXT
- `issued_to` TEXT
- `issue_date` TEXT
- `expected_return_date` TEXT
- `returned_by` TEXT
- `actual_return_date` TEXT
- `status` TEXT (`Active`, `Returned`)
- `created_at` TEXT

### `active_sessions`
- `id` INTEGER PRIMARY KEY
- `user_id` INTEGER
- `username` TEXT
- `role` TEXT
- `login_time` TEXT
- `last_activity` TEXT

### `audit_log`
- `id` INTEGER PRIMARY KEY
- `user_id` INTEGER
- `action` TEXT
- `details` TEXT
- `timestamp` TEXT

### `book_requests` (optional workflow)
- `id` INTEGER PRIMARY KEY
- `book_id`, `student_id`
- `student_username` TEXT
- `request_date`, `expected_return_date` TEXT
- `status` TEXT
- `admin_id` INTEGER
- `admin_action_at`, `created_at` TEXT

## 9. Project Explanation

The Library Management System provides a web interface for managing book inventory and student book loans. It supports two kinds of users: Admins and Students.

Admins can:
- Add and delete books.
- Manage users.
- View audit logs.
- Monitor rate-limited sessions.

Students can:
- Browse available books.
- Issue books.
- Return books.
- View their personal issue history.

All user actions are validated and recorded to preserve security and accountability.

## 10. How the Project Works

1. Start the application with `python app.py` or by running `run.bat` / `run.sh`.
2. Open the browser at `http://localhost:5000`.
3. Register a new user or log in with an existing account.
4. Depending on role, access either the Admin dashboard or Student dashboard.
5. For Admin:
   - Add books via the admin interface.
   - Manage users and review logs.
6. For Student:
   - Browse books and request issue/return.
7. The server stores updates in `library.db` and enforces session limits.

## 11. Python Concepts and OOP Topics Used

### Python Concepts
- Flask web framework for routing and templating.
- SQLite database access using `sqlite3`.
- Environment variable loading with `python-dotenv`.
- Session management with `flask_session`.
- CSRF protection using `Flask-WTF`.
- Password hashing with `werkzeug.security`.
- File upload validation using `werkzeug.utils.secure_filename`.
- Regular expressions for input validation.
- Date and time handling with `datetime`.
- Modular helper functions for database and file handling.

### OOP Topics
- The current implementation uses a **functional style** within `app.py`.
- Flask and Werkzeug provide object-based APIs (`Flask`, `Session`, `EmailMessage`, `Request`), but the project does not define custom classes.
- The system relies on library-provided classes rather than custom class-based models.

## 12. Advantages and Limitations

### Advantages
- Easy deployment with `run.bat` / `run.sh`.
- Secure user authentication and role-based access.
- Rate limiting prevents too many concurrent logins.
- Audit logging captures user actions.
- Environment variables keep secrets out of code.
- SQLite makes deployment simple with no external database server.
- Clear documentation is available in `README.md`, `QUICKSTART.md`, and `SECURITY.md`.

### Limitations
- The app is designed for small-scale use with SQLite.
- No custom class-based models or ORM are used.
- Scalability is limited by single-process Flask and SQLite concurrency.
- The UI is based on templates without an SPA frontend.
- Admin/Student roles are not extensible beyond the two built-in roles.
- Some features, such as book requests and notifications, may require further refinement.

## 13. Conclusion

This Library Management System provides a complete web-based solution for tracking books, users, and issuance activity. It is built with security in mind, including input validation, session management, CSRF protection, and safe database access.

The project is ready for demonstration and small deployments, with a clear upgrade path for future improvements such as database migration, improved UI, and richer analytics.

## 14. References

- `README.md`
- `QUICKSTART.md`
- `SECURITY.md`
- `IMPLEMENTATION_SUMMARY.md`
- `app.py`
- `FILE_STRUCTURE.txt`
- `requirements.txt`
- Flask documentation: https://flask.palletsprojects.com/
- Werkzeug security docs: https://werkzeug.palletsprojects.com/
- python-dotenv docs: https://saurabh-kumar.com/python-dotenv/
