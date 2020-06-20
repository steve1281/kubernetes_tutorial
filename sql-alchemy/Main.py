from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= "postgres://postgres:uU7PaQAoNI@127.0.0.1:5432/alchemy"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

# classes that represent tables 
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique = True)
    email = db.Column(db.String(80), unique = True)

    def __init(self, username, email):
        self.username = username
        self.email = email

