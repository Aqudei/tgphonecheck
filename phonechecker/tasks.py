from background_task import background
from telethon.sync import TelegramClient
import os
from dotenv import load_dotenv

load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")
client = TelegramClient(PHONE_NUMBER, API_ID, API_HASH)


@background(schedule=5)
def process_batch(batch_uuid):
    """
    docstring
    """

    client.connect()
    user_authorized = client.is_user_authorized()
    if not user_authorized:
        client.send_code_request(PHONE_NUMBER)
