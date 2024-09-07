import nest_asyncio
nest_asyncio.apply()

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.sessions import StringSession
import asyncio

# Replace with your actual API credentials
api_id = yourAPI
api_hash = 'hash code'

# Specify your phone number
phone_number = '+133333333333'

# Create a new Telegram client session in-memory
session = StringSession()  # Create an empty StringSession
client = TelegramClient(session, api_id, api_hash)

async def main():
    try:
        # Start the Telegram client
        await client.start(phone=phone_number)
        
        print("Successfully connected to Telegram!")
        
        # Check if the user is authorized
        if await client.is_user_authorized():
            print("Authorization successful.")
        else:
            print("Authorization failed. You might need to check your phone number or API credentials.")
    
    except SessionPasswordNeededError:
        # This block handles two-factor authentication
        password = input("Two-step verification enabled. Please enter your password: ")
        await client.sign_in(password=password)
        print("Successfully authorized with two-factor authentication.")

    # Print the session string after logging in
    print("Your session string is:", client.session.save())

# Running the client and obtaining a session using async context
async def run():
    async with client:
        await main()

# Use the running event loop
asyncio.get_event_loop().run_until_complete(run())
