import pytest
import json

from messaging.handlers.messages_post import handler
from messaging.services import (email, sms, store)


def test_with_valid_params(mocker):
    # mocks
    message = {
        'recipient': 'recipient',
        'body': 'body',
        'email_address': 'email',
        'phone_number': 'number',
    }
    event = {'body': json.dumps(message)}
    context = {}

    mocker.patch('messaging.services.email.send')
    mocker.patch('messaging.services.sms.send')
    mocker.patch('messaging.services.store.create')
    store.create.return_value = message

    # call handler
    response = handler(event, context)

    # assertions
    store.create.assert_called_with(**message)
    email.send.assert_called_with(message['email_address'], message['body'])
    sms.send.assert_called_with(message['phone_number'], message['body'])

    assert response == {
        'statusCode': 200,
        'body': json.dumps(message)
    }
