from flask import render_template, session, url_for, redirect, request
from flask.json import jsonify

from app import ROOMS, spotify
from app.game.manager import Manager
from app.room import bp
from app.room.forms import CreateForm


@bp.route('/room/<room>')
def room(room):
    name = session.get('name', '')
    session_room = session.get('room', '')
    if name == '' or session_room == '' or session_room != room or room not in ROOMS:
        return redirect(url_for('main.index'))
    gm = ROOMS[room]
    return render_template('room/room.html', title=room, name=name, song=gm.song.display_name)


@bp.route('/create', methods=['GET', 'POST'])
def create():
    form = CreateForm()
    if form.validate_on_submit():
        gm = Manager(form.song.data, form.artist.data, spotify_manager=spotify, duration=form.duration.data)
        while gm.room_id in ROOMS:
            # Generate new id if id already in manager
            gm.generate_room_id()
        room_id = gm.room_id
        ROOMS[room_id] = gm
        session['name'] = form.name.data
        session['room'] = room_id
        return redirect(url_for('room.room', room=session.get('room', '')))
    return render_template('room/create.html', form=form, title='Create Room')


@bp.route('/song_autocomplete', methods=['GET', 'POST'])
def song_autocomplete():
    search_term = request.args.get('term')
    if not search_term:
        return jsonify([])
    tracks = spotify.search_track(search_term)
    options = [{'value': t['name'],
                'label': t['name'] + ' by ' + t['artists'][0]['name'],
                'artist': t['artists'][0]['name']}
               for t in tracks]
    return jsonify(options)

@bp.route('/playlist_mode', methods=['GET', 'POST'])
def get_playlist():
    return
