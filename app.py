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
    
    # Redirect to appropriate page
    if user.role == 'company':
        return redirect(url_for('admin_companies'))
    else:
        return redirect(url_for('admin_students'))


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

if __name__ == '__main__':
    app.run(debug=True)
