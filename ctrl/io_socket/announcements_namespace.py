import logging
from flask import request
from flask_socketio import Namespace, join_room, leave_room

sids = {}


class AnnouncementsNamespace(Namespace):
    def on_connect(self):
        logging.info('New connection')

    def on_join(self, data):
        global sids
        room = data['room']
        user = data['uid']
        logging.info("User joined room")
        sock_id = request.sid
        sids[user] = sock_id
        join_room(room)

    def on_leave(self, data):
        global sids
        room = data['room']
        logging.info("User left room")
        leave_room(room)

    def on_disconnect(self):
        logging.info('Client disconnected')
