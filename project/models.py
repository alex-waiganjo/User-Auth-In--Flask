from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50),nullable=False,unique=True)
    email = db.Column(db.String(50),nullable=False)
    password = db.Column(db.String(100),nullable=False,unique=True)

    def __repr__(self):
        return f"{self.name} , {self.email}" 