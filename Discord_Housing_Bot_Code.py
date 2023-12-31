import json
import os
import random
import discord
import requests
from replit import db
import asyncio
from discord.ext import tasks
from datetime import datetime, timedelta
import pytz

#variables
housing_triggers = ["looking for housing", "i'm looking for a roommate", "i'm looking for housing", "i'm Looking for an apartment","i'm looking for accommodation options", "reach out if you have any leads","let me know if you have any leads", "sublease available","landlord is looking for tenants", "am seeking accommodation","please dm if you have any leads", "take over our current","move in date in", "landlord is looking for tenants","i'm looking for a place", "i'm looking for an apartment", "i have a place","i'm looking for a place","furnished", "furnished","landlord","looking for accommodations", "looking for accommodation"
]

GOOGLE_SHEET_URL = ""
Gapi = ""

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = discord.Client(intents=intents)


async def cache_all_members(guild):
  print(f"Starting to cache members for guild: {guild.name}")  # Debug line
  members = [member async for member in guild.fetch_members(limit=None)]
  print(f"Finished caching members for guild: {guild.name}")  # Debug line


# Function to fetch Discord usernames from Google Sheet
# Function to fetch Discord usernames for which the "update" value is "true" from Google Sheet via SheetDB API
def get_discord_usernames_for_update():
  try:
    # Fetch the data from the Google Sheet via SheetDB API
    response = requests.get(Gapi)
    
    response.raise_for_status()
    data = json.loads(response.text)
    # Filter usernames where "update" column value is "true"
    return [(entry["Discord username"], entry["Created date"]) for entry in data
            if entry["update"].lower() == "true"]
  except requests.RequestException as e:
    print(f"Failed to get usernames: {e}")
    return []


# Function to update "update" value in Google Sheet via SheetDB API
    def update_sheetdb_entry(username, update_value):
      try:
        url = f"{Gapi}/Discord%20username/{username}"
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        
        data = {"data": {"update": update_value}}

        # Make the PATCH request
        response = requests.patch(url, headers=headers, json=data)

        if response.status_code == 200:
          print("Successfully updated the SheetDB entry.")
        else:
          print(f"Failed to update SheetDB entry: {response.status_code}")
          print(response.text)

      except requests.RequestException as e:
        print(f"An error occurred: {e}")

interaction_wait_time_seconds = 172800 #two days

async def initiate_conversation(user):
    try:
        await user.send("Hi there!")
        await user.send(
            "Did you find a roommate or an apartment? Answer 'Yes' if you found what you were looking for and 'No' if you're still looking for a roommate or an apartment. Thanks!"
        )
        db["pending_responses"][str(user.id)] = (datetime.utcnow() + timedelta(seconds=interaction_wait_time_seconds)).strftime('%Y-%m-%dT%H:%M:%S.%f')
    except discord.errors.Forbidden:
        print(f"Couldn't send a message to {user.name}. They might have DMs disabled, blocked the bot, or the bot might lack permissions.")



# Dictionary to track the next time a user should receive a message
if "pending_responses" not in db.keys():
    db["pending_responses"] = {}
loop_interval_seconds = 86400
# Time delta for sending follow-up messages (1 week)
message_time_delta_seconds = 604800

@tasks.loop(seconds=loop_interval_seconds)
async def send_scheduled_messages():
  user_time_zone = pytz.timezone('America/New_York')
  usernames_timestamps = get_discord_usernames_for_update()

  for username, timestamp in usernames_timestamps:
    current_time_utc = datetime.utcnow().replace(tzinfo=pytz.utc)
    current_time = current_time_utc.astimezone(user_time_zone)
    try:
        time_record_created_naive = datetime.strptime(timestamp, "%m/%d/%Y %H:%M:%S")
        time_record_created = user_time_zone.localize(time_record_created_naive)
    except ValueError:
        print(f"Invalid timestamp format for username {username}: {timestamp}")
        continue

    if username not in db["next_send_time"]:
      next_send_time_for_user = time_record_created + timedelta(seconds=message_time_delta_seconds)
      db["next_send_time"][username] = next_send_time_for_user.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
    else:
      next_send_time_for_user = datetime.strptime(db["next_send_time"][username], '%Y-%m-%dT%H:%M:%S.%f%z')

    print(f"Next message to {username} is scheduled for: {next_send_time_for_user}")

    if current_time >= next_send_time_for_user:
      user = discord.utils.get(client.get_all_members(), name=username)
      if not user:
        print(f"User not found in guild: {username}")
        continue
      if user:
        await initiate_conversation(user)
        new_next_send_time = current_time + timedelta(seconds=message_time_delta_seconds + interaction_wait_time_seconds)
        db["next_send_time"][username] = new_next_send_time.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
        print(f"Next message to {username} is scheduled for: {new_next_send_time}")
      else:
        print(f"User not found in guild: {username}")


@tasks.loop(seconds=loop_interval_seconds)
async def check_for_overdue_responses():
    now = datetime.utcnow()
    if "pending_responses" not in db.keys():
        db["pending_responses"] = {}
    
    if "pending_responses" in db.keys():
        overdue_users = [int(user_id) for user_id, deadline_str in db["pending_responses"].items() if now > datetime.strptime(deadline_str, '%Y-%m-%dT%H:%M:%S.%f')]
        for user_id in overdue_users:
            user = await client.fetch_user(user_id)
            if user:
              await user.send(f"You did not answer on time. I'll touch base with you again in one week and get an update on your search. Good Luck!")
            del db["pending_responses"][str(user_id)]

@client.event
async def on_ready():
  for guild in client.guilds:
    await cache_all_members(guild)
  check_for_overdue_responses.start()
  send_scheduled_messages.start()



@client.event
async def on_message(message):
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

    if str(message.author.id) in db["pending_responses"]:
        deadline_str = db["pending_responses"][str(message.author.id)]
        deadline = datetime.strptime(deadline_str, '%Y-%m-%dT%H:%M:%S.%f')
        if datetime.utcnow() > deadline:
            await message.author.send(
                f"You did not answer on time. I'll touch base with you again in one week and get an update on your search. Good luck!"
            )
            del db["pending_responses"][str(message.author.id)]
            return

        if msg == 'yes':
            update_sheetdb_entry(message.author.name, "false")
            await message.author.send("Congratulations and good luck!")
            if str(message.author.id) in db["pending_responses"]:
                del db["pending_responses"][str(message.author.id)]
        elif msg == 'no':
            await message.author.send(
              f"Ok. I'll touch base with you again in one week and get an update on your search. Good luck!")
            if str(message.author.id) in db["pending_responses"]:
                del db["pending_responses"][str(message.author.id)]
        else:
            await message.author.send("Invalid input. Please enter 'Yes' or 'No'.")


for key in db.keys():
    print(f"{key}: {db[key]}")

try:
  token = os.environ["TOKEN"]
  client.run(token)
except KeyError:
  print("TOKEN environment variable not found.")
