# MESS AUTOMATION SYSTEM

This is a simple mess automation that can have two types of users, `Student` and `Manager`. For each day, the `Manager` will fill up a form that will contain entries like `Base Meals`, `Price of Base Meals`, and a list of `Extras` and their corresponding `Prices`. The manager can add as many number of extras as he wants. Once added for a particular day, the Manager can't update the meal options.

Now, when the `Student` logs in, he/she will come to a different dashboard where he/she can select the `Extras` set by the `Manager` on that particular day. The student can choose any number of extras. 
Note that, when the student logs in before any `Manager` has filled the form, he/she will see "Not Avilable" in the Base Meal and Extras option.

This application has been made using `Flask` framework for backend and basic `html`, `css` and `javascript` for frontend, all in the same folder structure. 

SQL database has been used `sqlite3`



# Setup

### Create a Virtual Environment

1. `python3 -m venv venv`
2. Activate the virtual environment
`source venv/bin/activate`
3. Install the packages
`pip install -r requirements.txt`


### Creating tables in Database

Note: If there are existing contents in the db, first clear them. In `flask shell`, run this, 

```
from your_app import db
db.drop_all()
```

1. Open your terminal or command prompt and navigate to the directory where the app.py file is there.
2. Open the flask shell using the command `flask shell`.
3. Type this inside the flask shell
    ```
    >>> from app import db
    >>> db.create_all()
    ```
    This will reflect the table models that are there inside the app.py file

4. Exit - `exit()`

5. Now run the command `python app.py`

Open the url `http://127.0.0.1:8000/` and enjoy.

The post has deliberately been set to 8000, so that it can be opened by others connected to the same Wifi network as the server computer.
Get the ip address of the computer(mac) using `ipconfig getifaddr en0` and open in another device (connected to the same wifi network) `<ip-address>:8000/` for a better real-life experience. 


-- You can open the database.db file inside `instance/` using a good vscode extension. Like SQLite Viewer. To open the database.db with this, right click and select `Open With..`

# Using the App

Using the app includes Registering as `Manager` and `Student`. Manager can use the Dashboard to set the meals for a prticular day. Student can Choose the extras from the set meals for that particular day. 

## Home Page

`127.0.0.1:8000/`

<img src="resources/home.png?raw=true" alt="Home Page" width="400">

## User Registration

`http://127.0.0.1:8000/userRegistration`

Once Registered, it wil automatically go to the home screen within 2 seconds.

<img src="resources/userRegistration.png?raw=true" alt="User Registration" width="400">

## Manager and Student Login

Manager Login - `http://127.0.0.1:8000/managerLogin`
Student Login - `http://127.0.0.1:8000/studentLogin`

Once logged in, it wil automatically go to the dashboard screen within 2 seconds.

<img src="resources/managerLogin.png?raw=true" alt="Manager Page" width="400">
<img src="resources/studentLogin.png?raw=true" alt="Student Page" width="400">

## Manager Dashboard

`http://127.0.0.1:8000/managerDashboard`

<img src="resources/managerDashboard.png?raw=true" alt="Manager Dashboard" width="400">

## Student Dashboard

`http://127.0.0.1:8000/studentDashboard`

<img src="resources/studentDashboard.png?raw=true" alt="Student Dashboard" width="400">


## Logging Out

type the url `http://127.0.0.1:8000/logout` to logout.

Once logged out, it wil automatically go to the home screen within 2 seconds.
