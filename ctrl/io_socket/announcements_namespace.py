import logging
from flask_socketio import Namespace, emit, join_room, leave_room


class AnnouncementsNamespace(Namespace):
    @staticmethod
    def on_connect():
        logging.info('New connection')

    @staticmethod
    def on_join(data):
        room = data['room']
        join_room(room)

    @staticmethod
    def on_leave(data):
        room = data['room']
        leave_room(room)

    @staticmethod
    def on_disconnect():
        logging.info('Client disconnected')

    @staticmethod
    def on_my_event(data):
        emit('my_response', data)
