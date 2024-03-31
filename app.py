from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt

import json

app = Flask(__name__)

bcrypt = Bcrypt(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # SQLite database
app.config['SECRET_KEY'] = 'thisisasecretkey'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()

db = SQLAlchemy(app)

loginManager = LoginManager()
loginManager.init_app(app)
loginManager.login_view = "/"

@loginManager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

## ~~~~~~~~~~~~~~~~~~~~ Tables ~~~~~~~~~~~~~~~~~~~~
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(50), nullable=False)

## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@app.route('/test')
def test():
    print(current_user.is_authenticated)
    if current_user.is_authenticated: 
        print(current_user.id)
        print(current_user.email)
        print(current_user.role)
        return json.dumps({
            'id': current_user.id,
            'email': current_user.email,
            'role': current_user.role
        })
    return "NOT LOGGED IN"


## Function to redirect the logged in users to their default home pages, else go to the defaultPage
def redirectToLoggedInHomePage(current_user, defaultPage="home.html"):
    if current_user.is_authenticated:
        if current_user.role=="manager":
            return redirect(url_for('managerDashboard'))
        return redirect(url_for('managerDashboard'))
    return render_template(defaultPage)

@app.route("/")
def home():
    return redirectToLoggedInHomePage(current_user, defaultPage="home.html")

@app.route("/studentLogin")
def studentLoginPage():
    return redirectToLoggedInHomePage(current_user, defaultPage="studentLogin.html")

@app.route("/managerLogin")
def managerLoginPage():
    return redirectToLoggedInHomePage(current_user, defaultPage="managerLogin.html")

@app.route("/userRegistration")
def userRegistration():
    return redirectToLoggedInHomePage(current_user, defaultPage="userRegistration.html")


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
    
    existingUserUsername = Users.query.filter_by(
            email=email
        ).first()
    if existingUserUsername:
        return jsonify({'sCode': 400, 'success': False, 'message': f'{role} already exists'}), 400
    
    new_user = Users(email=email, role=role, password_hash=bcrypt.generate_password_hash(password))
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'sCode': 200, 'success': True, 'message': 'User added successfully'}), 201

@app.route('/authenticateStudent', methods=['POST'])
def authenticateStudent():
    print("\n\n\n\nINSIDE AUTHENTICATE USER\n\n\n")
    # Get username and password from the request
    try:
        data = request.get_json()
        email = data.get('username')
        password = data.get('password')

        user = Users.query.filter_by(email=email).first()

        print(user.role)

        if user and user.role == 'student':
            if bcrypt.check_password_hash(user.password_hash, password):
                login_user(user)
                return jsonify({'success': True, 'message':f'Logged in as {email}'})
            else:
                return jsonify({'success': False, 'message':'Incorrect Password'})
        else:
            return jsonify({'success': False, 'message':'Username not found!'})
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    
@app.route('/authenticateManager', methods=['POST'])
def authenticateManager():
    print("\n\n\n\nINSIDE AUTHENTICATE USER\n\n\n")
    # Get username and password from the request
    try:
        data = request.get_json()
        email = data.get('username')
        password = data.get('password')

        user = Users.query.filter_by(email=email).first()

        print(user.role)

        if user and user.role == 'manager':
            if bcrypt.check_password_hash(user.password_hash, password):
                login_user(user)
                return jsonify({'success': True, 'message':f'Logged in as {email}'})
            else:
                return jsonify({'success': False, 'message':'Incorrect Password'})
        else:
            return jsonify({'success': False, 'message':'Username not found!'})
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500




## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ DASHBOARD ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
@app.route('/unauthorizedPage', methods=['GET'])
def unauthorizedPage():
    return render_template("unauthorizedPage.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('logout.html')



@app.route('/studentDashboard', methods=['GET'])
@login_required
def studentDashboard():
    if current_user.role!='student':
        return redirect(url_for('unauthorizedPage'))
    return render_template("studentDashboard.html")

@app.route('/todaysMealOptions', methods=['GET'])
@login_required
def todaysMealOptions():
    return jsonify({
        'sCode': 200,
        'success': True,
        'message': 'here is the info of the meals',
        'mealOptions': {
            'baseMeal': 'Riceeeeee, dal, paneer, raita, salad',
            'baseMealPrice': '15000',
            'extrasList': [{'Chickennnnnn': '100'}, {'Mutton': '150'}, {'Sweet': '50'}]
        }
    })

@app.route('/studentSelectMeals', methods=['POST'])
@login_required
def studentSelectMeals():
    data = request.get_json()
    baseMeal = data.get('baseMeal')
    baseMealAmount = data.get('baseMealAmount')
    extraMealPrice = data.get('extraMealPrice')
    totalAmount = data.get('totalAmount')
    date = data.get('date')

    print("values")
    print(baseMeal, baseMealAmount, extraMealPrice, totalAmount)
    print(date)

    return jsonify({'sCode': 200, 'success': True, 'message': 'User added successfully'}), 200



@app.route('/managerDashboard', methods=['GET'])
@login_required
def managerDashboard():
    if current_user.role!='manager':
        return redirect(url_for('unauthorizedPage'))
    return render_template("managerDashboard.html")

if __name__ == "__main__":
    app.run(debug=True)