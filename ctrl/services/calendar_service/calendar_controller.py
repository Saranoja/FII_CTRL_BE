from flask_restful import Resource
from flask import make_response, jsonify
from services.auth.token_config import token_required
from repository import MeetingsRepository, AssignmentsRepository, DiscussionGroupsMembersRepository, UsersRepository


class CalendarController(Resource):
    @staticmethod
    @token_required
    def get(current_user):
        user_groups = DiscussionGroupsMembersRepository.get_discussion_groups_for_user(current_user.id)

        current_user_calendar = []

        meetings = []
        assignments = []

        for group in user_groups:
            meetings.extend(MeetingsRepository.get_meetings_for_group(group.discussion_group_id))

        for meeting in meetings:
            recurrence_interval = meeting.recurrence_interval
            if recurrence_interval is not None:
                recurrence_interval = str(meeting.recurrence_interval).split(',')[0]
            event = {
                'type': 'meeting',
                'title': meeting.title,
                'timestamp': meeting.timestamp,
                'recurrent': meeting.recurrent,
                'recurrence_interval': recurrence_interval,
                'url': meeting.url,
            }
            current_user_calendar.append(event)

        for group in user_groups:
            assignments.extend(AssignmentsRepository.get_assignments_for_group(group.discussion_group_id))

        for assignment in assignments:
            event = {
                'type': 'assignment',
                'title': assignment.title,
                'timestamp': assignment.deadline,
                'recurrent': False,
                'recurrence_interval': None,
                'url': assignment.file_url
            }
            current_user_calendar.append(event)

        return make_response(jsonify(current_user_calendar), 200)
