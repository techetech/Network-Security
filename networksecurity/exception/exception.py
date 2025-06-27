import sys
from networksecurity.logging import logger

class NetworkSecurityException(Exception):
    """Base class for all exceptions in the Network Security module."""
    def __init__(self,error_message,error_details:sys):
        super().__init__(error_message)
        self.error_message = error_message
        _,_,exc_tb = error_details.exc_info()

        self.line_number = exc_tb.tb_lineno
        self.file_name = exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return f"Error occurred in script: [{self.file_name}] at line number: [{self.line_number}] with error message: [{self.error_message}]"
    

    
    