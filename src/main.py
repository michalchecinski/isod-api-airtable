#!/usr/local/bin/python

import datetime
from airtable import Airtable
import requests
import json


def get_config():
    with open('/app/secrets.json') as json_file:
        return json.load(json_file)


def get_airtable_connection(config):
    base_key = 'apphKOOtsf80PN0Cb'
    table_name = 'Notifications'
    airtable_key = config['airtable-key']
    airtable = Airtable(base_key, table_name, api_key=airtable_key)
    return airtable


def get_isod_api_news(config):
    isod_key = config['isod-key']
    isod_api = 'https://isod.ee.pw.edu.pl/isod-portal'\
               '/wapi?q=mynewsfull&username=checinsm'\
               f'&apikey={isod_key}&from=0&to=5'

    response = requests.get(isod_api)

    return response


def add_to_airtable(airtable, notification):
    airtable.insert({
        'hash': notification['hash'],
        'subject': notification['subject'],
        'content': notification['content'],
        'modifiedDate': notification['modifiedDate'],
        'modifiedBy': notification['modifiedBy'],
        'noAttachments': notification['noAttachments'],
        'type': notification['type']
    })


if __name__ == '__main__':
    print(f'Running script at: {datetime.datetime.utcnow()}')

    config = get_config()

    news = get_isod_api_news(config)
    notification_list = news.json()['items']

    airtable = get_airtable_connection(config)

    for notification in notification_list:
        if not notification['hash'].startswith('CLASSESANNOUN'):
            records = airtable.search('hash', notification['hash'])
            if len(records) == 0:
                add_to_airtable(airtable, notification)
