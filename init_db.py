from login import app, db, User
from werkzeug.security import generate_password_hash

def init_database():
    with app.app_context():
        # Create all tables
        db.create_all()

        # Check if test user already exists
        test_user = User.query.filter_by(username='test').first()
        if not test_user:
            # Create a test user
            test_user = User(
                username='test',
                password=generate_password_hash('test123')
            )
            db.session.add(test_user)

        # Create another test user
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            admin_user = User(
                username='admin',
                password=generate_password_hash('admin123')
            )
            db.session.add(admin_user)

        # Commit the changes
        try:
            db.session.commit()
            print("Database initialized successfully!")
            print("Test Users Created:")
            print("1. Username: test, Password: test123")
            print("2. Username: admin, Password: admin123")
        except Exception as e:
            print(f"Error initializing database: {e}")
            db.session.rollback()

if __name__ == "__main__":
    init_database()
