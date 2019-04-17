import os

import boto3

CHARSET = 'UTF-8'
REGION = os.environ.get('AWS_REGION')
SOURCE = os.environ.get('SOURCE_EMAIL_ADDRESS')
SUBJECT = "New message from Alex' serverless messaging API"


def send(email_address, body):
    client = boto3.client('ses', region_name=REGION)

    client.send_email(
        Source=SOURCE,
        Destination={
            'ToAddresses': [email_address]
        },
        Message={
            'Subject': {
                'Data': SUBJECT,
                'Charset': CHARSET
            },

            'Body': {
                'Text': {
                    'Data': body,
                    'Charset': CHARSET
                },
            }
        },
    )
