#!/usr/bin/python3

import time
from datetime import datetime
import json
import os
from google.cloud import pubsub_v1

temp_threshold = 50.1
update_interval=5.0

topic_name=os.environ['TOPIC']
topic_name2=os.environ['TOPIC2']
project_id=os.environ['PROJECT_ID']

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_name)
topic_path2 = publisher.topic_path(project_id, topic_name2)
# /sys/class/thermal/thermal_zone0/temp

def get_cpu_temp():
    with open('/sys/class/thermal/thermal_zone0/temp') as f:
        return float(f.read())/1000

def notify_cpu_temp(temp):
    now = datetime.now()
    data={'timestamp': now.timestamp(), 'time': str(now), 'temperature': temp}
    res=publisher.publish(topic_path, json.dumps(data).encode('utf-8')) #encode rende il nostro sistema solido
    print(data, res.result())
    if temp >= temp_threshold:
        data={'timestamp': now.timestamp(), 'time': str(now)}
        res=publisher.publish(topic_path2, json.dumps(data).encode('utf-8'))


if __name__ == '__main__':
    while True:
        notify_cpu_temp(get_cpu_temp())
        time.sleep(update_interval)