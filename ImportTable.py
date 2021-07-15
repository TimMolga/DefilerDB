import re
from helper_methods import get_date


class ImportTable:
    """
    This class creates a table to help with importing data into the database

    Attributes
    ----------
    table_name : str
        the file name of the imported CSV or XLSX file
    column_names : str
        column names
    column_names_types : str
        column names and types in the dataframe
    import_table : Pandas.DataFrame
        the dataframe of the imported CSV or XLSX file data
    """

    def __init__(self, file_path, import_table):
        """
        Parameters
        ----------
        file_path : str
            the file path of the imported CSV or XLSX file
        import_table : pandas.DataFrame
            the dataframe of the imported CSV or XLSX file data
        """
        self.table_name = self._get_file_name(file_path)
        self.column_names = self._get_dataframe_column_names(import_table)
        self.column_names_types = self._get_column_names_types_string(
            import_table)
        self.import_table = import_table

    def _get_column_names_types_string(self, dataframe):
        """
        Get column names and types and convert them into a string for the create table query

        Parameters
        ----------
        dataframe : pandas.DataFrame
            the dataframe to get column names and data types from  

        Returns
        -------
        str
            column names and types in the dataframe
        """
        dictionary_types = self._get_dataframe_column_types(dataframe)
        return ','.join(['Id integer'] + list(
            {f'{key} {dictionary_types[key]}' for key in dictionary_types}))

    def _get_dataframe_column_names(self, dataframe):
        """
        Get the column names from a dataframe

        Parameters
        ----------
        dataframe : pandas.DataFrame
            the dataframe to get column names from

        Returns
        -------
        str
            column names
        """
        return ','.join(['Id'] + list(dataframe.columns))

    def _get_dataframe_column_types(self, dataframe):
        """
        Get the column data types from a dataframe and converts it to valid sqlite column types

        Parameters
        ----------
        dataframe : pandas.DataFrame
            the dataframe to get column data types from  

        Returns
        -------
        dict
            valid sqlite3 column data types
        """
        dictionary_types = dict(dataframe.dtypes)
        for key in dictionary_types:
            if (dictionary_types[key] == 'int64'):
                dictionary_types[key] = 'INTEGER'
            elif (dictionary_types[key] == 'float64'):
                dictionary_types[key] = 'REAL'
            else:
                dictionary_types[key] = 'TEXT'
        return dictionary_types

    def _get_file_name(self, path):
        """
        Get the file name from a file path

        Parameters
        ----------
        path : str
            the path of the file to get the name from

        Returns
        -------
        str
            a file name without file type or a default table name
        """
        path_string = ' '
        date = get_date()
        if '/' in path:
            path_string = path.split('/')[-1].split(".")[0]
        elif '\\' in path:
            path_string = path.split('\\')[-1].split(".")[0]
        return path_string if re.match("^[A-Za-z0-9_-]*$", path_string) or not path_string else f'DefaultTable{date}'
