#!/usr/local/bin/python

import datetime
import os
from airtable import Airtable
import requests


def get_airtable_connection():
    base_key = 'apphKOOtsf80PN0Cb'
    table_name = 'Table 1'
    airtable_key = os.environ['AIRTABLE_API_KEY']
    airtable = Airtable(base_key, table_name, api_key=airtable_key)
    return airtable


def get_isod_api_news():
    isod_key = os.environ['ISOD_API_KEY']
    isod_api = f'https://isod.ee.pw.edu.pl/isod-portal/wapi?q=mynewsfull&username=checinsm&apikey={isod_key}&from=0&to=5'

    response = requests.get(isod_api)

    return response


def add_to_airtable(airtable, notification):
    airtable.insert({'hash': notification['hash'],
    'subject': notification['subject'],
    'content': notification['content'],
    'modifiedDate': notification['modifiedDate'],
    'modifiedBy': notification['modifiedBy'],
    'noAttachments': notification['noAttachments'],
    'type': notification['type']
    })


if __name__=='__main__':
    news = get_isod_api_news()
    notification_list = news.json()['items']

    airtable = get_airtable_connection()

    for notification in notification_list:
        if notification['type']==1002:
            continue

        records = airtable.search('hash', notification['hash'])
        if len(records) == 0:
            add_to_airtable(airtable, notification)
