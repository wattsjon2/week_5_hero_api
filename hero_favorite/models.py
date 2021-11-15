from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime

# adding flask security for passwords
from werkzeug.security import generate_password_hash, check_password_hash

# import for secrets module (given by python)
import secrets 

from flask_login import LoginManager, UserMixin
from flask_marshmallow import Marshmallow


db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = '')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True)
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    hero = db.relationship('Hero', backref = "owner", lazy = True)

    def __init__(self,email, first_name ='',last_name = '', id = '', password = '', token = '', g_auth_verify = False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self,password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def set_token(self,length):
        return secrets.token_hex(length)

    def __repr__(self):
        return f'User {self.email} has been added to the Database'


class Hero(db.Model):
    id = db.Column(db.String, primary_key = True)
    fav_hero = db.Column(db.String(150))
    reason = db.Column(db.String(250), nullable = True)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, fav_hero, reason, user_token, id = ""):
        self.id = self.set_id()
        self.fav_hero = fav_hero
        self.reason = reason
        self.user_token = user_token

    def set_id(self):
        return secrets.token_urlsafe()

    def __repr__(self):
        return f'The following hero has been added: {self.fav_hero}'


# creation of API schema via the marshmallow object
class HeroSchema(ma.Schema):
    class Meta:
        fields = ['id','fav_hero','reason']


hero_schema = HeroSchema()
heroes_schema = HeroSchema(many = True)