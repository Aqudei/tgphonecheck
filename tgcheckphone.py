#!/usr/local/bin/python3
from telethon import TelegramClient, errors, events, sync
from telethon.tl.types import InputPhoneContact
from telethon import functions, types
from dotenv import load_dotenv
import argparse
import os
from getpass import getpass

load_dotenv()

result = {}

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
PHONE_NUMBER = '+639617703851'


def get_names(phone_number):
    try:
        contact = InputPhoneContact(
            client_id=0, phone=phone_number, first_name="", last_name="")
        contacts = client(functions.contacts.ImportContactsRequest([contact]))

        if len(contacts.to_dict()['users']) <= 0:
            return f'ERROR: there was no response for the phone number: {phone_number}'

        user = contacts.to_dict()['users'][0]
        username = user['username']
        if not username:
            print(
                "*"*5 + f' Response detected, but no user name returned by the API for the number: {phone_number} ' + "*"*5)

        try:
            del_usr = client(
                functions.contacts.DeleteContactsRequest(id=[user['id']]))
        except Exception as e:
            print("Error in deleting contact <{}> from TG".format(
                phone_number))

        return username
    except:
        raise


def user_validator(phones):
    '''
    The function uses the get_api_response function to first check if the user exists and if it does, then it returns the first user name and the last user name.
    '''
    try:
        for phone in phones:
            api_res = get_names(phone)
            result[phone] = api_res
    except:
        raise


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Check to see if a phone number is a valid Telegram account')
    parser.add_argument('--phones', nargs='+', type=str)

    args = parser.parse_args()

    client = TelegramClient(PHONE_NUMBER, API_ID, API_HASH)
    client.connect()
    if not client.is_user_authorized():
        client.send_code_request(PHONE_NUMBER)
        try:
            client.sign_in(PHONE_NUMBER, input(
                'Enter the code (sent on telegram): '))
        except errors.SessionPasswordNeededError:
            pw = getpass(
                'Two-Step Verification enabled. Please enter your account password: ')
            client.sign_in(password=pw)
    phones = []
    if args.phones:
        phones.extend(args.phones)

    user_validator(phones)
    print(result)
