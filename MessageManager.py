from datetime import datetime, timedelta
import pytz
import discord

class MessageManager:
    def __init__(self, client, scheduler, db_manager):
        self.client = client  # Discord client
        self.scheduler = scheduler  # ResponseScheduler instance
        self.db_manager = db_manager  # SchedulerDatabaseManager instance


    async def on_message(message,housing_triggers):
        if message.author == client.user:
         return

        msg = message.content.lower()

        if msg.startswith('$hello'):
            await message.channel.send('Hello!')

        if any(word in msg for word in housing_triggers):
            await message.channel.send("Hi there")
            await message.channel.send(
            f"Looking for a roommate or housing? Add your profile to the up-to-date housing Google sheet!{GOOGLE_SHEET_URL}"
            )


    async def initiate_conversation(self):
        # Retrieve overdue users
        usersToContact = self.scheduler.check_for_user_to_contact()
        for username in usersToContact:
            user = discord.utils.get(self.client.get_all_members(), name=username)
            if user:
                # Send the initial conversation message
                await user.send("Hi there!")
                await user.send("Did you find a roommate or an apartment? Answer 'Yes' or 'No'. Thanks!")
                current_time_str = datetime.now().strftime('%m/%d/%Y %H:%M:%S')
                self.scheduler.calculate_and_store_next_send_time(username, current_time_str)
            else:
                print(f"User not found: {username}")

    async def handle_user_response(self, message):
        user_id = str(message.author.id)
        username = message.author.name
        msg_content = message.content.lower()

    async def handle_user_response(self, message):
            username = message.author.name
            msg_content = message.content.lower()
            deadline_str = self.db_manager.get_pending_response(username)
            if deadline_str:
                deadline = datetime.strptime(deadline_str, '%Y-%m-%dT%H:%M:%S.%f')
                if datetime.utcnow() > deadline:
                    await message.author.send(
                        "You did not answer in time. I'll touch base with you again in one week and get an update on your search. Good luck!."
                    )
                else:
                    if msg_content == 'yes':
                        await self.sheet_fetcher.remove_user_entry(username)
                        await message.author.send("Thank you for your response. Best wishes!")
                    elif msg_content == 'no':
                        await message.author.send("We will check back with you later. Thank you!")
                    else:
                        await message.author.send("Invalid input. Please enter 'Yes' or 'No'.")

                # Regardless of the response, remove the user from awaiting responses
                self.db_manager.remove_user_awaiting_response(username)
                
                if msg_content != 'yes':  
                    self.scheduler.calculate_and_store_next_send_time(username, datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f'))

        


    

    
