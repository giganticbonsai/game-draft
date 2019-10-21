from flask import render_template, session, url_for, redirect

from app.room import bp


@bp.route('/room/<room>')
def room(room):
    name = session.get('name', '')
    session_room = session.get('room', '')
    if name == '' or session_room == '' or session_room != room:
        return redirect(url_for('main.index'))
    return render_template('room/room.html', room=room, name=name)
