class AmazonCreatorsException(Exception):
    """Base exception for all Amazon Creators API errors."""
    pass

class AuthenticationError(AmazonCreatorsException):
    """Raised when there is an issue obtaining or refreshing the OAuth token."""
    pass

class RateLimitError(AmazonCreatorsException):
    """Raised when the API returns a 429 TooManyRequests."""
    pass

class InvalidRequestError(AmazonCreatorsException):
    """Raised when the API returns a 400 Bad Request."""
    pass

class APIError(AmazonCreatorsException):
    """Raised for general API errors (e.g. 500 Internal Server Error)."""
    def __init__(self, message: str, status_code: int = None, type: str = None, code: str = None):
        super().__init__(message)
        self.status_code = status_code
        self.type = type
        self.code = code
