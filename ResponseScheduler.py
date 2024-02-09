
from datetime import datetime, timedelta
import pytz

class ResponseScheduler:
    DEFAULT_TIME_WAITING_ON_USER_RESPONSE = 30
    DEFAULT_NEXT_FOLLOWUP_MESSAGE_DELTA = 20
    DEFAULT_CHECKING_ON_NEXT_MESSAGING_TIME_LOOP = 15

    def __init__(self, user_data,db_manager, user_time_zone='America/New_York',
                 time_waiting_on_user_response=DEFAULT_TIME_WAITING_ON_USER_RESPONSE,
                 next_followup_message_delta=DEFAULT_NEXT_FOLLOWUP_MESSAGE_DELTA,
                 checking_on_next_messaging_time_loop=DEFAULT_CHECKING_ON_NEXT_MESSAGING_TIME_LOOP):
        self.user_data = user_data
        self.db_manager = db_manager 
        self.user_time_zone = pytz.timezone(user_time_zone)
        self.time_waiting_on_user_response = time_waiting_on_user_response
        self.next_followup_message_delta = next_followup_message_delta
        self.checking_on_next_messaging_time_loop = checking_on_next_messaging_time_loop

    def update_with_new_data(self, new_data):
        for username, record_creation_date_str in new_data:
            self.calculate_and_store_next_send_time(username, record_creation_date_str)

    def calculate_and_store_next_send_time(self, username, reference_time):
        try:
            localized_reference_time = reference_time.astimezone(self.user_time_zone)

            # Calculate next send time based on the localized reference time
            next_send_time_for_user = localized_reference_time + timedelta(seconds=self.NEXT_FOLLOWUP_MESSAGE_DELTA)
            # Store the next send time in the database
            self.db_manager.store_next_send_time(username, next_send_time_for_user)
        except Exception as e:
            print(f"Error calculating or storing next send time for {username}: {e}")
    
    def check_for_user_to_contact(self):
        usersToContact = {}
        current_time_utc = datetime.utcnow().replace(tzinfo=pytz.utc)
        current_time = current_time_utc.astimezone(self.user_time_zone)
        
        for username, next_send_time in self.db_manager.get_next_send_times().items():
            if current_time >= next_send_time:
                usersToContact[username] = next_send_time
                self.db_manager.store_overdue_user(username)  # Store overdue user
        
        return usersToContact
    
    def mark_user_awaiting_response(self, username):
        response_due_time = datetime.utcnow() + timedelta(seconds=self.time_waiting_on_user_response)
        self.db_manager.store_user_awaiting_response(username, response_due_time)