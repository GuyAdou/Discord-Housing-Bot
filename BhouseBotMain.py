
from replit import db
import discord
import asyncio
from datetime import datetime, timedelta
import pytz

from GoogleSheetFetcher import GoogleSheetFetcher
from ResponseScheduler import ResponseScheduler
from SchedulerDatabaseManager import SchedulerDatabaseManager
from MessageManager import MessageManager

# Variables
housing_triggers =  ["looking for housing", "i'm looking for a roommate", "i'm looking for housing", "i'm Looking for an apartment","i'm looking for accommodation options", "reach out if you have any leads","let me know if you have any leads", "sublease available","landlord is looking for tenants", "am seeking accommodation","please dm if you have any leads", "take over our current","move in date in", "landlord is looking for tenants","i'm looking for a place", "i'm looking for an apartment", "i have a place","i'm looking for a place","furnished", "furnished","landlord","looking for accommodations", "looking for accommodation"
]
GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/16wlIAiNEazCtrcf3KMAiXi1DJLYP4oMzNjjG5HThzXc/edit?usp=sharing"
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = discord.Client(intents=intents)


db_manager = SchedulerDatabaseManager(db)
Gapi_url = GOOGLE_SHEET_URL
fetcher = GoogleSheetFetcher(Gapi_url)
fetcher.dataFetcher() 
user_data = fetcher.dataProcessing()
response_scheduler = ResponseScheduler(user_data=user_data, db_manager=db_manager, user_time_zone='America/New_York')
message_manager = MessageManager(client, response_scheduler, db_manager, housing_triggers)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    asyncio.create_task(daily_data_update(fetcher, response_scheduler))

@client.event
async def on_message(message):
    await message_manager.on_message(message)

async def daily_data_update(fetcher, scheduler):
    while True:
        fetcher.dataFetcher()
        new_data = fetcher.dataProcessing()
        if new_data:
            scheduler.update_with_new_data(new_data)
        await asyncio.sleep(86400)  # Sleep for 24 hours

if __name__ == "__main__":
    client.run(TOKEN)




