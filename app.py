from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

## ~~~~~~~~~~~~~~~~~~~~ Tables ~~~~~~~~~~~~~~~~~~~~
# Reflect the existing database tables
db.reflect()
# Access the users table
Users = db.Model.metadata.tables['users']

## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



@app.route("/")
def home():
    return render_template("home.html")

@app.route("/studentLogin")
def studentLoginPage():
    return render_template("studentLogin.html")

@app.route("/managerLogin")
def managerLoginPage():
    return render_template("managerLogin.html")

@app.route("/userRegistration")
def userRegistration():
    return render_template("userRegistration.html")

student = {
    'student1': 'password1',
    'student2': 'password2'
}

manager = {
    'manager1': 'password1',
    'manager2': 'password2'
}

@app.route('/register', methods=['POST'])
def register():
    print("\n\n\n\nINSIDE USER REGISTRATION\n\n\n\n")
    # Get the data from the request
    role = request.form.get('user-type')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm-password')

    # Check if passwords match
    if password != confirm_password:
        return jsonify({'sCode': 400, 'success': False, 'message': 'Passwords do not match'}), 400
    
    if Users.query.filter_by(email=email).first() and Users.query.filter_by(role=role).first():
        return jsonify({'message': f'{role} already exists'}), 400
    
    new_user = Users(email=email, role=role, password=generate_password_hash(password))
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User added successfully'}), 201


@app.route('/authenticateStudent', methods=['POST'])
def authenticateStudent():
    print("\n\n\n\nINSIDE AUTHENTICATE USER\n\n\n")
    # Get username and password from the request
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Check if username exists and password matches
    if username in student and student[username] == password:
        # Authentication successful
        return jsonify({
            'success': True, 
            'message': 'Authentication successful'
            }), 200
    else:
        # Authentication failed
        return jsonify({
            'success': False, 
            'message': 'Authentication failed. Invalid username or password'
            }), 401
    
@app.route('/authenticateManager', methods=['POST'])
def authenticateManager():
    print("\n\n\n\nINSIDE AUTHENTICATE USER\n\n\n")
    # Get username and password from the request
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Check if username exists and password matches
    if username in manager and manager[username] == password:
        # Authentication successful
        return jsonify({
            'success': True, 
            'message': 'Authentication successful'
            }), 200
    else:
        # Authentication failed
        return jsonify({
            'success': False, 
            'message': 'Authentication failed. Invalid username or password'
            }), 401


## ~~~~~~~~~~~~~~~~~ DASHBOARD ~~~~~~~~~~~~~~~~~
@app.route('/studentDashboard', methods=['GET'])
def studentDashboard():
    return render_template("studentDashboard.html")

@app.route('/managerDashboard', methods=['GET'])
def managerDashboard():
    return render_template("managerDashboard.html")

if __name__ == '__main__':
    app.run(debug=True)
