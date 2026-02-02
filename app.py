"""
Flask Web Application for AI-Powered Job Application Agent
Run on localhost for web interface
"""

import os
import sys
import json
import re
from flask import Flask, render_template, request, jsonify, send_file, flash, redirect, url_for
from dotenv import load_dotenv
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from models import init_db, Profile, User

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

# Import our modular components
from utils.deepseek_client import DeepSeekClient
from utils.document_builder import DocumentBuilder
from utils.match_calculator import MatchCalculator
from agents.job_analyzer import JobAnalyzer
from agents.cv_customizer import CVCustomizer
from agents.cover_letter_generator import CoverLetterGenerator

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')

# Initialize database (SQLite by default, configurable via DATABASE_URL)
init_db(app)

# Configure login manager
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id: str):
    try:
        return User.query.get(int(user_id))
    except Exception:
        return None


# Global variables for initialized components
client = None
builder = None
match_calculator = None
job_analyzer = None
cv_customizer = None
cover_letter_generator = None

def initialize_components():
    """Initialize all AI components."""
    global client, builder, match_calculator, job_analyzer, cv_customizer, cover_letter_generator
    
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise ValueError("DEEPSEEK_API_KEY not found in environment variables")
    
    client = DeepSeekClient(api_key=api_key)
    builder = DocumentBuilder()
    match_calculator = MatchCalculator()
    job_analyzer = JobAnalyzer(client)
    cv_customizer = CVCustomizer(client)
    cover_letter_generator = CoverLetterGenerator(client)

def load_profile(path: str = "data/master_profile.json") -> dict:
    """
    Load the master profile.

    Migration note:
    - Primary source is DB (Profile singleton).
    - If DB profile is empty but JSON file exists, import it once.
    """
    # 1. Try DB first
    if current_user.is_authenticated:
        profile_row = Profile.get_or_create_for_user(current_user.id)
    else:
        profile_row = Profile.get_singleton_profile()
    data = profile_row.to_dict()
    if data:
        return data

    # 2. Fallback: import from existing JSON file (one-time migration)
    try:
        with open(path, 'r', encoding='utf-8') as f:
            file_data = json.load(f)
            profile_row.update_from_dict(file_data)
            return file_data
    except FileNotFoundError:
        # If no file and no DB data, return empty profile structure
        return {}
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON in {path}")

def sanitize_filename(name: str) -> str:
    """Sanitize filename for Windows."""
    return re.sub(r'[<>:"/\\|?*]', '', name).strip().replace(' ', '_')

@app.route('/')
@login_required
def index():
    """Main page."""
    try:
        profile = load_profile()
        # Use redesigned template if available, fallback to original
        try:
            return render_template('index_redesigned.html', profile=profile)
        except:
            return render_template('index.html', profile=profile)
    except Exception as e:
        flash(f"Error loading profile: {str(e)}", "error")
        try:
            return render_template('index_redesigned.html', profile=None)
        except:
            return render_template('index.html', profile=None)

@app.route('/api/process', methods=['POST'])
@login_required
def process_job():
    """Process job description and generate CV/cover letter."""
    try:
        data = request.json
        job_description = data.get('job_description', '').strip()
        
        if not job_description or len(job_description) < 50:
            return jsonify({
                'success': False,
                'error': 'Job description is too short. Please provide at least 50 characters.'
            }), 400
        
        # Initialize components if not already done
        if client is None:
            initialize_components()
        
        # Load profile
        profile = load_profile()
        
        # Analyze job
        analysis = job_analyzer.analyze(job_description)
        role_title = analysis.get('role_info', {}).get('title', 'Unknown Role')
        company = analysis.get('role_info', {}).get('company', 'Unknown Company')
        
        # Calculate match score
        match_data = match_calculator.calculate_match_score(profile, analysis)
        
        # Customize CV
        customized_cv = cv_customizer.customize(profile, analysis)
        
        # Generate cover letter
        cover_letter_text = cover_letter_generator.generate(profile, analysis)
        
        # Generate documents
        os.makedirs("output", exist_ok=True)
        safe_title = sanitize_filename(role_title)
        safe_company = sanitize_filename(company)
        
        cv_filename = f"output/CV_{safe_company}_{safe_title}.docx"
        cl_filename = f"output/CL_{safe_company}_{safe_title}.docx"
        
        # Create documents (reuse builder but create new instances for each)
        cv_builder = DocumentBuilder()
        cv_builder.create_cv(customized_cv, cv_filename)
        
        cl_builder = DocumentBuilder()
        cl_builder.create_cover_letter(cover_letter_text, profile, cl_filename)
        
        return jsonify({
            'success': True,
            'role_title': role_title,
            'company': company,
            'match_score': match_data,
            'cv_file': cv_filename,
            'cover_letter_file': cl_filename,
            'analysis': analysis
        })
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': f'Configuration error: {str(e)}'
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Processing error: {str(e)}'
        }), 500

@app.route('/api/download/<path:filename>')
def download_file(filename):
    """Download generated files."""
    try:
        # Security: only allow files from output directory
        if not filename.startswith('output/'):
            return jsonify({'error': 'Invalid file path'}), 403
        
        file_path = filename
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
        
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/profile', methods=['GET'])
@login_required
def get_profile():
    """Get current profile."""
    try:
        profile = load_profile()
        return jsonify({'success': True, 'profile': profile})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/profile', methods=['POST'])
@login_required
def update_profile():
    """Update profile and persist to DB."""
    try:
        data = request.json
        profile_data = data.get('profile')

        if not profile_data:
            return jsonify({'success': False, 'error': 'No profile data provided'}), 400

        if not profile_data.get('personal_info', {}).get('name'):
            return jsonify({'success': False, 'error': 'Name is required'}), 400

        if current_user.is_authenticated:
            profile_row = Profile.get_or_create_for_user(current_user.id)
        else:
            profile_row = Profile.get_singleton_profile()
        profile_row.update_from_dict(profile_data)

        return jsonify({'success': True, 'message': 'Profile updated successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """User registration."""
    if request.method == 'POST':
        data = request.form
        email = data.get('email', '').strip().lower()
        password = data.get('password', '').strip()

        if not email or not password:
            flash('Email and password are required.', 'error')
            return render_template('auth_signup.html')

        if User.get_by_email(email):
            flash('Email is already registered. Please log in.', 'error')
            return render_template('auth_signup.html')

        password_hash = generate_password_hash(password)
        user = User.create(email=email, password_hash=password_hash)
        login_user(user)
        return redirect(url_for('index'))

    return render_template('auth_signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login."""
    if request.method == 'POST':
        data = request.form
        email = data.get('email', '').strip().lower()
        password = data.get('password', '').strip()

        user = User.get_by_email(email)
        if not user or not user.password_hash or not check_password_hash(user.password_hash, password):
            flash('Invalid email or password.', 'error')
            return render_template('auth_login.html')

        login_user(user)
        return redirect(url_for('index'))

    return render_template('auth_login.html')


@app.route('/logout')
@login_required
def logout():
    """Log out current user."""
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    # Initialize components on startup
    try:
        initialize_components()
        print("✅ All components initialized successfully")
    except Exception as e:
        print(f"⚠️  Warning: Could not initialize components: {e}")
        print("💡 Make sure DEEPSEEK_API_KEY is set in .env file")
    
    print("\n🚀 Starting Flask web server...")
    print("📱 Open your browser and go to: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop the server\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
