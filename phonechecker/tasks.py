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
from phonechecker.models import BotLogin, Check, MySql, PhoneNumber, Upload
from telethon import TelegramClient, errors, events
from telethon.tl.types import InputPhoneContact
from telethon import functions, types
import MySQLdb
from celery import shared_task
load_dotenv()


API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")

BATCH_SIZE = 40


def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]


# @background()
@shared_task
def mysql_import(batch_id):
    """
    docstring
    """
    db_info = MySql.objects.filter(batch_id=batch_id).first()
    if not db_info:
        return

    db = MySQLdb.connect(host=db_info.db_host, user=db_info.db_username,
                         passwd=db_info.db_password, db=db_info.db_name, port=db_info.db_port)
    cursor = db.cursor()
    cursor.execute("""SELECT %s FROM %s""" %
                   (db_info.db_column, db_info.db_table))
    items = cursor.fetchall()
    for item in items:
        print(item)

    cursor.close()


# @background()
@shared_task
def csv_import(batch_id):
    """
    docstring
    """
    upload = Upload.objects.filter(batch_id=batch_id).first()
    if not upload:
        return

    df = pd.read_csv(upload.file.path, dtype='str')

    for phone_number in df[upload.phone_column]:
        # if not item.startswith("+"):
        #     item = "+{}".format(item)
        obj, created = PhoneNumber.objects.update_or_create(
            phone_number=phone_number)
        Check.objects.update_or_create(
            batch=batch_id,
            phone_number=obj
        )


def get_names(client, phone_number):
    username = ''
    try:
        contact = InputPhoneContact(
            client_id=0, phone=phone_number, first_name="", last_name="")
        contacts = client(functions.contacts.ImportContactsRequest([contact]))
        user = contacts.to_dict()['users'][0]
        username = user['username']
        if not username:
            print(
                "*"*5 + f' Response detected, but no user name returned by the API for the number: {phone_number} ' + "*"*5)
            try:
                del_usr = client(
                    functions.contacts.DeleteContactsRequest(id=[user['id']]))
            except:
                pass

        else:
            try:
                del_usr = client(
                    functions.contacts.DeleteContactsRequest(id=[username]))
            except:
                pass

        return username
    except Exception as e:
        return f'ERROR! There was error in response for the phone number <{phone_number}>. {e}'


def validate_numbers(client, batch_uuid):
    '''
    The function uses the get_api_response function to first check if the user exists and if it does, then it returns the first user name and the last user name.
    '''
    result = {}
    numbers = Check.objects.filter(batch=batch_uuid).values_list(
        'phone_number__phone_number', flat=True)
    try:
        for b in batch(numbers, BATCH_SIZE):
            for phone in b:
                response = get_names(client, phone)
                result[phone] = response

                phone_number = PhoneNumber.objects.filter(
                    phone_number=phone).first()
                if not phone_number:
                    continue

                check = Check.objects.filter(
                    batch=batch_uuid, phone_number=phone_number).first()
                if not check:
                    continue

                if response is None:
                    check.result = 2
                elif response.startswith('ERROR'):
                    check.result = 3
                    check.debug = response
                else:
                    check.result = 1
                    check.username = response
                check.timestamp = timezone.now()
                check.save()
            sleep(300)
        return result
    except:
        raise


# @background(schedule=3)
@shared_task
def run_telethon(batch_uuid):
    """
    docstring
    """
    WAIT_SECONDS = 120

    loop_start = timezone.now()
    login = BotLogin.objects.filter(batch=batch_uuid).first()
    while not login and (timezone.now()-loop_start).total_seconds() < WAIT_SECONDS:
        login = BotLogin.objects.filter(batch=batch_uuid).first()
    if not login:
        return

    client = TelegramClient(login.phone_number, API_ID, API_HASH)

    print("Connecting to Telegram")
    client.connect()

    is_user_authorized = client.is_user_authorized()
    if not is_user_authorized:
        print("User is not authorized. Initiating Login...")
        print("Sending Auth request using phone: {}".format(login.phone_number))
        client.send_code_request(login.phone_number)
        login = BotLogin.objects.filter(batch=batch_uuid).first()
        loop_start = timezone.now()
        print("Waiting for code...")
        while (login.code == '' or login.code is None) and (timezone.now()-loop_start).total_seconds() < WAIT_SECONDS:
            login = BotLogin.objects.filter(batch=batch_uuid).first()

        if login.code == '' or login.code is None:
            print("No code received. Exiting..")
            return

        print("Code received!")
        client.sign_in(login.phone_number, login.code)

    print("Looking up numbers...")
    result = validate_numbers(client, batch_uuid)
    print(result)

    # for phone in result:
    #     r = result[phone]
    #     phone_number = PhoneNumber.objects.filter(phone_number=phone).first()
    #     if not phone_number:
    #         continue

    #     check = Check.objects.filter(
    #         batch=batch_uuid, phone_number=phone_number).first()
    #     if not check:
    #         continue

    #     if r is None:
    #         check.result = 2
    #     elif r.startswith('ERROR'):
    #         check.result = 3
    #     else:
    #         check.result = 1
    #     check.timestamp = timezone.now()
    #     check.save()
