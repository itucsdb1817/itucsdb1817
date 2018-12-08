from flask_wtf import FlaskForm
from wtforms import Form, fields, validators

class BasePostForm(Form):
    title   = fields.TextField('Title', [validators.required(), validators.length(max=255, min=2)])
    tag     = fields.TextField('Tag', [validators.required(), validators.length(max=32)])

class TextPostForm(BasePostForm):
    content = fields.TextAreaField('Content', [validators.required()])