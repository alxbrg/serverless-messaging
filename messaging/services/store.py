from datetime import datetime
import os
import uuid

from pynamodb.models import Model
from pynamodb.attributes import (UnicodeAttribute, UTCDateTimeAttribute)

HOST = os.environ.get('DB_CONNECTION_STRING')  # NOTE: only for local dev env
REGION = os.environ.get('AWS_REGION')
TABLE_NAME = os.environ.get('DB_TABLE_MESSAGES')


class Message(Model):
    class Meta:
        host = HOST
        region = REGION
        table_name = TABLE_NAME
        read_capacity_units = 1
        write_capacity_units = 1

    id = UnicodeAttribute(hash_key=True)
    recipient = UnicodeAttribute()
    email_address = UnicodeAttribute(null=True)
    phone_number = UnicodeAttribute(null=True)
    body = UnicodeAttribute()
    sent_at = UTCDateTimeAttribute()


def ensure_table_exists():
    """
    Creates the Message table if it doesn't exist.
    NOTE: this will only happen in local environment as the table is provisionned by Serverless
    """

    if not Message.exists():
        Message.create_table(wait=True)


def format_message(message):
    message = message.__dict__.get('attribute_values')
    message.update({'sent_at': message.get('sent_at').isoformat()})

    return message


def create(recipient, body, email_address=None, phone_number=None):
    ensure_table_exists()

    message = Message(
        id=str(uuid.uuid4()),
        recipient=recipient,
        email_address=email_address,
        phone_number=phone_number,
        body=body,
        sent_at=datetime.now(),
    )

    message.save()

    return format_message(message)


def find_by_recipient(recipient):
    ensure_table_exists()

    messages = Message.scan(Message.recipient == recipient)
    messages = map(format_message, messages)
    messages = list(messages)

    return messages
