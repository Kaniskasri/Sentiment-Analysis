# from flask import Flask, render_template, request, redirect, url_for, flash, session
# from flask_sqlalchemy import SQLAlchemy
# from werkzeug.security import generate_password_hash, check_password_hash
# import subprocess
# import os
# import sys
# import time

# app = Flask(__name__)
# app.secret_key = 'your_secret_key_here'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

# # Global variable to track Streamlit process
# streamlit_process = None

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     password = db.Column(db.String(120), nullable=False)

# def create_tables():
#     with app.app_context():
#         db.create_all()

# def start_streamlit():
#     """Function to start Streamlit server"""
#     global streamlit_process
#     if streamlit_process is None:
#         try:
#             # Get the path to the current directory
#             current_dir = os.path.dirname(os.path.abspath(__file__))
#             app_path = os.path.join(current_dir, 'app.py')
            
#             # Start Streamlit process
#             if os.name == 'nt':  # Windows
#                 streamlit_process = subprocess.Popen(
#                     ['streamlit', 'run', app_path],
#                     creationflags=subprocess.CREATE_NEW_CONSOLE
#                 )
#             else:  # Unix/Linux/Mac
#                 streamlit_process = subprocess.Popen(
#                     ['streamlit', 'run', app_path]
#                 )
            
#             # Wait for Streamlit to start
#             time.sleep(5)
#             return True
#         except Exception as e:
#             print(f"Error starting Streamlit: {e}")
#             return False
#     return True

# @app.route('/')
# def home():
#     if 'username' not in session:
#         return redirect(url_for('login'))
    
#     # Start Streamlit when user is logged in
#     if start_streamlit():
#         return redirect('http://localhost:8501')
#     else:
#         flash('Error starting the application')
#         return redirect(url_for('login'))

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
        
#         user = User.query.filter_by(username=username).first()
        
#         if user and check_password_hash(user.password, password):
#             session['username'] = username
            
#             # Start Streamlit when user logs in
#             if start_streamlit():
#                 return redirect('http://localhost:8501')
#             else:
#                 flash('Error starting the application')
#                 return redirect(url_for('login'))
#         else:
#             flash('Invalid username or password')
    
#     return render_template('login.html')

# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
        
#         if User.query.filter_by(username=username).first():
#             flash('Username already exists')
#             return redirect(url_for('signup'))
        
#         hashed_password = generate_password_hash(password)
#         new_user = User(username=username, password=hashed_password)
        
#         try:
#             db.session.add(new_user)
#             db.session.commit()
#             flash('Registration successful! Please login.')
#             return redirect(url_for('login'))
#         except Exception as e:
#             print(f"Error during registration: {e}")
#             flash('Error occurred during registration')
#             return redirect(url_for('signup'))
    
#     return render_template('signup.html')

# @app.route('/logout')
# def logout():
#     global streamlit_process
    
#     # Clear the session
#     session.clear()
    
#     # Stop Streamlit process
#     if streamlit_process:
#         try:
#             if os.name == 'nt':  # Windows
#                 subprocess.run(['taskkill', '/F', '/T', '/PID', str(streamlit_process.pid)])
#             else:  # Unix/Linux/Mac
#                 streamlit_process.terminate()
#             streamlit_process = None
#         except Exception as e:
#             print(f"Error stopping Streamlit: {e}")
    
#     return redirect(url_for('login'))

# def cleanup():
#     """Cleanup function to be called when the Flask app stops"""
#     global streamlit_process
#     if streamlit_process:
#         try:
#             streamlit_process.terminate()
#         except:
#             pass

# # Create tables before running the app
# create_tables()

# if __name__ == '__main__':
#     try:
#         # Make sure no Streamlit process is running
#         if os.name == 'nt':  # Windows
#             os.system('taskkill /F /IM streamlit.exe 2>nul')
#         else:  # Unix/Linux/Mac
#             os.system('pkill streamlit')
        
#         # Run the Flask app
#         app.run(debug=True, port=5000)
#     finally:
#         cleanup()





# from flask import Flask, render_template, request, redirect, url_for, flash, session
# from flask_sqlalchemy import SQLAlchemy
# from werkzeug.security import generate_password_hash, check_password_hash
# import subprocess
# import os
# import sys
# import time

