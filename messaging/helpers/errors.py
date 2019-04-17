class ErrorCodes:
    DEFAULT = 'UNEXPECTED_ERROR'
    INVALID_PARAMETER = 'INVALID_PARAMETER'


class ApiError(Exception):
    def __init__(
            self,
            message='An unexpected or unspecified error occurred',
            status=500,
            code=ErrorCodes.DEFAULT,
    ):
        self.message = message
        self.status = status
        self.code = code
