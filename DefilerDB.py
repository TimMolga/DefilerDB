import config
import sqlite3 as sql
import pandas as pd
from helper_methods import create_response_message


class DefilerDB():
    """
    This class handles the database connection opening and closing, as well as querying and committing queries

    Methods
    -------
    execute_create_table_query(path, table_name, column_names_types)
        Executes a query that creates a table in the database
    execute_insert_query(self, table_name, column_names, dataframe)
        Executes a query that inserts data in the database
    execute_select_query(self, query_string)
        Executes a query that selects data from the database
    execute_drop_table_query(self, table_name)
        Executes a query that drops a table from the database
    """

    def __init__(self):
        self._db_connection = sql.connect(config.DB_NAME)
        self._db_cursor = self._db_connection.cursor()

    def _create_insert_cursor_query(self, table_name, column_names, row):
        """
        Creates a query string for inserting data into a table

        Parameters
        ----------
        table_name : str
            the table name to insert into; taken from the file name that was uploaded
        column_names : str
            column names for the insert statement
        row : pandas.IterTuple
            the row data to insert into the database

        Returns
        -------
        str
            a query string to insert data into a table
        """
        #list_row = list(row)
        #list_row_formatted = ','.join(repr(val) for val in list_row)
        list_row = ','.join(repr(val) for val in list(row))
        return f'INSERT INTO {table_name} ({column_names}) VALUES ({list_row})'

    def execute_create_table_query(self, table_name, column_names_types):
        """
        Executes a query that creates a table in the database

        Parameters
        ----------
        table_name : str
            the table name to create
        column_names_types : str
            the column names and their types to create in the table

        Returns
        -------
        str
            a message if the query was completed successfully or failed
        """
        try:
            self._db_connection.execute(
                f'CREATE TABLE {table_name} ({column_names_types})')
            return create_response_message(f'Created {table_name}', True)
        except sql.OperationalError as err:
            return create_response_message(err)

    def execute_drop_table_query(self, table_name):
        """
        Executes a query that drops a table from the database

        Parameters
        ----------
        table_name : str
            the table to drop in the database

        Returns
        -------
        str
            a message if the query was completed successfully or failed
        """
        try:
            if not table_name:
                return create_response_message('Table name missing')
            self._db_connection.execute(f'DROP TABLE {table_name}')
            return create_response_message(f'Dropped {table_name}', True)
        except sql.OperationalError as err:
            return create_response_message(err)

    def execute_insert_query(self, table_name, column_names, dataframe):
        """
        Executes a query that inserts data in the database

        Parameters
        ----------
        table_name : str
            the table name to insert data in
        column_names : str
            the column names to insert data into
        dataframe : pandas.DataFrame
            the dataframe to insert data from

        Returns
        -------
        str
            a message if the query was completed successfully or failed
        """
        try:
            if not dataframe.empty:
                for row in dataframe.itertuples():
                    self._db_cursor.execute(self._create_insert_cursor_query(
                        table_name, column_names, row))
                return create_response_message(f'Inserts into {table_name} complete', True)
            else:
                return create_response_message('No data to insert')
        except sql.OperationalError as err:
            return create_response_message(err)

    def execute_select_query(self, query_string):
        """
        Executes a query that selects data from a dataframe

        Parameters
        ----------
        query_string : str
            a select query for the database

        Returns
        -------
        pandas.DataFrame, str
            a dataframe with queried data
            an error message if the query is invalid
        """
        try:
            if 'SELECT' in query_string:
                dataframe = pd.read_sql_query(
                    query_string, self._db_connection)
                return dataframe
            else:
                return create_response_message('Only SELECT queries are allowed')
        except pd.io.sql.DatabaseError as err:
            return create_response_message(err)

    def __del__(self):
        self._db_connection.commit()
        self._db_connection.close()
