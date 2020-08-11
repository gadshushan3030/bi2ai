# define Python user-defined exceptions
class Error(Exception):
    """Base class for other exceptions"""
    pass


class AuthorizationError(Error):
    """Raised when the access is not authorized"""
    pass


class ValidationError(Error):
    """Raised when the input value does not pass a validation rule"""
    pass


class NotFoundError(Error):
    """Raised when a resource could not be found"""
    pass


class ResourceError(Error):
    """Raised when the api cannot interact with other internal resource"""
    pass
