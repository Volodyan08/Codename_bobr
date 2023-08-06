import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import uuid
from sqlalchemy import func
from dotenv import load_dotenv
from flask_migrate import Migrate


load_dotenv()


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

db = SQLAlchemy(app, session_options={'autoflush': False})
migrate = Migrate(app, db)


class User(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, firstname, lastname, email):
        self.id =  default=str(uuid.uuid4())
        self.firstname = firstname
        self.lastname = lastname
        self.email = email


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/users', methods=['POST'])
def get_users():
    users = User.query.all()
    result = [
        {
            'id': user.id,
            'firstname': user.firstname,
            'lastname': user.lastname,
            'email': user.email
        }
        for user in users
    ]
    return jsonify(result)


if __name__ == '__main__':
    app.run()
