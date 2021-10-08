from time import sleep, timezone
from background_task import background
from django.db.models.fields import CharField
from telethon.sync import TelegramClient
import os
from dotenv import load_dotenv
from django.conf import settings
import csv
import phonenumbers
import pandas as pd
from django.utils import timesince, timezone
from phonechecker.models import BotLogin, Check, PhoneNumber
from telethon import TelegramClient, errors, events
from telethon.tl.types import InputPhoneContact
from telethon import functions, types
load_dotenv()


API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")


@background()
def process_upload(batch_id, filename):
    """
    docstring
    """
    df = pd.read_csv(os.path.join(
        settings.MEDIA_ROOT, 'tmp', filename), dtype='str')

    for item in df['PhoneNumbers']:
        # if not item.startswith("+"):
        #     item = "+{}".format(item)
        print("Parsing Number: {}".format(item))
        parsed = phonenumbers.parse(item)
        if phonenumbers.is_valid_number(parsed):
            formatted = phonenumbers.format_number(
                parsed, phonenumbers.PhoneNumberFormat.E164)
            obj, created = PhoneNumber.objects.update_or_create(
                phone_number=formatted)
            Check.objects.update_or_create(
                batch=batch_id,
                phone_number=obj
            )


def get_names(client, phone_number):
    try:
        contact = InputPhoneContact(
            client_id=0, phone=phone_number, first_name="", last_name="")
        contacts = client(functions.contacts.ImportContactsRequest([contact]))
        user = contacts.to_dict()['users'][0]
        username = user['username']
        if not username:
            print(
                "*"*5 + f' Response detected, but no user name returned by the API for the number: {phone_number} ' + "*"*5)
            del_usr = client(
                functions.contacts.DeleteContactsRequest(id=[user['id']]))
            return
        else:
            del_usr = client(
                functions.contacts.DeleteContactsRequest(id=[username]))
            return username
    except IndexError as e:
        return f'ERROR: there was no response for the phone number: {phone_number}'
    except TypeError as e:
        return f"TypeError: {e}. --> The error might have occured due to the inability to delete the {phone_number} from the contact list."
    except:
        raise


def lookup_numbers(client, batch_uuid):
    '''
    The function uses the get_api_response function to first check if the user exists and if it does, then it returns the first user name and the last user name.
    '''
    result = {}
    numbers = Check.objects.filter(batch=batch_uuid).values_list(
        'phone_number__phone_number', flat=True)
    try:
        for phone in numbers:
            api_res = get_names(client, phone)
            result[phone] = api_res
        return result
    except:
        raise


@background(schedule=3)
def run_telethon(batch_uuid):
    """
    docstring
    """
    if os.path.isfile("{}.session".format(PHONE_NUMBER)):
        os.remove("{}.session".format(PHONE_NUMBER))

    client = TelegramClient(PHONE_NUMBER, API_ID, API_HASH)
    # print("Deleting session file...")
    # tg_session_file = "{}.session".format(PHONE_NUMBER)
    # if os.path.isfile(tg_session_file):
    #     try:
    #         os.remove(tg_session_file)
    #     except:
    #         print("Unable to delete Telethon session...")

    WAIT_SECONDS = 120
    print("Connecting to Telegram")
    client.connect()

    is_user_authorized = client.is_user_authorized()
    if not is_user_authorized:
        print("User is not authorized. Initiating Login...")
        print("Sending Auth request using phone: {}".format(PHONE_NUMBER))
        client.send_code_request(PHONE_NUMBER)
        login = BotLogin.objects.filter(batch=batch_uuid).first()
        loop_start = timezone.now()
        print("Waiting for code...")
        while not login and (timezone.now()-loop_start).total_seconds() < WAIT_SECONDS:
            login = BotLogin.objects.filter(batch=batch_uuid).first()
        if not login:
            print("No code received. Exiting..")
            return

        print("Code received!")
        client.sign_in(PHONE_NUMBER, login.code)

    print("Looking up numbers...")
    result = lookup_numbers(client, batch_uuid)
    print(result)

    for phone in result:
        r = result[phone]
        phone_number = PhoneNumber.objects.filter(phone_number=phone).first()
        if not phone_number:
            continue

        check = Check.objects.filter(
            batch=batch_uuid, phone_number=phone_number).first()
        if not check:
            continue

        if r is None:
            check.result = 2
        elif r.startswith('ERROR'):
            check.result = 3
        else:
            check.result = 1
        check.timestamp = timezone.now()
        check.save()
