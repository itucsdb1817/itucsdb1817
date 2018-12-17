from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,DateTimeField, DateField,TextAreaField
from wtforms.validators import DataRequired
from wtforms import validators
from wtforms.fields.html5 import EmailField
from datetime import datetime
import os
import sys

#Form for user to log in.
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), validators.Regexp('^\w+$')])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


#Registration form for user to sign up.
#Restrictions may be implemented later.
class RegistrationForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    birth_date = DateField('Birth Date',validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), validators.Regexp('^\w+$')])
    email = EmailField('Email address', [validators.DataRequired(), validators.Email()])
    password = PasswordField('New Password',  [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField('Sign Up')


#Change password form
class PasswordForm(FlaskForm):

    old_password = PasswordField('Password')
    new_password = PasswordField('New Password',  [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField('Change')

#Report review form for admins
class ReviewForm(FlaskForm):
    action_taken = StringField('action_taken', validators=[DataRequired()])
    is_dismissed = BooleanField('is_dismissed',validators=[DataRequired()])
    submit = SubmitField('Submit')




