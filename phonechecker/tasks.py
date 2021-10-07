from background_task import background
from telethon.sync import TelegramClient
import os
from dotenv import load_dotenv
from django.conf import settings
import csv
import phonenumbers

from phonechecker.models import Check, PhoneNumber
load_dotenv()


API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")
client = TelegramClient(PHONE_NUMBER, API_ID, API_HASH)


@background(schedule=5)
def process_upload(batch_id):
    """
    docstring
    """
    with open(os.path.join(settings.MEDIA_ROOT, 'tmp', 'numbers.csv'), 'rt') as infile:
        reader = csv.reader(infile)
        for item in reader:
            parsed = phonenumbers.parse(item[0])
            if phonenumbers.is_valid_number(parsed):
                formatted = phonenumbers.format_number(
                    parsed, phonenumbers.PhoneNumberFormat.E164)
                obj, created = PhoneNumber.objects.update_or_create(
                    phone_number=formatted)
                Check.objects.create(
                    batch=batch_id,
                    phone_number=obj
                )


@background(schedule=5)
def process_batch(batch_uuid):
    """
    docstring
    """

    client.connect()
    user_authorized = client.is_user_authorized()
    if not user_authorized:
        client.send_code_request(PHONE_NUMBER)
