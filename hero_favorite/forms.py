from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms import validators
from wtforms.validators import DataRequired, Email

class UserLoginForm(FlaskForm):
    # email, password, submit_button
    email = StringField('Email', validators= [DataRequired(),Email()])
    password = PasswordField('Password', validators= [DataRequired()])
    submit_button = SubmitField()


class UserHeroAddForm(FlaskForm):
    # email, password, submit_button
    hero = StringField('Hero', validators= [DataRequired()])
    reason = StringField('Reason', validators= [DataRequired()])
    submit_button = SubmitField()