# JSONHelper
Flask app to help students understand how to manipulate JSON objects

URL: https://jsonhelpersinthushan.herokuapp.com/

## How it works:

User inputs link to a JSON file (ex: http://api.worldbank.org/v2/country/all/indicator/NY.GDP.MKTP.CD?format=json) and is returned with a formated output where end nodes can be 
clicked and the user will recieve Python code that can be used to reach that node via code.

Requirements:
certifi==2020.11.8
chardet==3.0.4
click==7.1.2
dominate==2.6.0
Flask==1.1.2
Flask-Bootstrap==3.3.7.1
Flask-SQLAlchemy==2.4.4
gunicorn==20.0.4
idna==2.10
itsdangerous==1.1.0
Jinja2==2.11.2
MarkupSafe==1.1.1
requests==2.25.0
SQLAlchemy==1.3.20
urllib3==1.26.2
visitor==0.1.3
Werkzeug==1.0.1
