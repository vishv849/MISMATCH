from flask import jsonify, request, abort, send_from_directory
from app import app, db
from models import User, Interest, Match, Message, Report, ContactForm
from sqlalchemy.exc import IntegrityError
import os
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirect to login page if not authenticated

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#Example routes (adjust based on your actual needs):

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or 'SomaiyaEmail' not in data or 'password' not in data:  # Add password
        return jsonify({'message': 'Missing data'}), 400

    hashed_password = generate_password_hash(data['password'], method='sha256') # Hash the password

    new_user = User(SomaiyaEmail=data['SomaiyaEmail'], password=hashed_password) # Store the hashed password

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'Registered successfully'}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Email already exists'}), 400

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'SomaiyaEmail' not in data or 'password' not in data:
        return jsonify({'message': 'Missing data'}), 400

    user = User.query.filter_by(SomaiyaEmail=data['SomaiyaEmail']).first()

    if not user or not check_password_hash(user.password, data['password']): #Check hashed password
        return jsonify({'message': 'Invalid credentials'}), 401

    login_user(user)  # Log in the user
    return jsonify({'message': 'Logged in successfully'}), 200

@app.route('/api/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200

@app.route('/api/profile', methods=['GET', 'PUT'])
@login_required
def profile():
    if request.method == 'GET':
        user_data = {
            'UserID': current_user.UserID,
            'SomaiyaEmail': current_user.SomaiyaEmail,
            'InstagramHandle': current_user.InstagramHandle,
            'PhoneNumber': current_user.PhoneNumber,
            'Department': current_user.Department,
            'AboutYou': current_user.AboutYou,
            'ProfilePhoto': current_user.ProfilePhoto,
            'interests': [interest.InterestName for interest in current_user.interests]
        }
        return jsonify(user_data), 200

    elif request.method == 'PUT':
        data = request.get_json()
        if not data:
            return jsonify({'message': 'No data provided'}), 400

        current_user.InstagramHandle = data.get('InstagramHandle', current_user.InstagramHandle)
        current_user.PhoneNumber = data.get('PhoneNumber', current_user.PhoneNumber)
        current_user.Department = data.get('Department', current_user.Department)
        current_user.AboutYou = data.get('AboutYou', current_user.AboutYou)

        # Handle interests (example: replace existing interests with new ones)
        new_interests = data.get('interests', [])
        current_user.interests = []  # Clear existing interests
        for interest_name in new_interests:
            interest = Interest.query.filter_by(InterestName=interest_name).first()
            if interest:
                current_user.interests.append(interest)
            else:
                # Handle case where interest doesn't exist (create it or return an error)
                return jsonify({'message': f'Interest "{interest_name}" does not exist'}), 400

        db.session.commit()
        return jsonify({'message': 'Profile updated successfully'}), 200

@app.route('/api/upload_photo', methods=['POST'])
@login_required
def upload_photo():
    if 'photo' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    file = request.files['photo']

    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        current_user.ProfilePhoto = '/uploads/' + filename  # Save relative path
        db.session.commit()
        return jsonify({'message': 'Photo uploaded successfully', 'filepath': current_user.ProfilePhoto}), 200
    else:
        return jsonify({'message': 'Invalid file type'}), 400

@app.route('/uploads/<filename>')  # Route to serve uploaded photos
def serve_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/api/matches', methods=['GET'])
@login_required
def get_matches():
    # Retrieve matches for the current user, filter by status, etc.
    matches = Match.query.filter((Match.User1ID == current_user.UserID) | (Match.User2ID == current_user.UserID)).all()  # Adjust logic as needed
    match_list = []
    for match in matches:
        other_user_id = match.User2ID if match.User1ID == current_user.UserID else match.User1ID
        other_user = User.query.get(other_user_id)

        match_data = {
            'MatchID': match.MatchID,
            'OtherUserID': other_user.UserID,
            'OtherUserEmail': other_user.SomaiyaEmail,
            'Status': match.Status
        }
        match_list.append(match_data)
    return jsonify(match_list), 200

@app.route('/api/interests', methods=['GET'])
def get_interests():
    interests = Interest.query.all()
    interest_list = [{'InterestID': interest.InterestID, 'InterestName': interest.InterestName} for interest in interests]
    return jsonify(interest_list), 200

#More routes for managing messages, reports, etc.