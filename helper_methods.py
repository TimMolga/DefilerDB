'''
This script file has helper methods to extract or process data to help function execution.
'''
import os
from datetime import datetime
import config


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


def drop_database():
    """
    Drops the database

    Returns
    -------
    str
        a message if the operation was completed successfully or failed
    """
    if os.path.exists(config.DB_NAME):
        os.remove(config.DB_NAME)
        return create_response_message(f'Dropped {config.DB_NAME}', True)
    else:
        return create_response_message(f'{config.DB_NAME} does not exist')


def get_date():
    """Gets the current date in YYYYMMDDHMS format.

    Returns
    -------
    str
        A datetime.
    """
    return datetime.now().strftime('%Y%m%d%H%M%S')
