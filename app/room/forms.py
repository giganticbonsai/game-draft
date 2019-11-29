from flask import current_app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, URL, NumberRange


class CreateForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    song = StringField('Song', validators=[DataRequired()], id='autocomplete')
    artist = StringField('Artist', validators=[DataRequired()], id='artist')
    duration = IntegerField('Time Limit (mins)', validators=[DataRequired()], description='Time per song')
    submit = SubmitField('Create Room')


class PlaylistForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    playlist = StringField('Spotify Playlist ID', validators=[DataRequired(), URL()])
    duration = IntegerField('Time Limit (mins)', validators=[DataRequired()])
    submit = SubmitField('Create Room')


class FreeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    number_of_songs = StringField('Number of Songs', validators=[DataRequired(),
                                                                 NumberRange(1, 10)])
    category = SelectField('Category', choices=[])
    duration = IntegerField('Time Limit (mins)', validators=[DataRequired()])
    submit = SubmitField('Create Room')
