# task manager
## Instructions
### Clone the repository 

```
$ git clone https://github.com/alizameller/UI-UX.git
$ cd UI-UX
```
### Initialize a virtual environment

Windows:
```
$ python3 -m venv venv
$ venv\Scripts\activate.bat
```

Unix/MacOS:
```
$ python3 -m venv venv
$ source venv/bin/activate
```
### Install the dependencies
```
$ pip install -r requirements.txt
```
### Set up database
In your database client application (ex: psql), run the db.sql file

Example: Database called "postgres" in psql:
```
postgres=# \i '<path to db.sql file>'
```
### Connect to database from app.py
Modify the SQLALCHEMY_DATABASE_URI variable 
```
app.config['SQLALCHEMY_DATABASE_URI'] = <YOUR DATABSE CONNECTION URL HERE>
```
### Run the application
In the root directory of the cloned repo run:
```
$ flask run
```
The following message should display:
```
* Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```
Open the url: http://127.0.0.1:5000

https://github.com/alizameller/UI-UX/assets/49292194/f45f39b3-4e04-45c8-b1e2-54c89097332d




