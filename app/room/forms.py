from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class CreateForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    song = StringField('Song Title', validators=[DataRequired()])
    duration = IntegerField('Time Limit(mins)', validators=[DataRequired()])
    submit = SubmitField('Create Room')
