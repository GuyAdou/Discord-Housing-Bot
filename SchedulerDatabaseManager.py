from datetime import datetime, timedelta
import pytz
from replit import db

class SchedulerDatabaseManager:
    def __init__(self, db):
        self.db = db  # The Replit database instance

    def store_next_send_time(self, username, next_send_time):
        self.db["next_send_time"][username] = next_send_time.strftime('%Y-%m-%dT%H:%M:%S.%f%z')

    def get_next_send_time(self, username):
        try:
            next_send_time_str = self.db["next_send_time"][username]
            next_send_time = datetime.strptime(next_send_time_str, '%Y-%m-%dT%H:%M:%S.%f%z')
            return next_send_time
        except KeyError:
            return None

    def store_overdue_user(self, username,timestamp):
        self.db["overdue_users"][username] = timestamp.strftime('%Y-%m-%dT%H:%M:%S.%f%z')

    def get_overdue_users(self):
        if "overdue_users" in self.db.keys():
            return {username: datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%S.%f%z') for username, timestamp_str in self.db["overdue_users"].items()}
        else:
            return {}
    def store_user_awaiting_response(self, username, response_due_time):
    
        self.db["awaiting_responses"][username] = response_due_time.strftime('%Y-%m-%dT%H:%M:%S.%f%z')

    def get_users_awaiting_response(self):
   
        if "awaiting_responses" not in self.db.keys():
            return {}
        return {username: datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S.%f%z') for username, time_str in self.db["awaiting_responses"].items()}
    
    def remove_user_awaiting_response(self, username):
        """
        Remove a user from the "awaiting_responses" list once they have responded.
        """
        if "awaiting_responses" in self.db.keys() and username in self.db["awaiting_responses"]:
            del self.db["awaiting_responses"][username]





