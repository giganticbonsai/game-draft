from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class JoinForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    room = StringField('Room', validators=[DataRequired()])
    submit = SubmitField('Join Room')