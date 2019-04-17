import logging

from messaging.services import store
from messaging.helpers import (
    ApiError,
    parse_event,
    error_response,
    response,
    validate,
)


def handler(event, _):
    """
    Retrieves all messages sent to a particular recipient.
    """

    try:
        # parse query string
        data = parse_event(event, 'queryStringParameters')

        # validate request
        validate.params({'recipient': validate.is_non_empty_string}, data)

        # fetch messages from store
        messages = store.find_by_recipient(data.get('recipient'))

        # respond
        return response({'messages': messages})

    except ApiError as api_error:  # catch ApiErrors
        logging.error(api_error)
        return error_response(api_error)

    except Exception as exception:  # return default error response
        logging.error(exception)
        return error_response()