# app = Flask(__name__)
# app.secret_key = 'your_secret_key_here'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

# # Global variable to track Streamlit process
# streamlit_process = None

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     password = db.Column(db.String(120), nullable=False)

# def create_tables():
#     with app.app_context():
#         db.create_all()

# def start_streamlit():
#     """Function to start Streamlit server"""
#     global streamlit_process
#     if streamlit_process is None:
#         try:
#             # Get the path to the current directory
#             current_dir = os.path.dirname(os.path.abspath(__file__))
#             app_path = os.path.join(current_dir, 'app.py')
            
#             # Start Streamlit process
#             if os.name == 'nt':  # Windows
#                 streamlit_process = subprocess.Popen(
#                     ['streamlit', 'run', app_path],
#                     creationflags=subprocess.CREATE_NEW_CONSOLE
#                 )
#             else:  # Unix/Linux/Mac
#                 streamlit_process = subprocess.Popen(
#                     ['streamlit', 'run', app_path]
#                 )
            
#             # Wait for Streamlit to start
#             time.sleep(5)
#             return True
#         except Exception as e:
#             print(f"Error starting Streamlit: {e}")
#             return False
#     return True

# @app.route('/')
# def home():
#     # Redirect to login if not logged in
#     if 'username' not in session:
#         return redirect(url_for('login'))
#     return redirect(url_for('dashboard'))

# @app.route('/dashboard')
# def dashboard():
#     # Check if user is logged in
#     if 'username' not in session:
#         return redirect(url_for('login'))
    
#     # Start Streamlit when user is logged in
#     if start_streamlit():
#         return redirect('http://localhost:8501')
#     else:
#         flash('Error starting the application')
#         return redirect(url_for('login'))

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     # If user is already logged in, redirect to dashboard
#     if 'username' in session:
#         return redirect(url_for('dashboard'))

#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
        
#         user = User.query.filter_by(username=username).first()
        
#         if user and check_password_hash(user.password, password):
#             session['username'] = username
#             return redirect(url_for('dashboard'))
#         else:
#             flash('Invalid username or password')
    
#     return render_template('login.html')

# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     # If user is already logged in, redirect to dashboard
#     if 'username' in session:
#         return redirect(url_for('dashboard'))

#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
        
#         if User.query.filter_by(username=username).first():
#             flash('Username already exists')
#             return redirect(url_for('signup'))
        
#         hashed_password = generate_password_hash(password)
#         new_user = User(username=username, password=hashed_password)
        
#         try:
#             db.session.add(new_user)
#             db.session.commit()
#             flash('Registration successful! Please login.')
#             return redirect(url_for('login'))
#         except Exception as e:
#             print(f"Error during registration: {e}")
#             flash('Error occurred during registration')
#             return redirect(url_for('signup'))
    
#     return render_template('signup.html')

# @app.route('/logout')
# def logout():
#     global streamlit_process
    
#     # Clear the session
#     session.clear()
    
#     # Stop Streamlit process
#     if streamlit_process:
#         try:
#             if os.name == 'nt':  # Windows
#                 subprocess.run(['taskkill', '/F', '/T', '/PID', str(streamlit_process.pid)])
#             else:  # Unix/Linux/Mac
#                 streamlit_process.terminate()
#             streamlit_process = None
#         except Exception as e:
#             print(f"Error stopping Streamlit: {e}")
    
#     return redirect(url_for('login'))

# def cleanup():
#     """Cleanup function to be called when the Flask app stops"""
#     global streamlit_process
#     if streamlit_process:
#         try:
#             streamlit_process.terminate()
#         except:
#             pass

# # Create tables before running the app
# create_tables()

# if __name__ == '__main__':
#     try:
#         # Make sure no Streamlit process is running
#         if os.name == 'nt':  # Windows
#             os.system('taskkill /F /IM streamlit.exe 2>nul')
#         else:  # Unix/Linux/Mac
#             os.system('pkill streamlit')
        
#         # Run the Flask app
#         app.run(debug=True, port=5000)
#     finally:
#         cleanup()

