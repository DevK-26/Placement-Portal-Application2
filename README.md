# Placement Portal Application

A comprehensive Flask-based web application for managing campus placements, job postings, and student applications.

## Phase 1: Setup & Authentication Implementation ✅

This phase implements the complete authentication system with role-based access control.

## Features

### Authentication & Authorization
- ✅ User registration with role selection (Student/Company)
- ✅ Secure login with password hashing
- ✅ Session management with Flask-Login
- ✅ Remember me functionality
- ✅ Role-based access control (Admin, Student, Company)
- ✅ Protected routes with decorators

### Database Models
- ✅ User model with authentication
- ✅ Student profile management
- ✅ Company profile management
- ✅ Job posting system
- ✅ Application tracking

### User Interface
- ✅ Responsive Bootstrap 5 design
- ✅ Dynamic navigation based on user role
- ✅ Flash messaging system
- ✅ Form validation (client & server-side)
- ✅ Role-specific dashboards

## Tech Stack

- **Backend:** Flask 3.0.0
- **Database:** SQLite with SQLAlchemy 3.1.1
- **Authentication:** Flask-Login 0.6.3
- **Password Security:** Werkzeug 3.0.1
- **Frontend:** Bootstrap 5, Bootstrap Icons
- **JavaScript:** Vanilla JS for form validation

## Installation

1. **Clone the repository:**
```bash
git clone https://github.com/DevK-26/Placement-Portal-Application2.git
cd Placement-Portal-Application2
```

2. **Create a virtual environment (recommended):**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Initialize the database:**
```bash
python init_db.py
```

This will create all database tables and seed the default admin user.

5. **Run the application:**
```bash
python app.py
```

6. **Access the application:**
Open your browser and navigate to `http://127.0.0.1:5000`

## Default Admin Credentials

After running `init_db.py`, you can login with:
- **Username:** `admin`
- **Password:** `admin123`
- **Email:** `admin@placementportal.com`

⚠️ **Important:** Change these credentials in production!

## Project Structure

```
Placement-Portal-Application2/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── models.py             # Database models
├── decorators.py         # Role-based access decorators
├── init_db.py           # Database initialization script
├── requirements.txt      # Python dependencies
├── .gitignore           # Git ignore rules
├── templates/           # HTML templates
│   ├── base.html        # Base template with navbar
│   ├── index.html       # Landing page
│   ├── login.html       # Login page
│   ├── register.html    # Registration page
│   ├── dashboard.html   # User dashboard
│   ├── admin.html       # Admin panel
│   ├── student_profile.html   # Student profile
│   └── company_profile.html   # Company profile
└── static/              # Static assets
    ├── css/
    │   └── style.css    # Custom styles
    └── js/
        └── script.js    # Form validation
```

## Usage

### Admin User
1. Login with admin credentials
2. Access Admin Panel to view all users
3. Manage system-wide settings

### Student Registration
1. Click "Register" on the homepage
2. Fill in username, email, password
3. Select "Student" as role
4. After registration, login with credentials
5. Access student-specific features

### Company Registration
1. Click "Register" on the homepage
2. Fill in username, email, password
3. Select "Company" as role
4. After registration, login with credentials
5. Access company-specific features

## Security Features

### Implemented
- ✅ Password hashing with Werkzeug
- ✅ Session management with secure cookies
- ✅ Role-based access control
- ✅ SQL injection protection (SQLAlchemy ORM)
- ✅ CSRF protection ready (use Flask-WTF for forms in production)

### Security Notes
⚠️ **Development Setup:** This is Phase 1 development setup. For production deployment:
1. Disable debug mode in `app.py`
2. Use environment variables for SECRET_KEY
3. Use a production WSGI server (Gunicorn, uWSGI)
4. Enable HTTPS
5. Implement CSRF protection with Flask-WTF
6. Add rate limiting for authentication endpoints
7. Use a production-grade database (PostgreSQL, MySQL)
8. Implement proper logging and monitoring

## Routes

### Public Routes
- `/` - Home page
- `/login` - Login page
- `/register` - Registration page

### Protected Routes
- `/dashboard` - User dashboard (login required)
- `/logout` - Logout (login required)

### Admin Routes
- `/admin` - Admin panel (admin role required)

### Student Routes
- `/student/profile` - Student profile (student role required)

### Company Routes
- `/company/profile` - Company profile (company role required)

## Database Schema

### Users Table
- id, username, email, password_hash, role, created_at

### Student Profiles Table
- id, user_id, full_name, roll_number, branch, cgpa, resume_path, phone

### Company Profiles Table
- id, user_id, company_name, industry, description, website, contact_person, contact_email, contact_phone

### Job Postings Table
- id, company_id, title, description, requirements, salary, location, job_type, posted_at, deadline, is_active

### Applications Table
- id, job_id, user_id, status, applied_at, cover_letter

## Testing

The application has been tested with:
- ✅ Admin login and logout
- ✅ Student registration and login
- ✅ Role-based access control
- ✅ Form validation
- ✅ Database operations
- ✅ Flash messaging
- ✅ Responsive UI

## Future Enhancements (Phase 2+)

- [ ] Profile editing for students and companies
- [ ] Job posting creation and management
- [ ] Job application submission
- [ ] Application status tracking
- [ ] File upload for resumes
- [ ] Email notifications
- [ ] Advanced search and filtering
- [ ] Analytics dashboard
- [ ] Export reports

## Contributing

This is an educational project. Feel free to fork and modify for your needs.

## License

This project is created for educational purposes.

## Author

DevK-26

---

**Note:** This is Phase 1 of the Placement Portal Application. More features will be added in subsequent phases.
