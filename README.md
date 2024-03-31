## Create a Virtual Environment

1. python3 -m venv venv
2. Activate the virtual environment
source venv/bin/activate
3. Install the packages
pip install -r requirements.txt


## Creating tables in Database

1. Open your terminal or command prompt and navigate to the directory where you want to create the SQLite database file.
2. Run the SQLite command-line interface: sqlite3 database.db
3. Once you are in the SQLite prompt, you can define your tables using SQL commands.
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    role VARCHAR(50) NOT NULL
);
4. After defining your tables, you can exit the SQLite prompt by typing .exit

Since you have already created the table in your SQLite database without defining a corresponding SQLAlchemy model, you can still interact with the table using Flask-SQLAlchemy's reflection feature. Reflection allows SQLAlchemy to automatically create SQLAlchemy models based on the existing database tables.

