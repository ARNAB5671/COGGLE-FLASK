## Create a Virtual Environment

1. `python3 -m venv venv`
2. Activate the virtual environment
`source venv/bin/activate`
3. Install the packages
`pip install -r requirements.txt`


## Creating tables in Database

1. Open your terminal or command prompt and navigate to the directory where the app.py file is there.
2. Open the flask shell using the command `flask shell`.
3. Type this inside the flask shell
    ```
    >>> from app import db
    >>> db.create_all()
    ```
    This will reflect the table models that are there inside the app.py file

4. Exit - `exit()`

5. Now run the command `flask run` or `python app.py`

Open the url `http://127.0.0.1:5000/` and enjoy.


-- You can open the database.db file inside `instance/` using a good vscode extension. Like SQLite Viewer. To open the database.db with this, right click and select `Open With..`

### Logging Out
type the url`http://127.0.0.1:5000/logout` to logout.
