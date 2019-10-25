from flask import render_template, session, url_for, redirect

from app import ROOMS
from app.game.manager import Manager
from app.room import bp
from app.room.forms import CreateForm


@bp.route('/room/<room>')
def room(room):
    name = session.get('name', '')
    session_room = session.get('room', '')
    if name == '' or session_room == '' or session_room != room or room not in ROOMS:
        return redirect(url_for('main.index'))
    return render_template('room/room.html', room=room, name=name, song=ROOMS[room].song, clues=ROOMS[room].clues)


@bp.route('/create', methods=['GET', 'POST'])
def create():
    form = CreateForm()
    if form.validate_on_submit():
        gm = Manager(form.song.data)
        while gm.room_id in ROOMS:
            # Generate new id if id already in manager
            gm.generate_room_id()
        room_id = gm.room_id
        ROOMS[room_id] = gm
        session['name'] = form.name.data
        session['room'] = room_id
        return redirect(url_for('room.room', room=session.get('room', '')))
    return render_template('room/create.html', form=form)
