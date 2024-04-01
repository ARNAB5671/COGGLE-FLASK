from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from datetime import datetime

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


class Meals(db.Model):
    __tablename__ = 'meals'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, unique=True, nullable=False)  # Make date field unique
    base_meal = db.Column(db.String(255))
    base_meal_price = db.Column(db.Float)
    extras = db.Column(db.String)  # Storing JSON strings for extras
    extras_prices = db.Column(db.String)  # Storing JSON strings for extras prices

    def __init__(self, date, base_meal, base_meal_price, extras, extras_prices):
        self.date = date
        self.base_meal = base_meal
        self.base_meal_price = base_meal_price
        self.extras = json.dumps(extras)
        self.extras_prices = json.dumps(extras_prices)

    def get_extras(self):
        return json.loads(self.extras)

    def get_extras_prices(self):
        return json.loads(self.extras_prices)

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

@app.route('/todaysMealOptions', methods=['POST'])
@login_required
def todaysMealOptions():
    print("HERE")
    request_data = request.get_json()
    today = request_data.get('date')

    # Convert date string to datetime object
    today = datetime.strptime(today, '%Y-%m-%d').date()
    meal = Meals.query.filter_by(date=today).first()
    if not meal:
        return jsonify({
            'sCode': 404,
            'success': False,
            'message': 'meals not available'
        })
    extrasList = list()
    for extra, price in zip(meal.get_extras(), meal.get_extras_prices()):
        extrasList.append({extra: price})
    print("HERE")
    return jsonify({
        'sCode': 200,
        'success': True,
        'message': 'here is the info of the meals',
        'mealOptions': {
            'baseMeal': meal.base_meal,
            'baseMealPrice': meal.base_meal_price,
            'extrasList': extrasList
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

@app.route('/setMeal', methods=['POST'])
@login_required
def setMeal():
    print("Hitting the API")
    data = request.get_json()

    dateString = data.get('date')
    dateObject = datetime.strptime(dateString, '%Y-%m-%d').date()
    baseMeal = data.get('base-meals')[0]
    baseMealPrice = data.get('base-meal-price')[0]
    extras = data.get('extras[]')
    extrasPrices = data.get('prices[]')

    existing_meal = Meals.query.filter_by(date=dateObject).first()
    if existing_meal:
        return jsonify({'sCode': 400, 'success':False, 'message': 'Meal already set for this date'}), 200
    
    meal = Meals(date=dateObject, base_meal=baseMeal, base_meal_price=baseMealPrice,
             extras=extras, extras_prices=extrasPrices)
    
    db.session.add(meal)
    db.session.commit()

    return jsonify({'sCode': 200, 'success':True}), 200

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8000)