import pytest
import json

from messaging.handlers.messages_get import handler
from messaging.services import store


def test_with_valid_params(mocker):
    # mocks
    recipient = 'recipient'
    message = 'message'
    event = {'queryStringParameters': {'recipient': recipient}}

    mocker.patch('messaging.services.store.find_by_recipient')
    store.find_by_recipient.return_value = [message]

    # call handler
    response = handler(event, None)

    # assertions
    store.find_by_recipient.assert_called_with(recipient)

    assert response == {
        'statusCode': 200,
        'body': json.dumps({
            'messages': [message]
        })
    }


def test_with_invalid_params(mocker):
    # call handler
    response = handler({}, None)

    # assertion
    assert response == {
        'statusCode': 400,
        'body': json.dumps({
            'error': {
                'message': "Missing or invalid 'recipient' parameter",
                'status': 400,
                'code': 'INVALID_PARAMETER'
            }
        })
    }
