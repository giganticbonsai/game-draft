from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class CreateForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    song = StringField('Song Title', validators=[DataRequired()])
    submit = SubmitField('Create Room')
