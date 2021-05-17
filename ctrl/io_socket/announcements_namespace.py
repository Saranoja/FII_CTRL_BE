import logging
from flask_socketio import Namespace, join_room, leave_room


class AnnouncementsNamespace(Namespace):
    def on_connect(self):
        logging.info('New connection')

    def on_join(self, data):
        room = data['room']
        logging.info("User joined room")
        join_room(room)

    def on_leave(self, data):
        room = data['room']
        logging.info("User left room")
        leave_room(room)

    def on_disconnect(self):
        logging.info('Client disconnected')
