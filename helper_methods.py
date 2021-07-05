'''
This script file has helper methods to extract or process data to help function execution.
'''
import os
from datetime import datetime
 
def create_response_message(message, response_type=False):
    """Create a formatted success or error message.

    Parameters
    ----------
    message : str
        The message to return. 
    response_type : str
        The type of message; Default is False for error messages, True for success messages.
        
    Returns
    -------
    str
        A response message.
    """
    if response_type:
        return f'SUCCESS: {message}'
    else:
        return f'ERROR: {message}'

def drop_database(db_name):
        """
        Drops the database

        Parameters
        ----------
        table_name : str
            the database to drop
            
        Returns
        -------
        str
            a message if the operation was completed successfully or failed
        """
        if os.path.exists(db_name):
            os.remove(db_name)
            return create_response_message(f'Dropped {db_name}', True)
        else:
            return create_response_message(f'{db_name} does not exist')

def get_date():
    """Gets the current date in YYYYMMDDHMS format.
        
    Returns
    -------
    str
        A datetime.
    """
    return datetime.now().strftime('%Y%m%d%H%M%S')