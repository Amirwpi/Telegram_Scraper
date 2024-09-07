#*This code and documentation were written by [Amir Jamali](https://github.com/Amirwpi).*
#Main Scrapper

import asyncio
import datetime
import csv
import os
from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.sessions import StringSession
from telethon.errors import FloodWaitError
import nest_asyncio

nest_asyncio.apply()  # Apply the patch to allow nested event loops

api_id = '0000000000000'
api_hash = 'API_HASH'
group_title = 'groupname'
#Grouptitle for example https://t.me/groupname
limit_msg = 100

session_string = 'SESSION'
Repeat_number = 2000

datetime_before = datetime.datetime(2024, 9, 3, 22, 6, 3, tzinfo=datetime.timezone.utc)

# Directory to save media files
media_save_path = "downloaded_media"
os.makedirs(media_save_path, exist_ok=True)

async def get_messages(client, timestamp_before):
    all_messages = []
    try:
        group = await client.get_entity(group_title)
        posts = await client(GetHistoryRequest(
            peer=group,
            limit=limit_msg,
            offset_date=timestamp_before,
            offset_id=0,
            max_id=0,
            min_id=0,
            add_offset=0,
            hash=0
        ))

        for message in posts.messages:
            if message.from_id:
                try:
                    # Retrieve user information
                    user = await client.get_entity(message.from_id)
                    message_data = message.to_dict()  # Convert message to dictionary

                    # Check for media and download it
                    if message.media:
                        # Download the media and save it in the specified directory
                        file_path = await client.download_media(message, file=media_save_path)
                        print(f"Downloaded media: {file_path}")

                        # Add the file path to the message data
                        message_data['media_file_path'] = file_path
                    else:
                        # No media present for this message
                        message_data['media_file_path'] = None

                    # Add the modified message data to the list
                    all_messages.append(message_data)

                except FloodWaitError as e:
                    print(f'FloodWaitError: Waiting for {e.seconds} seconds')
                    await asyncio.sleep(e.seconds)  # Wait for the required time
                    user = await client.get_entity(message.from_id)
                    all_messages.append(message.to_dict())
    except Exception as e:
        print(f"An error occurred: {e}")
    return all_messages

async def main():
    global datetime_before  # Use global if you want to modify this outside its scope
    async with TelegramClient(StringSession(session_string), api_id, api_hash) as client:
        for jj in range(Repeat_number):
            Loop_number = 50
            timestamp_before = int(datetime_before.timestamp())

            File_name_part1 = datetime_before.strftime("%Y-%m-%d--%H-%M-%S")
            all_messages = []

            for i in range(Loop_number):
                try:
                    messages = await get_messages(client, timestamp_before)
                    all_messages.extend(messages)
                    if all_messages:
                        datetime_before = all_messages[-1]['date']
                        timestamp_before = int(datetime_before.timestamp()) - 1
                    print(f"Iteration: {i}, Total messages collected: {len(all_messages)}")

                    # Small delay between iterations to avoid hitting rate limits
                    await asyncio.sleep(1)

                except FloodWaitError as e:
                    print(f'FloodWaitError at iteration {i}: Waiting for {e.seconds} seconds')
                    await asyncio.sleep(e.seconds)  # Wait for the required time before retrying

            File_name_part2 = datetime_before.strftime("%Y-%m-%d--%H-%M-%S")
            File_name = f"{group_title}---From---{File_name_part2}---To---{File_name_part1}.csv"

            all_fieldnames = set()
            for msg in all_messages:
                all_fieldnames.update(msg.keys())

            # Save messages with media information to a CSV file
            with open(File_name, 'w', newline='', encoding='utf-8-sig') as f:  # Use 'utf-8-sig' for BOM
                writer = csv.DictWriter(f, fieldnames=list(all_fieldnames), restval='')
                writer.writeheader()
                writer.writerows(all_messages)

            print(f"Messages and media saved to {File_name}. Moving to the next repeat iteration...\n")

await main()  # Use 'await' directly to run the async function in Jupyter
