import pandas as pd
from helper_methods import create_response_message, get_date


class Exporter():
    """
    This class handles exporting database tables into CSV or XLSX files

    Methods
    -------
    export_file_data(dataframe, path, table_name, file_type)
        Exports a dataframe to a CSV or XLSX file in a folder
    """

    def export_file_data(self, path, dataframe, table_name, file_type):
        """Exports a dataframe to a CSV or XLSX file in a folder

        Parameters
        ----------
        dataframe : pandas.DataFrame
            the dataframe to export to CSV or XLSX
        path : str
            the path of the folder to save the file to
        table_name : str
            the file name
        file_type : str
            the type of file to save the file as (CSV or XLSX)

        Returns
        -------
        str
            a message if the export was completed successfully or failed
        """
        file_path_name = f'{path}\\{table_name}{get_date()}.{file_type.lower()}'
        file_type_lower = file_type.lower()
        try:
            if path:
                if not dataframe.empty:
                    if file_type_lower == 'csv':
                        dataframe.to_csv(file_path_name, index=False)
                        return create_response_message(f'Export to CSV - Saved in {file_path_name}', True)
                    else:
                        dataframe.to_excel(file_path_name, index=False)
                        return create_response_message(f'Export to Excel - Saved in {file_path_name}', True)
                else:
                    return create_response_message('No data to export')
            else:
                return create_response_message('No path provided')
        except:
            return create_response_message('Exporting Data')
