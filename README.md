# Placement Portal Application

A comprehensive Flask-based web application for managing campus placements, job postings, and student applications.

## Phase 1: Setup & Authentication Implementation ✅

This phase implements the complete authentication system with role-based access control.

## Phase 2: Admin Module Implementation ✅

This phase implements the complete admin dashboard with statistics, approval systems, search functionality, and user management.

## Phase 3: Company Module Implementation ✅

This phase implements the complete company dashboard with drive management, applicant viewing, and status update capabilities.

## Phase 4: Student Module Implementation ✅

This phase implements the complete student dashboard with profile management, drive browsing with filters, application submission, and application tracking.

## Phase 5: Validation & Polish Implementation ✅

This phase implements comprehensive form validation (frontend + backend), confirmation dialogs, enhanced UX, and code quality improvements.

## Features

### Authentication & Authorization
- ✅ User registration with role selection (Student/Company)
- ✅ Secure login with password hashing
- ✅ Session management with Flask-Login
- ✅ Remember me functionality
- ✅ Role-based access control (Admin, Student, Company)
- ✅ Protected routes with decorators

### Admin Module (Phase 2)
- ✅ **Dashboard with Statistics:** Real-time counts of users, students, companies, drives, and applications
- ✅ **Company Approval System:** Approve/reject company registrations
- ✅ **Drive Approval System:** Approve/reject job postings (drives)
- ✅ **Search Functionality:** Search students, companies, and drives
- ✅ **Blacklist/Deactivate:** Toggle user active status
- ✅ **Entity Management:** View and manage all students, companies, drives, and applications

### Company Module (Phase 3)
- ✅ **Company Dashboard:** Statistics for drives, applications, and shortlisted candidates
- ✅ **Drive Creation:** Create placement drives with detailed job information
- ✅ **Drive Management:** Edit, delete, and open/close drives
- ✅ **Applicant Viewing:** View all applicants for each drive with details
- ✅ **Status Updates:** Update individual application status (reviewed, shortlisted, rejected, accepted)
- ✅ **Bulk Shortlisting:** Select and shortlist multiple applicants at once

### Student Module (Phase 4)
- ✅ **Student Dashboard:** Statistics for available drives, applications, shortlisted, and accepted
- ✅ **Profile Management:** Create and edit student profile with academic details
- ✅ **Drive Browsing:** Browse drives with advanced filters (search, job type, location)
- ✅ **Drive Details:** View complete job descriptions, requirements, and company info
- ✅ **Application Submission:** Apply to drives with optional cover letter
- ✅ **Application Tracking:** View all applications with status tracking
- ✅ **Application Details:** Detailed view with status visualization
- ✅ **Placement History:** View all accepted placements

### Validation & Polish (Phase 5)
- ✅ **Frontend Validation:** Real-time password confirmation, CGPA (0-10), phone (10 digits), date validation
- ✅ **Backend Validation:** Length limits (title: 200, description/requirements: 2000, cover letter: 1000 chars)
- ✅ **UX Enhancements:** Confirmation dialogs, auto-dismiss alerts, form loading states, character counters
- ✅ **Data Integrity:** Comprehensive validation on both frontend and backend for all inputs
- ✅ **Code Quality:** PEP 8 compliance, constants for magic numbers, optimized regex patterns

### Database Models
- ✅ User model with authentication, approval, and active status
- ✅ Student profile management
- ✅ Company profile management
- ✅ Job posting system with approval workflow
- ✅ Application tracking

### User Interface
- ✅ Responsive Bootstrap 5 design
- ✅ Dynamic navigation based on user role
- ✅ Flash messaging system
- ✅ Form validation (client & server-side)
- ✅ Role-specific dashboards
- ✅ Statistics cards with visual indicators
- ✅ Search forms with placeholders
- ✅ Status badges (Active/Blacklisted, Approved/Pending, Application Status)
- ✅ Card-based drive display
- ✅ Bulk selection with JavaScript
- ✅ Timeline visualizations

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
│   ├── admin.html              # Admin dashboard
│   ├── admin_companies.html    # Company management
│   ├── admin_students.html     # Student management
│   ├── admin_drives.html       # Drive management
│   ├── admin_applications.html # Applications view
│   ├── student_profile.html    # Student profile
│   └── company_profile.html    # Company profile
└── static/              # Static assets
    ├── css/
    │   └── style.css    # Custom styles
    └── js/
        └── script.js    # Form validation
