from telethon import TelegramClient, errors, events
from telethon.tl.types import InputPhoneContact
from telethon import functions, types
from dotenv import load_dotenv
import asyncio
import requests
import argparse
import os
from getpass import getpass

load_dotenv()

result = {}

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
PHONE_NUMBER = os.getenv('PHONE_NUMBER')
API_URL = os.getenv('API_URL')

client = TelegramClient(PHONE_NUMBER, API_ID, API_HASH)


async def get_names(phone_number):
    try:
        contact = InputPhoneContact(
            client_id=0, phone=phone_number, first_name="", last_name="")
        contacts = await client(functions.contacts.ImportContactsRequest([contact]))
        user = contacts.to_dict()['users'][0]
        username = user['username']
        if not username:
            print(
                "*"*5 + f' Response detected, but no user name returned by the API for the number: {phone_number} ' + "*"*5)
            del_usr = await client(functions.contacts.DeleteContactsRequest(id=[user['id']]))
            return
        else:
            del_usr = await client(
                functions.contacts.DeleteContactsRequest(id=[username]))
            return username
    except IndexError as e:
        return f'ERROR: there was no response for the phone number: {phone_number}'
    except TypeError as e:
        return f"TypeError: {e}. --> The error might have occured due to the inability to delete the {phone_number} from the contact list."
    except:
        raise


async def user_validator():
    '''
    The function uses the get_api_response function to first check if the user exists and if it does, then it returns the first user name and the last user name.
    '''
    input_phones = input("Phone numbers: ")
    phones = input_phones.split()
    try:
        for phone in phones:
            api_res = await get_names(phone)
            result[phone] = api_res
    except:
        raise


async def main():
    await client.connect()
    user_authorized = await client.is_user_authorized()
    if not user_authorized:
        await client.send_code_request(PHONE_NUMBER)
        response = requests.get(
            API_URL + '/checker/botlogin/{}'.format(PHONE_NUMBER))
        response_json = response.json()
        while response_json == {} or response_json.get('code') == '':
            await asyncio.sleep(1)

        try:
            await client.sign_in(PHONE_NUMBER, response_json['code'])
            # await client.sign_in(PHONE_NUMBER, input(
            #     'Enter the code (sent on telegram): '))
        except errors.SessionPasswordNeededError:
            pw = getpass(
                'Two-Step Verification enabled. Please enter your account password: ')
            client.sign_in(password=pw)
    await user_validator()
    print(result)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Check to see if a phone number is a valid Telegram account')

    args = parser.parse_args()
    client.loop.run_until_complete(main())
