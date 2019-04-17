import json

from .errors import ApiError


def response(data, status=200):
    return {
        'statusCode': status,
        'body': json.dumps(data),
    }


def error_response(api_error=ApiError()):
    return response({'error': api_error.__dict__}, api_error.status)
