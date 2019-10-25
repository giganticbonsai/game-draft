import random
import string

from flask import session, current_app
from flask_socketio import emit, join_room, leave_room

from app.game.manager import Manager
from .. import socketio, ROOMS


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


@socketio.on('create', namespace='/room')
def create(options):
    gm = Manager(options['song'])
    while gm.room_id in ROOMS:
        # Generate new id if id already in manager
        gm.generate_room_id()
    room_id = gm.room_id
    ROOMS[room_id] = gm
    join_room(room_id)
    emit('join_room', {'room': room_id})
