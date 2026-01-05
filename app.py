from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_
from config import Config
from models import db, User, StudentProfile, CompanyProfile, JobPosting, Application
from decorators import admin_required, student_required, company_required

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login"""
    return User.query.get(int(user_id))

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page and authentication"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember', False) == 'on'
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user, remember=remember)
            flash(f'Welcome back, {user.username}!', 'success')
            
            # Redirect to next page or dashboard
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registration page"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        role = request.form.get('role')
        
        # Validation
        if not all([username, email, password, confirm_password, role]):
            flash('All fields are required.', 'danger')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'danger')
            return render_template('register.html')
        
        if role not in ['student', 'company']:
            flash('Invalid role selected.', 'danger')
            return render_template('register.html')
        
        # Check if username or email already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'danger')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'danger')
            return render_template('register.html')
        
        # Create new user
        new_user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            role=role
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    """Logout functionality"""
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Protected dashboard page"""
    return render_template('dashboard.html')

@app.route('/admin')
@admin_required
def admin_panel():
    """Admin panel - admin only with statistics"""
    # Get statistics
    total_users = User.query.count()
    total_students = User.query.filter_by(role='student').count()
    total_companies = User.query.filter_by(role='company').count()
    approved_companies = User.query.filter_by(role='company', is_approved=True).count()
    pending_companies = User.query.filter_by(role='company', is_approved=False).count()
    
    total_drives = JobPosting.query.count()
    approved_drives = JobPosting.query.filter_by(is_approved=True).count()
    pending_drives = JobPosting.query.filter_by(is_approved=False).count()
    
    total_applications = Application.query.count()
    
    stats = {
        'total_users': total_users,
        'total_students': total_students,
        'total_companies': total_companies,
        'approved_companies': approved_companies,
        'pending_companies': pending_companies,
        'total_drives': total_drives,
        'approved_drives': approved_drives,
        'pending_drives': pending_drives,
        'total_applications': total_applications
    }
    
    return render_template('admin.html', stats=stats)

@app.route('/admin/companies')
@admin_required
def admin_companies():
    """View all companies"""
    search = request.args.get('search', '')
    if search:
        companies = CompanyProfile.query.join(User).filter(
            or_(
                CompanyProfile.company_name.ilike(f'%{search}%'),
                CompanyProfile.industry.ilike(f'%{search}%'),
                User.email.ilike(f'%{search}%')
            )
        ).all()
    else:
        companies = CompanyProfile.query.all()
    
    return render_template('admin_companies.html', companies=companies, search=search)

@app.route('/admin/company/approve/<int:user_id>')
@admin_required
def approve_company(user_id):
    """Approve a company"""
    user = User.query.get_or_404(user_id)
    if user.role != 'company':
        flash('Invalid user type.', 'danger')
        return redirect(url_for('admin_companies'))
    
    user.is_approved = True
    db.session.commit()
    flash(f'Company {user.username} approved successfully!', 'success')
    return redirect(url_for('admin_companies'))

@app.route('/admin/company/reject/<int:user_id>')
@admin_required
def reject_company(user_id):
    """Reject a company"""
    user = User.query.get_or_404(user_id)
    if user.role != 'company':
        flash('Invalid user type.', 'danger')
        return redirect(url_for('admin_companies'))
    
    user.is_approved = False
    db.session.commit()
    flash(f'Company {user.username} rejected.', 'warning')
    return redirect(url_for('admin_companies'))

@app.route('/admin/students')
@admin_required
def admin_students():
    """View all students"""
    search = request.args.get('search', '')
    if search:
        students = StudentProfile.query.join(User).filter(
            or_(
                StudentProfile.full_name.ilike(f'%{search}%'),
                StudentProfile.roll_number.ilike(f'%{search}%'),
                StudentProfile.branch.ilike(f'%{search}%'),
                User.email.ilike(f'%{search}%')
            )
        ).all()
    else:
        students = StudentProfile.query.all()
    
    return render_template('admin_students.html', students=students, search=search)

@app.route('/admin/drives')
@admin_required
def admin_drives():
    """View all drives (job postings)"""
    search = request.args.get('search', '')
    if search:
        drives = JobPosting.query.join(CompanyProfile).filter(
            or_(
                JobPosting.title.ilike(f'%{search}%'),
                JobPosting.location.ilike(f'%{search}%'),
                CompanyProfile.company_name.ilike(f'%{search}%')
            )
        ).all()
    else:
        drives = JobPosting.query.all()
    
    return render_template('admin_drives.html', drives=drives, search=search)

@app.route('/admin/drive/approve/<int:drive_id>')
@admin_required
def approve_drive(drive_id):
    """Approve a drive"""
    drive = JobPosting.query.get_or_404(drive_id)
    drive.is_approved = True
    db.session.commit()
    flash(f'Drive "{drive.title}" approved successfully!', 'success')
    return redirect(url_for('admin_drives'))

@app.route('/admin/drive/reject/<int:drive_id>')
@admin_required
def reject_drive(drive_id):
    """Reject a drive"""
    drive = JobPosting.query.get_or_404(drive_id)
    drive.is_approved = False
    db.session.commit()
    flash(f'Drive "{drive.title}" rejected.', 'warning')
    return redirect(url_for('admin_drives'))

