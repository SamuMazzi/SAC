#!/usr/bin/python3

import json
from google.cloud import pubsub_v1


publisher = pubsub_v1.PublisherClient()

def publ():
    publisher.publish('league1', json.dumps({
        'aa': 'csacs'
    }).encode('utf-8'))


if __name__ == '__main__':
    publ()