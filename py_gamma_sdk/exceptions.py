class GammaError(Exception):
    """Base exception for Gamma SDK."""
    pass

class GammaAPIError(GammaError):
    """Exception raised for API errors."""
    def __init__(self, message: str, status_code: int = None, response_text: str = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_text = response_text

class NotFoundError(GammaAPIError):
    """Raised when a resource is not found."""
    pass

class ValidationError(GammaError):
    """Raised when client-side validation fails."""
    pass
