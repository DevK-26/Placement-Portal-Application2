from app import app, db
from models import User
from werkzeug.security import generate_password_hash

def init_database():
    """Initialize database and create default admin user"""
    with app.app_context():
        # Create all tables
        print("Creating database tables...")
        db.create_all()
        print("✓ Database tables created successfully!")
        
        # Check if admin user already exists
        admin = User.query.filter_by(username='admin').first()
        
        if admin:
            print("✓ Admin user already exists.")
        else:
            # Create default admin user
            print("Creating default admin user...")
            admin_user = User(
                username='admin',
                email='admin@placementportal.com',
                password_hash=generate_password_hash('admin123'),
                role='admin'
            )
            db.session.add(admin_user)
            db.session.commit()
            print("✓ Default admin user created successfully!")
            print("  Username: admin")
            print("  Email: admin@placementportal.com")
            print("  Password: admin123")
        
        print("\nDatabase initialization complete!")

if __name__ == '__main__':
    init_database()
