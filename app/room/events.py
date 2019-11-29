from flask import session, current_app
from flask_socketio import emit, join_room, leave_room
from .. import socketio, ROOMS

import eventlet
eventlet.monkey_patch()

thread = {}

@socketio.on('joined', namespace='/room')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    name = session.get('name')
    join_room(room)
    gm = ROOMS[room]
    gm.add_player(name)
    emit('status', {'msg': name + ' has entered the room.'}, room=room)


@socketio.on('text', namespace='/room')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get('room')
    emit('message', {'msg': session.get('name') + ':' + message['msg']}, room=room)


@socketio.on('left', namespace='/room')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    name = session.get('name')
    leave_room(room)
    gm = ROOMS[room]
    gm.remove_player(name)
    emit('status', {'msg': session.get('name') + ' has left the room.'}, room=room)

@socketio.on('connect', namespace='/room')
def on_connect():
    global thread
    room = session.get('room')
    gm = ROOMS[room]
    if room not in thread:
        thread[room] = socketio.start_background_task(update_thread, current_app._get_current_object(), room, gm)


def update_thread(app, room, gm):
    with app.app_context():
        tick_time = app.config.get('ROOM_UPDATE_INTERVAL', 1)
        while True:
            socketio.emit('update', gm.jsonify(), namespace='/room', room=room)
            if gm.song.guessed:
                break
            if gm.playtime[1] == '00:00':
                # End Thread if times up
                gm.end_game()
                socketio.emit('status', {'msg': 'TIMES UP! GAME OVER!'}, namespace='/room', room=room)
            if gm.time_to_open_clue:
                nc = gm.song.open_next_clue()
                socketio.emit('status', {'msg': nc + ' Revealed!'}, namespace='/room', room=room)
            socketio.sleep(tick_time)


@socketio.on('guess', namespace='/room')
def make_guess(message):
    name = session.get('name')
    room = session.get('room')
    gm = ROOMS[room]
    guess = message['msg']
    gm.is_song(guess, name)
    if gm.song.guessed:
        emit('status', {'msg': name + ' GUESSED CORRECTLY!'}, room=room)
    else:
        emit('guess', {'msg': name + ' guessed "{}". '.format(guess) + 'INCORRECT!'}, room=room)

