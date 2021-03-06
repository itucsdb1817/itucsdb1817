from flask_wtf import FlaskForm
from wtforms import TextField, TextAreaField, SubmitField, SelectField, validators

class BasePostForm(FlaskForm):
    title   = TextField('Title', [validators.required(), validators.length(min=2, max=255)])
    tag     = TextField('Tag', [validators.length(min=2, max=32), validators.Regexp('^\w+$')])

class TextPostForm(BasePostForm):
    content = TextAreaField('Content', [validators.required()])
    content_type = SelectField('Post Type', [validators.required()], choices=[('text', 'Text Post'), ('image', 'Image Post'), ('link', 'Link Post')])

class TextPostEditForm(FlaskForm):
    content = TextAreaField('Content', [validators.required()])

class DeleteForm(FlaskForm):
    yes = SubmitField('Action')
    no = SubmitField('Action')
