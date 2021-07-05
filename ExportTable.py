class ExportTable:
    """
    This class creates a table that holds dataframe data for query results and exporting

    Attributes
    ----------
    table_name : str
        the table name of table in memory
    export_table : Pandas.DataFrame
        the dataframe of the SQL query result
    data_headers : list
        the header names in the export table
    data_values : list
        the data values in the export table
    """

    def __init__(self, query, export_table):
        """
        Parameters
        ----------    
        query : str
            the query to extract table name from
        export_table : Pandas.DataFrame
            the dataframe of the SQL query result
        data_headers : list
            the header names in the export table
        data_values : list
            the data values in the export table
        """
        self.table_name = self._get_table_name(query)
        self.export_table = export_table
        self.data_headers = self._load_data_headers(export_table)
        self.data_values = self._load_data_values(export_table)

    def _get_table_name(self, query_string):
        """
        Gets a table name from a query string

        Parameters
        ----------
        query_string : str
            the query string to get the table name from

        Returns
        -------
        str
            a table name
        """
        string_list = query_string.upper().split(' ')
        string_index = string_list.index('FROM')
        string_stripped = string_list[string_index+1].rstrip('\n')
        return string_stripped

    def _load_data_headers(self, dataframe):
        """
        Loads dataframe headers into a list

        Parameters
        ----------
        dataframe : Pandas.DataFrame
            the dataframe to convert into a header list

        Returns
        -------
        list
            a list of headers
        """
        if dataframe.empty:
            return ['No Results']
        return list(dataframe.columns)

    def _load_data_values(self, dataframe):
        """
        Loads dataframe data into a list

        Parameters
        ----------
        dataframe : Pandas.DataFrame
            the dataframe to convert into a data list

        Returns
        -------
        list
            a list of data
        """
        if dataframe.empty:
            return ['']
        return dataframe.values.tolist()
