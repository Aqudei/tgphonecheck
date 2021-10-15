from telethon import TelegramClient, errors, events
from telethon.tl.types import InputPhoneContact
from telethon import functions, types
from dotenv import load_dotenv
import asyncio
import requests
import argparse
import os
from getpass import getpass
import csv
from time import sleep
load_dotenv()

result = {}

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
PHONE_NUMBER = "+639672874486"
API_URL = os.getenv('API_URL')

client = TelegramClient(PHONE_NUMBER, API_ID, API_HASH)\



def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]


async def get_names(phone_number):
    try:
        contact = InputPhoneContact(
            client_id=0, phone=phone_number, first_name="", last_name="")
        contacts = await client(functions.contacts.ImportContactsRequest(contacts=[contact]))
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


async def user_validator(phones):
    '''
    The function uses the get_api_response function to first check if the user exists and if it does, then it returns the first user name and the last user name.
    '''
    processed = 0
    sleep_secs = 200
    for b in batch(phones, 100):
        try:
            for phone in b:
                api_res = await get_names(phone)
                result[phone] = api_res
                processed += 1
        except errors.FloodWaitError as e:
            sleep_secs = e.seconds
        except:
            raise
        finally:
            print("Total processed: {}".format(processed))

        sleep(sleep_secs)


async def main(args):
    await client.connect()
    user_authorized = await client.is_user_authorized()
    if not user_authorized:
        await client.send_code_request(PHONE_NUMBER)

        try:
            await client.sign_in(PHONE_NUMBER, input("Code: "))
            # await client.sign_in(PHONE_NUMBER, input(
            #     'Enter the code (sent on telegram): '))
        except errors.SessionPasswordNeededError:
            pw = input(
                'Two-Step Verification enabled. Please enter your account password: ')
            client.sign_in(password=pw)

    phones = []
    if args.csv:
        with open(args.csv, "rt") as infile:
            reader = csv.reader(infile)
            for idx, item in enumerate(reader):
                if idx == 0:
                    continue
                phones.append(item[0])

    await user_validator(phones)
    print(result)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Check to see if a phone number is a valid Telegram account')
    parser.add_argument("--csv")
    args = parser.parse_args()
    client.loop.run_until_complete(main(args))
