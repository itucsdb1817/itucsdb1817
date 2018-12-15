from flask_wtf import FlaskForm
from wtforms import TextField, TextAreaField, SubmitField, validators

class BasePostForm(FlaskForm):
    title   = TextField('Title', [validators.required(), validators.length(max=255, min=2)])
    tag     = TextField('Tag', [validators.length(max=32)])

class TextPostForm(BasePostForm):
    content = TextAreaField('Content', [validators.required()])

class TextPostEditForm(FlaskForm):
    content = TextAreaField('Content', [validators.required()])

class DeleteForm(FlaskForm):
    yes = SubmitField('Action')
    no = SubmitField('Action')
