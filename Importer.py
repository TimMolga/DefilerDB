import pandas as pd
from helper_methods import create_response_message


class Importer:
    """
    This class handles importing of CSV or XLSX files into dataframes

    Methods
    -------
    import_file_data(path, sheet=None)
        Gets the data from a CSV or Excel file and returns it in a dataframe
    """

    def import_file_data(self, path, sheet=None):
        """
        Gets the data from a CSV or Excel file and return it in a dataframe

        Parameters
        ----------
        path : str
            the path of the file to retrieve data from
        sheet : str
            the sheet to read from if reading from an Excel file

        Returns
        -------
        pandas.DataFrame, str
            a dataframe of data from a CSV or Excel file
            an error message if the import fails
        """
        try:
            if path.endswith('.csv'):
                df = pd.read_csv(path)
                validated_df = self._validate_imported_data_columns(df)
                validated_df.index = validated_df.index + 1
                return validated_df
            elif path.endswith('.xlsx'):
                if sheet:
                    df = pd.read_excel(path, sheet_name=sheet)
                    validated_df = self._validate_imported_data_columns(df)
                    validated_df.index = validated_df.index + 1
                    return validated_df
                else:
                    return create_response_message('Specify Sheet Name')
            else:
                return create_response_message('Invalid File Type')
        except:
            return create_response_message('Import Failed')

    def _validate_imported_data_columns(self, dataframe):
        """
        Check if dataframe has valid column names (no blank, null, or duplicate columns)

        Parameters
        ----------
        dataframe : pandas.DataFrame
            the dataframe to validate column names for

        Returns
        -------
        pandas.DataFrame, str
            a dataframe with validated column names or an error message
            an error message if the columns are invalid
        """
        df_columns = dataframe.columns.str.upper()
        for col in df_columns:
            if 'NULL' in col or '.' in col or ':' in col:
                return create_response_message('Invalid Column Names')
        return dataframe
