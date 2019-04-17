import logging

from messaging.services import (email, sms, store)
from messaging.helpers import (
    ApiError,
    ErrorCodes,
    parse_event,
    error_response,
    response,
    validate,
)


def handler(event, _):
    """
    Sends a message (via email and/or SMS) to the specified recipient and stores it.
    """

    try:
        # parse request body
        data = parse_event(event, 'body')

        # validate request
        validate.params({
            'body': validate.is_non_empty_string,
            'recipient': validate.is_non_empty_string,
            'email_address': validate.is_nil_or_non_empty_string,
            'phone_number': validate.is_nil_or_non_empty_string,
        }, data)

        body = data.get('body')
        email_address = data.get('email_address')
        phone_number = data.get('phone_number')

        if email_address is None and phone_number is None:
            raise ApiError(
                "Specify either an 'email_address' or a 'phone_number'.",
                400,
                ErrorCodes.INVALID_PARAMETER,
            )

        # send message over specified medium(s)
        try:
            if email_address:
                email.send(email_address, body)
            if phone_number:
                sms.send(phone_number, body)
        except Exception:  # TODO: handle exceptions more granularly
            raise ApiError(
                "Something went wrong when attempting to send the message(s). Make sure that the " +
                "recipient's email address and phone number are valid.",
                500,
                ErrorCodes.MESSAGE_NOT_SENT,
            )

        # store message
        message = store.create(**data)

        return response(message)

    except ApiError as api_error:  # catch ApiErrors
        logging.error(api_error)
        return error_response(api_error)

    except Exception as exception:  # return default error response
        logging.error(exception)
        return error_response()
