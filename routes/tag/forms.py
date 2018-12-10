from flask_wtf import FlaskForm
from wtforms import TextField, TextAreaField, validators, StringField

class TagEditForm(FlaskForm):
    description = TextAreaField(
        'Description',
        [validators.DataRequired()]
    )
    rules = TextAreaField(
        'Description',
        [validators.DataRequired()]
    )

class TagCreationForm(TagEditForm):
    title = StringField(
        'Title',
        [validators.DataRequired(), validators.length(max=32)]
    )

# TODO: Create the form for managing moderators