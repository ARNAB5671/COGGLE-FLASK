from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

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
    user_type = request.form.get('user-type')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm-password')

    # Check if passwords match
    if password != confirm_password:
        return jsonify({'sCode': 400, 'success': False, 'message': 'Passwords do not match'}), 400

    if user_type == 'manager':
        if email in manager:
            return jsonify({'sCode': 400, 'success': False, 'message': 'Manager already exists'}), 400
        else:
            manager[email] = password
            return jsonify({'sCode': 200, 'success': True, 'message': 'Manager registered successfully'}), 200
    elif user_type == 'student':
        if email in student:
            return jsonify({'sCode': 400, 'success': False, 'message': 'Student already exists'}), 400
        else:
            student[email] = password
            return jsonify({'sCode': 200, 'success': True, 'message': 'Student registered successfully'}), 200

    # Return success response
    return jsonify({'sCode': 400, 'success': False, 'message': 'Something Went Wrong, Contact Admin'}), 200


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
