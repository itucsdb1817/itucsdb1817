from flask_wtf import FlaskForm
from wtforms import Form, fields, validators

class BasePost(Form):
    title   = fields.TextField('Title', [validators.required(), validators.length(max=255, min=2)])
    tag     = fields.TextField('Tag', [validators.required(), validators.length(max=32)])

class TextPost(BasePost):
    content = fields.TextAreaField('Content', [validators.required()])