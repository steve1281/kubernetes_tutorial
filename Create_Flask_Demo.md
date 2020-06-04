# Python Flask - Learning

This is a review of the python flask. I will be using the online tutorial from freecodecamp
link: https://www.youtube.com/watch?v=Z1RJmh_OqeA

## Setup Notes
```
I am doing my work in my kubernetes development desktop which is a ubuntu 20.04 (Jun 4, 2020)
Creating a folder to work under:
$ mkdir ~/projects/kuber-demos/flask-demo

At this point, I am going to work from visual code.
$ cd ~/projects/kuber-demos/flask-demo
$ code .

Then open a terminal.

steve@kube:~/projects/kuber-demos/flask-demo$ python3 --version
Python 3.8.2

steve@kube:~/projects/kuber-demos/flask-demo$ pip3 install virtualenv
...
Successfully installed appdirs-1.4.4 distlib-0.3.0 filelock-3.0.12 virtualenv-20.0.21

steve@kube:~/projects/kuber-demos/flask-demo$ virtualenv env
created virtual environment CPython3.8.2.final.0-64 in 443ms
  creator CPython3Posix(dest=/home/steve/projects/kuber-demos/flask-demo/env, clear=False, global=False)
  seeder FromAppData(download=False, pip=latest, setuptools=latest, wheel=latest, via=copy, app_data_dir=/home/steve/.local/share/virtualenv/seed-app-data/v1.0.1)
  activators BashActivator,CShellActivator,FishActivator,PowerShellActivator,PythonActivator,XonshActivator

steve@kube:~/projects/kuber-demos/flask-demo$ source env/bin/activate
(env) steve@kube:~/projects/kuber-demos/flask-demo$


(env) steve@kube:~/projects/kuber-demos/flask-demo$ pip3 install flask flask-sqlalchemy
Collecting flask
...
Successfully installed Jinja2-2.11.2 MarkupSafe-1.1.1 SQLAlchemy-1.3.17 Werkzeug-1.0.1 click-7.1.2 flask-1.1.2 flask-sqlalchemy-2.4.3 itsdangerous-1.1.0
```

## Quick test application
```
$ touch app.py
Edit the file:

from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello World!"

if __name-- == "__main__":
    app.run(debug=True)

So we can run this:

(env) steve@kube:~/projects/kuber-demos/flask-demo$ python3 app.py
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 219-060-881

In another terminal, we can test it:

steve@kube:~/projects/kuber-demos/flask-demo$ curl localhost:5000
Hello World!

So that worked.
```

## Adding a static page:
```
Add two folders, templates and static
(env) steve@kube:~/projects/kuber-demos/flask-demo$ mkdir static
(env) steve@kube:~/projects/kuber-demos/flask-demo$ mkdir templates

Add render_template to the from flask import Flask, render_template
$ touch templates/index.html
Edit index.html
ooo. enter an !<tab> for fast boiler plate.
Add in a Hello World 2 
Should look like:

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    Hello World 2
</body>
</html>

rerun the python3 app.py 

and retest:

steve@kube:~/projects/kuber-demos/flask-demo$ curl localhost:5000
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    Hello World 2
</body>
```

## Adding a template
```
steve@kube:~/projects/kuber-demos/flask-demo$ touch templates/base.html
Note: flask uses jinja2 syntax.
Edit base.html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    {% block head %}{% endblock %}
</head>
<body>
    {% block body %} {% endblock %}
</body>
</html>

Edit index.html

{% extends 'base.html' %}

{% block head %}
<h1>Template Head </h1>
{% endblock %}

{%block body %}
<h1>Template Body </h1>
{% endblock %}

and re-run python3 app.py

$ curl localhost:5000

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
<h1>Template Head </h1>

</head>
<body>
    
<h1>Template Body </h1>

</body>

So that works.
```

## and static content
```

Create a new folder for css: $ mkdir static/css
$ touch static/css/main.css
Edit it

body {
    margin: 0;
    font-family: sans-serif;
}

And modify the base.html file:

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/main.css') }}"
    {% block head %}{% endblock %}
</head>
<body>
    {% block body %} {% endblock %}
</body>
</html>

Note the use of url_for() is necessary' you can't just put in static path here.

Next, open this in a browser and note the font change. 
http://127.0.0.1:5000/

```

## Setup database (SQL Alchemy is used here - basically a flat file)
```
In the activated virtualenv, run python3 and setup a database:

(env) steve@kube:~/projects/kuber-demos/flask-demo$ python3
Python 3.8.2 (default, Apr 27 2020, 15:53:34) 
[GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from app import db
/home/steve/projects/kuber-demos/flask-demo/env/lib/python3.8/site-packages/flask_sqlalchemy/__init__.py:833: FSADeprecationWarning: SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and will be disabled by default in the future.  Set it to True or False to suppress this warning.
  warnings.warn(FSADeprecationWarning(
>>> db.create_all()
>>> exit()


And add a model to the app.py
...
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

...
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)        

    def __repr__(self):
        return '<Task %r>' % self.id
...

```

## Add in controls, etc

```
This is a bit long winded; refer to the committed code.
Some notes:
jinja2 is used on the form.
for example:
        </tr>
        {% for task in tasks %}
            <tr>
                <td>{{ task.content }} </td>
                <td>{{ task.date_created }}</td>
                <td>
                    <a href="/delete/{{task.id}}">Delete</a><br>
                    <a href="/update/{{task.id}}">Update</a>
                </td>
            </tr>
        {% endfor %}
This works because we pass a tasks entity into the form:

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
...
    else: # GET
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template("index.html", tasks=tasks) 

```

## general comments about the online demo
```
Its not horrible; the information you need is there. 
However, he goes to fast in critical places - a common failure in online demos. 
The pause button is your friend.

Having said that, this 45 min demo took me > hour to do.
Probably worth mentioning - I have been building websites for 20 years. 
I have built flask (in 2.7) before. and have about 7 years of python programming.
Do not bother doing this demo unless you are comfortable with your python, css, and html skills.

And Heroku is wonderful, but out of scope for what I wanted, so I skipped it.

```





