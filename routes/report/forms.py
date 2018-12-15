from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,DateTimeField,TextAreaField
from wtforms.validators import DataRequired
from wtforms import validators
from wtforms.fields.html5 import EmailField
from datetime import datetime
import os
import sys

#Form for user to report a post/tag.
class ReportForm(FlaskForm):
    violated_rule = StringField('Which rule is violated?', validators=[DataRequired()])
    reason_description = TextAreaField('Please explain in detail.', validators=[DataRequired()])