```

## Usage

### Admin User
1. Login with admin credentials (username: `admin`, password: `admin123`)
2. Access Admin Dashboard to view statistics
3. **Manage Companies:**
   - View all registered companies
   - Approve/reject company registrations
   - Search companies by name, industry, or email
   - Blacklist/activate companies
4. **Manage Students:**
   - View all registered students
   - Search students by name, roll number, or branch
   - Blacklist/activate students
5. **Manage Drives (Job Postings):**
   - View all job postings
   - Approve/reject drives
   - Search drives by title, location, or company
6. **View Applications:**
   - Monitor all job applications
   - Track application status

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
5. **Note:** Company account requires admin approval before posting jobs
6. **Company Features:**
   - Complete company profile with business details
   - View company dashboard with statistics
   - Create placement drives with job details
   - Edit and manage existing drives
   - Open/Close drives to control applications
   - View all applicants for each drive
   - Update application status (reviewed, shortlisted, rejected, accepted)
   - Bulk shortlist multiple candidates

## Security Features

### Implemented
- ✅ Password hashing with Werkzeug
- ✅ Session management with secure cookies
- ✅ Role-based access control
- ✅ SQL injection protection (SQLAlchemy ORM)
- ✅ CSRF protection ready (use Flask-WTF for forms in production)

### Security Notes
⚠️ **Development Setup:** This is Phase 1 & 2 development setup. For production deployment:
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

### Admin Routes (Phase 2)
- `/admin` - Admin dashboard with statistics (admin role required)
- `/admin/companies` - Manage companies with approval (admin role required)
- `/admin/company/approve/<id>` - Approve company (admin role required)
- `/admin/company/reject/<id>` - Reject company (admin role required)
- `/admin/students` - Manage students (admin role required)
- `/admin/drives` - Manage drives/job postings (admin role required)
- `/admin/drive/approve/<id>` - Approve drive (admin role required)
- `/admin/drive/reject/<id>` - Reject drive (admin role required)
- `/admin/applications` - View all applications (admin role required)
- `/admin/user/toggle/<id>` - Activate/blacklist user (admin role required)

### Student Routes (Phase 4)
- `/student/profile` - Student profile (student role required)
- `/student/dashboard` - Student dashboard with statistics (student role required)
- `/student/profile/edit` - Create/edit student profile (student role required)
- `/student/drives` - Browse available drives with filters (student role required)
- `/student/drive/<id>` - View drive details (student role required)
- `/student/drive/<id>/apply` - Apply to drive (student role required)
- `/student/applications` - View all applications (student role required)
- `/student/application/<id>` - View application details (student role required)
- `/student/placement-history` - View accepted placements (student role required)

### Company Routes (Phase 3)
- `/company/profile` - Company profile (company role required)
- `/company/dashboard` - Company dashboard with statistics (company role required)
- `/company/drive/create` - Create new placement drive (company role required)
- `/company/drives` - View and manage all drives (company role required)
- `/company/drive/edit/<id>` - Edit drive details (company role required)
- `/company/drive/delete/<id>` - Delete drive (company role required)
- `/company/drive/toggle/<id>` - Open/Close drive (company role required)
- `/company/drive/<id>/applicants` - View applicants for drive (company role required)
- `/company/application/<id>/update-status` - Update application status (company role required)
- `/company/drive/<id>/shortlist` - Bulk shortlist applicants (company role required)

## Database Schema

### Users Table
- id, username, email, password_hash, role, created_at, **is_active, is_approved**

### Student Profiles Table
- id, user_id, full_name, roll_number, branch, cgpa, resume_path, phone

### Company Profiles Table
- id, user_id, company_name, industry, description, website, contact_person, contact_email, contact_phone

### Job Postings Table
- id, company_id, title, description, requirements, salary, location, job_type, posted_at, deadline, is_active, **is_approved**

### Applications Table
- id, job_id, user_id, status, applied_at, cover_letter

## Testing

The application has been tested with:

**Phase 1:**
- ✅ Admin login and logout
- ✅ Student registration and login
- ✅ Role-based access control
- ✅ Form validation
- ✅ Database operations
- ✅ Flash messaging
- ✅ Responsive UI

**Phase 2:**
- ✅ Admin dashboard with statistics
- ✅ Company approval/rejection workflow
- ✅ Drive approval/rejection workflow
- ✅ Search functionality for all entities
- ✅ Blacklist/activate user functionality
- ✅ All management pages rendering correctly
- ✅ Database schema updates

**Phase 3:**
- ✅ Company dashboard with drive statistics
- ✅ Drive creation with validation
- ✅ Drive management (edit, delete, toggle)
- ✅ Applicant viewing system
- ✅ Application status updates
- ✅ Bulk shortlisting functionality
- ✅ Ownership validation for all operations
- ✅ Navigation updates

**Phase 4:**
- ✅ Student dashboard with application statistics
- ✅ Profile creation and editing
- ✅ Drive browsing with filters (search, job type, location)
- ✅ Drive details view
- ✅ Application submission with cover letter
- ✅ Application tracking and status viewing
- ✅ Application details with status visualization
- ✅ Placement history for accepted applications
- ✅ Duplicate application prevention
- ✅ Deadline validation

**Phase 5:**
- ✅ Frontend validation (password confirmation, CGPA, phone, date)
- ✅ Backend validation (length limits, format checks)
- ✅ Confirmation dialogs for critical actions
- ✅ Auto-dismiss flash messages
- ✅ Form submission loading states with spinners
- ✅ Character counters on textareas
- ✅ Code quality improvements (PEP 8, constants)
- ✅ Visual validation feedback (is-valid/is-invalid classes)

## Future Enhancements (Phase 6+)

- [ ] Resume upload and management
- [ ] Email notifications for approvals and applications
- [ ] Advanced analytics dashboard with charts
- [ ] Export reports (PDF/CSV)
- [ ] Bulk operations for admin

## Contributing

This is an educational project. Feel free to fork and modify for your needs.

## License

This project is created for educational purposes.

## Author

DevK-26

---

**Note:** Phase 1, 2, 3, 4 & 5 complete. The application now includes full authentication, comprehensive admin module, complete company module with drive management and applicant tracking, complete student module with profile management, drive browsing, and application tracking, plus enterprise-grade form validation and UX enhancements.