@app.route('/admin/applications')
@admin_required
def admin_applications():
    """View all applications"""
    applications = Application.query.all()
    return render_template('admin_applications.html', applications=applications)

@app.route('/admin/user/toggle/<int:user_id>')
@admin_required
def toggle_user(user_id):
    """Activate/Deactivate (blacklist) a user"""
    user = User.query.get_or_404(user_id)
    if user.role == 'admin':
        flash('Cannot deactivate admin users.', 'danger')
        return redirect(url_for('admin_panel'))
    
    user.is_active = not user.is_active
    db.session.commit()
    status = 'activated' if user.is_active else 'deactivated'
    flash(f'User {user.username} {status} successfully!', 'success')
    
    # Redirect to appropriate page based on role
    if user.role == 'company':
        return redirect(url_for('admin_companies'))
    elif user.role == 'student':
        return redirect(url_for('admin_students'))
    else:
        return redirect(url_for('admin_panel'))


@app.route('/student/profile')
@student_required
def student_profile():
    """Student profile page - student only"""
    profile = StudentProfile.query.filter_by(user_id=current_user.id).first()
    return render_template('student_profile.html', profile=profile)

@app.route('/company/profile')
@company_required
def company_profile():
    """Company profile page - company only"""
    profile = CompanyProfile.query.filter_by(user_id=current_user.id).first()
    return render_template('company_profile.html', profile=profile)

@app.route('/company/dashboard')
@company_required
def company_dashboard():
    """Company dashboard with statistics"""
    profile = CompanyProfile.query.filter_by(user_id=current_user.id).first()
    
    if profile:
        # Get company's drives statistics
        total_drives = JobPosting.query.filter_by(company_id=profile.id).count()
        active_drives = JobPosting.query.filter_by(company_id=profile.id, is_active=True).count()
        approved_drives = JobPosting.query.filter_by(company_id=profile.id, is_approved=True).count()
        pending_drives = JobPosting.query.filter_by(company_id=profile.id, is_approved=False).count()
        
        # Get total applications for company's drives
        total_applications = db.session.query(Application).join(JobPosting).filter(
            JobPosting.company_id == profile.id
        ).count()
        
        # Get applications by status
        pending_applications = db.session.query(Application).join(JobPosting).filter(
            JobPosting.company_id == profile.id,
            Application.status == 'pending'
        ).count()
        
        shortlisted_applications = db.session.query(Application).join(JobPosting).filter(
            JobPosting.company_id == profile.id,
            Application.status == 'shortlisted'
        ).count()
        
        stats = {
            'total_drives': total_drives,
            'active_drives': active_drives,
            'approved_drives': approved_drives,
            'pending_drives': pending_drives,
            'total_applications': total_applications,
            'pending_applications': pending_applications,
            'shortlisted_applications': shortlisted_applications
        }
    else:
        stats = {
            'total_drives': 0,
            'active_drives': 0,
            'approved_drives': 0,
            'pending_drives': 0,
            'total_applications': 0,
            'pending_applications': 0,
            'shortlisted_applications': 0
        }
    
    return render_template('company_dashboard.html', profile=profile, stats=stats)

