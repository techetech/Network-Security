import sys
from networksecurity.logging import logger

class NetworkSecurityException(Exception):
    """Base class for all exceptions in the Network Security module."""
    def __init__(self,error_message,error_details:sys=None):
        super().__init__(error_message)
        self.error_message = error_message
        
        if error_details is not None:
            _,_,exc_tb = error_details.exc_info()
            if exc_tb is not None:
                self.line_number = exc_tb.tb_lineno
                self.file_name = exc_tb.tb_frame.f_code.co_filename
            else:
                self.line_number = "Unknown"
                self.file_name = "Unknown"
        else:
            self.line_number = "Unknown"
            self.file_name = "Unknown"

    def __str__(self):
        return f"Error occurred in script: [{self.file_name}] at line number: [{self.line_number}] with error message: [{self.error_message}]"
    

    
    