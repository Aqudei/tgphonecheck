import asyncio
from telethon import TelegramClient, errors
from telethon.tl.types import InputPhoneContact
from telethon import functions, types
from phonechecker.models import Check, TelethonLogin
from dotenv import load_dotenv
from background_task import background
import argparse
import os
from getpass import getpass

load_dotenv()


API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
PHONE_NUMBER = os.getenv('PHONE_NUMBER')

client = TelegramClient(PHONE_NUMBER, API_ID, API_HASH)


async def get_names(phone_number):
    try:
        contact = InputPhoneContact(
            client_id=0, phone=phone_number, first_name="", last_name="")
        contacts = await client(functions.contacts.ImportContactsRequest([contact]))
        username = contacts.to_dict()['users'][0]['username']
        if not username:
            print(
                "*"*5 + f' Response detected, but no user name returned by the API for the number: {phone_number} ' + "*"*5)
            del_usr = await client(
                functions.contacts.DeleteContactsRequest(id=[username]))
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


async def user_validator(batch):
    '''
    The function uses the get_api_response function to first check if the user exists and if it does, then it returns the first user name and the last user name.
    '''
    result = {}
    phones = Check.objects.filter(batch=batch).values_list('phone_number')
    try:
        for phone in phones:
            api_res = await get_names(phone)
            result[phone] = api_res
        return result
    except:
        raise


async def process_numbers(batch):
    """
    docstring
    """

    MAX_RETRIES = 20
    retries = 0

    await client.connect()
    is_user_authorized = await client.is_user_authorized()
    if not is_user_authorized:
        await client.send_code_request(PHONE_NUMBER)
        login = TelethonLogin.objects.filter(done=False, code='').first()
        while not login:
            if retries > MAX_RETRIES:
                return
            login = TelethonLogin.objects.filter(done=False).first()
            retries += 1
            await asyncio.sleep(2)

        login.done = True
        login.save()

        try:
            await client.sign_in(PHONE_NUMBER, login.code)
        except errors.SessionPasswordNeededError:
            await client.sign_in(password=login.two_factor)
    result = await user_validator(batch=batch)
    print(result)


@background(schedule=60)
def process_numbers_task(batch=None):
    # lookup user by id and send them a message
    client.loop.run_until_complete(process_numbers(batch))