@app.route('/company/drive/create', methods=['GET', 'POST'])
@company_required
def create_drive():
    """Create a new placement drive"""
    profile = CompanyProfile.query.filter_by(user_id=current_user.id).first()
    
    if not profile:
        flash('Please complete your company profile first.', 'warning')
        return redirect(url_for('company_profile'))
    
    if not current_user.is_approved:
        flash('Your company account needs admin approval before posting drives.', 'warning')
        return redirect(url_for('company_dashboard'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        requirements = request.form.get('requirements')
        salary = request.form.get('salary')
        location = request.form.get('location')
        job_type = request.form.get('job_type')
        deadline_str = request.form.get('deadline')
        
        # Validation
        if not all([title, description, requirements, location, job_type, deadline_str]):
            flash('All required fields must be filled.', 'danger')
            return render_template('create_drive.html', profile=profile)
        
        try:
            from datetime import datetime
            deadline = datetime.strptime(deadline_str, '%Y-%m-%d')
            
            # Create new drive
            new_drive = JobPosting(
                company_id=profile.id,
                title=title,
                description=description,
                requirements=requirements,
                salary=salary,
                location=location,
                job_type=job_type,
                deadline=deadline,
                is_active=True,
                is_approved=False  # Requires admin approval
            )
            
            db.session.add(new_drive)
            db.session.commit()
            
            flash('Drive created successfully! Waiting for admin approval.', 'success')
            return redirect(url_for('company_drives'))
        except ValueError:
            flash('Invalid date format.', 'danger')
            return render_template('create_drive.html', profile=profile)
    
    return render_template('create_drive.html', profile=profile)

@app.route('/company/drives')
@company_required
def company_drives():
    """View all company drives"""
    profile = CompanyProfile.query.filter_by(user_id=current_user.id).first()
    
    if profile:
        drives = JobPosting.query.filter_by(company_id=profile.id).order_by(JobPosting.posted_at.desc()).all()
    else:
        drives = []
    
    return render_template('company_drives.html', profile=profile, drives=drives)

@app.route('/company/drive/edit/<int:drive_id>', methods=['GET', 'POST'])
@company_required
def edit_drive(drive_id):
    """Edit a placement drive"""
    profile = CompanyProfile.query.filter_by(user_id=current_user.id).first()
    drive = JobPosting.query.get_or_404(drive_id)
    
    # Check ownership
    if drive.company_id != profile.id:
        flash('You do not have permission to edit this drive.', 'danger')
        return redirect(url_for('company_drives'))
    
    if request.method == 'POST':
        drive.title = request.form.get('title')
        drive.description = request.form.get('description')
        drive.requirements = request.form.get('requirements')
        drive.salary = request.form.get('salary')
        drive.location = request.form.get('location')
        drive.job_type = request.form.get('job_type')
        deadline_str = request.form.get('deadline')
        
        try:
            from datetime import datetime
            drive.deadline = datetime.strptime(deadline_str, '%Y-%m-%d')
            
            db.session.commit()
            flash('Drive updated successfully!', 'success')
            return redirect(url_for('company_drives'))
        except ValueError:
            flash('Invalid date format.', 'danger')
    
    return render_template('edit_drive.html', profile=profile, drive=drive)

@app.route('/company/drive/delete/<int:drive_id>')
@company_required
def delete_drive(drive_id):
    """Delete a placement drive"""
    profile = CompanyProfile.query.filter_by(user_id=current_user.id).first()
    drive = JobPosting.query.get_or_404(drive_id)
    
    # Check ownership
    if drive.company_id != profile.id:
        flash('You do not have permission to delete this drive.', 'danger')
        return redirect(url_for('company_drives'))
    
    db.session.delete(drive)
    db.session.commit()
    flash('Drive deleted successfully!', 'success')
    return redirect(url_for('company_drives'))

@app.route('/company/drive/toggle/<int:drive_id>')
@company_required
def toggle_drive(drive_id):
    """Close/Open a placement drive"""
    profile = CompanyProfile.query.filter_by(user_id=current_user.id).first()
    drive = JobPosting.query.get_or_404(drive_id)
    
    # Check ownership
    if drive.company_id != profile.id:
        flash('You do not have permission to modify this drive.', 'danger')
        return redirect(url_for('company_drives'))
    
    drive.is_active = not drive.is_active
    db.session.commit()
    
    status = 'opened' if drive.is_active else 'closed'
    flash(f'Drive "{drive.title}" {status} successfully!', 'success')
    return redirect(url_for('company_drives'))

@app.route('/company/drive/<int:drive_id>/applicants')
@company_required
def view_applicants(drive_id):
    """View applicants for a specific drive"""
    profile = CompanyProfile.query.filter_by(user_id=current_user.id).first()
    drive = JobPosting.query.get_or_404(drive_id)
    
    # Check ownership
    if drive.company_id != profile.id:
        flash('You do not have permission to view these applicants.', 'danger')
        return redirect(url_for('company_drives'))
    
    # Get all applications for this drive with student details
    applications = Application.query.filter_by(job_id=drive_id).order_by(Application.applied_at.desc()).all()
    
    return render_template('view_applicants.html', profile=profile, drive=drive, applications=applications)

@app.route('/company/application/<int:application_id>/update-status', methods=['POST'])
@company_required
def update_application_status(application_id):
    """Update application status"""
    profile = CompanyProfile.query.filter_by(user_id=current_user.id).first()
    application = Application.query.get_or_404(application_id)
    
    # Check ownership through drive
    if application.job.company_id != profile.id:
        flash('You do not have permission to update this application.', 'danger')
        return redirect(url_for('company_drives'))
    
    new_status = request.form.get('status')
    if new_status in ['pending', 'reviewed', 'shortlisted', 'rejected', 'accepted']:
        application.status = new_status
        db.session.commit()
        flash(f'Application status updated to {new_status}.', 'success')
    else:
        flash('Invalid status.', 'danger')
    
    return redirect(url_for('view_applicants', drive_id=application.job_id))

@app.route('/company/drive/<int:drive_id>/shortlist', methods=['POST'])
@company_required
def shortlist_applicants(drive_id):
    """Shortlist multiple applicants"""
    profile = CompanyProfile.query.filter_by(user_id=current_user.id).first()
    drive = JobPosting.query.get_or_404(drive_id)
    
    # Check ownership
    if drive.company_id != profile.id:
        flash('You do not have permission to modify these applications.', 'danger')
        return redirect(url_for('company_drives'))
    
    application_ids = request.form.getlist('application_ids')
    
    if application_ids:
        count = 0
        for app_id in application_ids:
            application = Application.query.get(int(app_id))
            if application and application.job_id == drive_id:
                application.status = 'shortlisted'
                count += 1
        
        db.session.commit()
        flash(f'{count} applicant(s) shortlisted successfully!', 'success')
    else:
        flash('No applicants selected.', 'warning')
    
    return redirect(url_for('view_applicants', drive_id=drive_id))

if __name__ == '__main__':
    app.run(debug=True)
