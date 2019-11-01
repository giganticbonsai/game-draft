from flask import session, current_app
from flask_socketio import emit, join_room, leave_room

import eventlet
eventlet.monkey_patch()

from .. import socketio, ROOMS

thread = {}

@socketio.on('joined', namespace='/room')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    join_room(room)
    emit('status', {'msg': session.get('name') + ' has entered the room.'}, room=room)


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
    leave_room(room)
    emit('status', {'msg': session.get('name') + ' has left the room.'}, room=room)


@socketio.on('open_clue', namespace='/room')
def open_clue(data):
    room = session.get('room')
    gm = ROOMS[room]
    next_clue = gm.open_next_clue()
    status = 'No More Clues to Reveal!'
    if next_clue:
        status = next_clue + 'Revealed!'
    emit('status', {'msg': status}, room=room)


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
            if not gm.playtime:
                # End Thread if times up
                gm.end_game()
                socketio.emit('status', {'msg': 'GAME OVER!'}, namespace='/room', room=room)
                socketio.emit('update', {'time': 'TIMES UP!', 'guesses': gm.latest_guess}, namespace='/room', room=room)
                break
            if gm.time_to_open_clue:
                nc = gm.open_next_clue()
                socketio.emit('status', {'msg': nc + 'Revealed!'}, namespace='/room', room=room)
            socketio.emit('update', {'time': gm.playtime[1], 'guesses': gm.latest_guess, 'clues': gm.clues}, namespace='/room', room=room)
            socketio.sleep(tick_time)


@socketio.on('guess', namespace='/room')
def make_guess(message):
    name = session.get('name')
    room = session.get('room')
    gm = ROOMS[room]
    guess = message['msg']
    if gm.is_song(guess):
        gm.end_game()
        emit('status', {'msg': name + ' GUESSED CORRECTLY!'}, room=room)
    else:
        emit('guess', {'msg': name + ' guessed "{}". '.format(guess) + 'INCORRECT!'}, room=room)

