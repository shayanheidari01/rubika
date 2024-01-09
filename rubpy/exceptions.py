import sys


class ClientError(Exception):
    pass

class StopHandler(ClientError):
    pass

class APIException(Exception):
    pass

class CancelledError(ClientError):
    pass


class RequestError(ClientError):
    def __init__(self, message, request=None):
        self.message = str(message)
        self.request = request


class UploadError(Exception):
    def __init__(self, status, status_det, dev_message: str=None):
        self.status = status
        self.status_det = status_det
        self.dev_message = dev_message

class CodeIsUsed(RequestError):
    pass


class TooRequests(RequestError):
    pass


class InvalidAuth(RequestError):
    pass


class ServerError(RequestError):
    pass


class UrlNotFound(RequestError):
    pass


class ErrorAction(RequestError):
    pass


class ErrorIgnore(RequestError):
    pass


class ErrorGeneric(RequestError):
    pass


class NoConnection(RequestError):
    pass


class InvalidInput(RequestError):
    pass


class Undeliverable(RequestError):
    pass


class NotRegistered(RequestError):
    pass


class CodeIsExpired(RequestError):
    pass


class InvalidMethod(RequestError):
    pass


class UsernameExist(RequestError):
    pass


class ErrorTryAgain(RequestError):
    pass


class ErrorMessageTry(RequestError):
    pass


class InternalProblem(RequestError):
    pass


class ErrorMessageIgn(RequestError):
    pass


class NotSupportedApiVersion(RequestError):
    pass


class ExcetionsHandler:
    def __init__(self, name) -> None:
        self.name = name

    def __getattr__(self, name):
        name = ''.join([chunk.title() for chunk in name.split('_')])
        return globals().get(name, ClientError)

    def __call__(self, name, *args, **kwargs):
        return getattr(self, name)

sys.modules[__name__] = ExcetionsHandler(__name__)