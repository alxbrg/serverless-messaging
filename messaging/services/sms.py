import os

import boto3

REGION = os.environ.get('AWS_REGION')


def send(phone_number, body):
    client = boto3.client('sns', region_name=REGION)
    client.publish(PhoneNumber=phone_number, Message=body)
