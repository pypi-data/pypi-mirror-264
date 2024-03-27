from typing import Any
from fastapi import FastAPI
from fastapi.responses import JSONResponse


class BaseError(Exception):
    """
    Base error class
    """

    def __init__(self, message: str, status_code: int, detail: Any | None = None):
        """
        Constructor

        :param message: Error message
        :param status_code: HTTP status code
        """
        self._message = message
        self._detail = detail
        self.status_code = status_code

    def message(self):
        """
        Get error message

        :return: Error message
        """
        return self._message

    def detail(self):
        """
        Get error detail

        :return: Error detail
        """
        return self._detail

    def __str__(self):
        """
        String representation

        :return: Error message
        """
        return self.message()


"""
List of HTTP Exceptions

400: Bad Request
401: Unauthorized
403: Forbidden
404: Not Found
405: Method Not Allowed
406: Not Acceptable
408: Request Timeout
409: Conflict
410: Gone
412: Precondition Failed
413: Payload Too Large
415: Unsupported Media Type
417: Expectation Failed
422: Unprocessable Entity
429: Too Many Requests
500: Internal Server Error
501: Not Implemented
502: Bad Gateway
503: Service Unavailable
504: Gateway Timeout
"""


class BadRequestError(BaseError):
    """
    Bad Request Error
    """

    def __init__(self, message: str, detail: str | None = None):
        """
        Constructor

        :param message: Error message
        """
        super().__init__(message, 400, detail=detail)


class UnauthorizedError(BaseError):
    """
    Unauthorized Error
    """

    def __init__(self, message: str = "Unauthorized", detail: Any | None = None):
        """
        Constructor

        :param message: Error message
        """
        super().__init__(message, 401, detail=detail)


class ForbiddenError(BaseError):
    """
    Forbidden Error
    """

    def __init__(self, message: str = "Forbidden", detail: Any | None = None):
        """
        Constructor

        :param message: Error message
        """
        super().__init__(message, 403, detail=detail)


class NotFoundError(BaseError):
    """
    Not Found Error
    """

    def __init__(self, message: str = "Not Found", detail: Any | None = None):
        """
        Constructor

        :param message: Error message
        """
        super().__init__(message, 404, detail=detail)


class MethodNotAllowedError(BaseError):
    """
    Method Not Allowed Error
    """

    def __init__(self, message: str = "Method Not Allowed", detail: Any | None = None):
        """
        Constructor

        :param message: Error message
        """
        super().__init__(message, 405, detail=detail)


class NotAcceptableError(BaseError):
    """
    Not Acceptable Error
    """

    def __init__(self, message: str = "Not Acceptable", detail: Any | None = None):
        """
        Constructor

        :param message: Error message
        """
        super().__init__(message, 406, detail=detail)


class RequestTimeoutError(BaseError):
    """
    Request Timeout Error
    """

    def __init__(self, message: str = "Request Timeout", detail: Any | None = None):
        """
        Constructor

        :param message: Error message
        """
        super().__init__(message, 408, detail=detail)


class ConflictError(BaseError):
    """
    Conflict Error
    """

    def __init__(self, message: str = "Conflict", detail: Any | None = None):
        """
        Constructor

        :param message: Error message
        """
        super().__init__(message, 409, detail=detail)


class GoneError(BaseError):
    """
    Gone Error
    """

    def __init__(self, message: str = "Gone", detail: Any | None = None):
        """
        Constructor

        :param message: Error message
        """
        super().__init__(message, 410, detail=detail)


class PreconditionFailedError(BaseError):
    """
    Precondition Failed Error
    """

    def __init__(self, message: str = "Precondition Failed", detail: Any | None = None):
        """
        Constructor

        :param message: Error message
        """
        super().__init__(message, 412, detail=detail)


class PayloadTooLargeError(BaseError):
    """
    Payload Too Large Error
    """

    def __init__(self, message: str = "Payload Too Large", detail: Any | None = None):
        """
        Constructor

        :param message: Error message
        """
        super().__init__(message, 413, detail=detail)


class UnsupportedMediaTypeError(BaseError):
    """
    Unsupported Media Type Error
    """

    def __init__(
        self, message: str = "Unsupported Media Type", detail: Any | None = None
    ):
        """
        Constructor

        :param message: Error message
        """
        super().__init__(message, 415, detail=detail)


class ExpectationFailedError(BaseError):
    """
    Expectation Failed Error
    """

    def __init__(self, message: str = "Expectation Failed", detail: Any | None = None):
        """
        Constructor

        :param message: Error message
        """
        super().__init__(message, 417, detail=detail)


class UnprocessableEntityError(BaseError):
    """
    Unprocessable Entity Error
    """

    def __init__(
        self, message: str = "Unprocessable Entity", detail: Any | None = None
    ):
        """
        Constructor

        :param message: Error message
        """
        super().__init__(message, 422, detail=detail)


class TooManyRequestsError(BaseError):
    """
    Too Many Requests Error
    """

    def __init__(self, message: str = "Too Many Requests", detail: Any | None = None):
        """
        Constructor

        :param message: Error message
        """
        super().__init__(message, 429, detail=detail)


class InternalServerError(BaseError):
    """
    Internal Server Error
    """

    def __init__(
        self, message: str = "Internal Server Error", detail: Any | None = None
    ):
        """
        Constructor

        :param message: Error message
        """
        super().__init__(message, 500, detail=detail)


class NotImplementedError(BaseError):
    """
    Not Implemented Error
    """

    def __init__(self, message: str = "Not Implemented", detail: Any | None = None):
        """
        Constructor

        :param message: Error message
        """
        super().__init__(message, 501, detail=detail)


class BadGatewayError(BaseError):
    """
    Bad Gateway Error
    """

    def __init__(self, message: str = "Bad Gateway", detail: Any | None = None):
        """
        Constructor

        :param message: Error message
        """
        super().__init__(message, 502, detail=detail)


class ServiceUnavailableError(BaseError):
    """
    Service Unavailable Error
    """

    def __init__(self, message: str = "Service Unavailable", detail: Any | None = None):
        """
        Constructor

        :param message: Error message
        """
        super().__init__(message, 503, detail=detail)


class GatewayTimeoutError(BaseError):
    """
    Gateway Timeout Error
    """

    def __init__(self, message: str = "Gateway Timeout", detail: Any | None = None):
        """
        Constructor

        :param message: Error message
        """
        super().__init__(message, 504, detail=detail)


def configure_error_handlers(app: FastAPI):
    """
    Configure errors handlers

    :param app: FastAPI instance
    """

    @app.exception_handler(BaseError)
    async def handle_base_error(request, exc):
        """
        Handle base error

        :param request: Request
        :param exc: Exception
        :return: Response
        """
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "status": exc.status_code,
                "title": exc.__class__.__name__.replace("Error", ""),
                "message": exc.message(),
                "detail": exc.detail(),
            },
        )
