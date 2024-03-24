"""
Functionality for issue management
"""

class CIException(Exception):
    """Custom exception class for Cortal Insight related errors."""
    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status_code = status_code
        super().__init__(f'Response [{status_code}] {message}')

class CIInvalidRequest(CIException, ValueError):
    """Custom exception for invalid requests."""
    pass

class CIExistingDatasetException(Exception):
    """Custom exception class for Cortal Insight related errors."""
    def __init__(self, message: "Datset Id not found"):
        self.message = message
        super().__init__(self.message)