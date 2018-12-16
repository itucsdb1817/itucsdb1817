from flask_wtf import FlaskForm
from wtforms import TextField, TextAreaField, validators, StringField

class TagEditForm(FlaskForm):
    description = TextAreaField(
        'Description',
        [validators.DataRequired()]
    )
    rules = TextAreaField(
        'Rules',
        [validators.DataRequired()]
    )

class TagCreationForm(TagEditForm):
    title = StringField(
        'Title',
        [validators.DataRequired(), validators.length(max=32)]
    )

class TagModForm(FlaskForm):
    user = TextField('Username', [validators.required()])

