from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError

from app import ROOMS


class JoinForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    room = StringField('Room', validators=[DataRequired()])
    submit = SubmitField('Join Room')

    def validate_name(self, name):
        if self.room.data in ROOMS:
            if self.name.data in ROOMS[self.room.data].players:
                raise ValidationError('Please user another name.')

    def validate_room(self, room):
        if self.room.data not in ROOMS:
            raise ValidationError('Room does not exist.')
