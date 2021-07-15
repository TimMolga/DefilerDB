import config
import PySimpleGUI as sg
from helper_methods import drop_database
from Importer import Importer
from Exporter import Exporter
from DefilerDB import DefilerDB
from ImportTable import ImportTable
from ExportTable import ExportTable
from GUI import GUI


class GUIRunner():
    """
    This class controls GUI window view logic

    Methods
    -------
    run_gui()
        Runs the GUI application
    """

    def __init__(self):
        self._import_table = None
        self._export_table = None
        self._window = GUI().make_main_window(self._get_available_tables())
        self._window_import = None
        self._window_result = None
        self._window_export = None
        self._window_drop_table = None
        self._window_drop_database = None
        self._window_help = None
        self._window_import_active = False
        self._window_result_active = False
        self._window_export_active = False
        self._window_drop_table_active = False
        self._window_drop_database_active = False
        self._window_help_active = False

    def _create_insert_data(self, path, data):
        """
        Creates a table and inserts data into the database and shows the result in a popup

        Parameters
        ----------
        path : str
            the file path to get the file from
        sheet : str
            the sheet to data from if an XLSX file
        """
        if 'ERROR' in data:
            sg.popup_ok(data)
        else:
            # pass variables to ImportTable to process and format data for insertion
            import_table = ImportTable(path, data)
            db = DefilerDB()
            create_result = db.execute_create_table_query(
                import_table.table_name, import_table.column_names_types)
            if 'ERROR' in create_result:
                sg.popup_ok(f'{create_result}')
            else:
                insert_result = db.execute_insert_query(
                    import_table.table_name, import_table.column_names, import_table.import_table)
                sg.popup_ok(f'{create_result}\n\n{insert_result}')

    def _drop_database(self):
        """
        Drops the database and displays the result

        """
        drop_result = drop_database()
        sg.popup_ok(f'{drop_result}')

    def _drop_table(self, table_name):
        """
        Drops a table from the database and displays the result

        Parameters
        ----------
        table_name : str
            the name of the table to drop
        """
        db = DefilerDB()
        drop_result = db.execute_drop_table_query(table_name)
        sg.popup_ok(f'{drop_result}')

    def _export_data(self, path, data, table_name, file_type):
        """
        Exports data from the query results window and shows the result in a popup

        Parameters
        ----------
        path : str
            the folder path to save the file to
        data : str
            the dataframe to export
        table_name : str
            the table name to save as the file name
        file_type : str
            the type of file to export data to; default is CSV
        """
        if path:
            exp = Exporter()
            folder_path_reversed = path.replace('/', '\\')
            export_result = exp.export_file_data(
                folder_path_reversed, data, table_name, file_type)
            sg.popup_ok(f'{export_result}')

    def _get_available_tables(self):
        """
        Gets a list of tables in the database

        Returns
        -------
        list
            a list of tables in the database
        """
        db = DefilerDB()
        tables = db.execute_select_query(
            'SELECT name FROM sqlite_master WHERE type=\'table\'')
        if tables.empty:
            return ['None Available']
        return tables.values.tolist()

    def _import_data(self, path, sheet):
        """
        Formats and imports a CSV or XLSX file from a file path

        Parameters
        ----------
        path : str
            the file path to get the file from
        sheet : str
            the sheet to data from if an XLSX file
        """
        imp = Importer()
        if path:
            file_path_reversed = path.replace('/', '\\')
            if sheet:
                imported_file = imp.import_file_data(file_path_reversed, sheet)
                self._create_insert_data(file_path_reversed, imported_file)
            else:
                imported_file = imp.import_file_data(file_path_reversed)
                self._create_insert_data(file_path_reversed, imported_file)

    def run_gui(self):
        """
        Runs the GUI application
        """
        while True:
            event, values = self._window.read()
            if event == sg.WIN_CLOSED or event == 'Exit':
                break
            elif event == 'Import From File...' and not self._window_import_active:
                self._window_import = GUI().make_import_window()
                self._window_import_active = True
            elif event == 'Drop Table...' and not self._window_drop_table_active:
                self._window_drop_table = GUI().make_drop_table_window()
                self._window_drop_table_active = True
            elif event == 'Drop Database...' and not self._window_drop_database_active:
                self._window_drop_database = GUI().make_drop_database_window()
                self._window_drop_database_active = True
            elif event == 'Importing Data' and not self._window_help_active:
                self._window_help = GUI().make_help_window(config.IMPORT_INFO)
                self._window_help_active = True
            elif event == 'Exporting Data' and not self._window_help_active:
                self._window_help = GUI().make_help_window(config.EXPORT_INFO)
                self._window_help_active = True
            elif event == 'Querying Data' and not self._window_help_active:
                self._window_help = GUI().make_help_window(config.QUERY_INFO)
                self._window_help_active = True
            elif event == 'About' and not self._window_help_active:
                self._window_help = GUI().make_help_window(config.ABOUT_INFO)
                self._window_help_active = True
            elif event == '-EXECUTEQUERY-' and not self._window_result_active:
                query_result = self._select_data(values['-STRINGQUERY-'])
                if query_result is not None:
                    self._window_result = GUI().make_result_window(
                        self._export_table.data_headers, self._export_table.data_values)
                    self._window_result_active = True
            if self._window_import_active:
                while True:
                    window_import_event, window_import_values = self._window_import.read()
                    if window_import_event == sg.WIN_CLOSED or window_import_event == '-CLOSE-':
                        self._window_import_active = False
                        break
                    elif window_import_event == '-IMPORTFILEDB-':
                        self._import_data(
                            window_import_values['-FILEPATH-'], window_import_values['-SHEETNAME-'])
                        self._window.FindElement(
                            '-AVAILABLETABLES-').update(values=self._get_available_tables())
                        self._window_import.close()
                self._window_import.close()
            if self._window_result_active:
                while True:
                    window_result_event, window_result_values = self._window_result.read()
                    if window_result_event == sg.WIN_CLOSED or window_result_event == '-CLOSE-':
                        self._window_result_active = False
                        break
                    elif window_result_event == '-EXPORTFILE-' and not self._window_export_active:
                        self._window_export = GUI().make_export_window()
                        self._window_export_active = True
                        break
                self._window_result.close()
            if self._window_export_active:
                while True:
                    window_export_event, window_export_values = self._window_export.read()
                    if window_export_event == sg.WIN_CLOSED or window_export_event == '-CLOSE-':
                        self._window_export_active = False
                        break
                    elif window_export_event == '-EXPORTFILEDB-':
                        self._export_data(window_export_values['-FOLDERPATH-'], self._export_table.export_table,
                                          self._export_table.table_name, window_export_values['-FILETYPE-'])
                        self._window_export.close()
                self._window_export.close()
            if self._window_drop_table_active:
                while True:
                    window_drop_table_event, window_drop_table_values = self._window_drop_table.read()
                    if window_drop_table_event == sg.WIN_CLOSED or window_drop_table_event == '-CLOSE-':
                        self._window_drop_table_active = False
                        break
                    elif window_drop_table_event == '-DROPTABLE-':
                        self._drop_table(
                            window_drop_table_values['-TABLENAME-'])
                        self._window.FindElement(
                            '-AVAILABLETABLES-').update(values=self._get_available_tables())
                        self._window_drop_table.close()
                self._window_drop_table.close()
            if self._window_drop_database_active:
                while True:
                    window_drop_database_event, window_drop_database_values = self._window_drop_database.read()
                    if window_drop_database_event == sg.WIN_CLOSED or window_drop_database_event == '-CLOSE-':
                        self._window_drop_database_active = False
                        break
                    elif window_drop_database_event == '-DROPDATABASE-':
                        self._drop_database()
                        self._window_drop_database.close()
                self._window_drop_database.close()
                self._window.close()
            if self._window_help_active:
                while True:
                    window_help_event, window_help_values = self._window_help.read()
                    if window_help_event == sg.WIN_CLOSED or window_help_event == '-CLOSE-':
                        self._window_help_active = False
                        break
                self._window_help.close()

    def _select_data(self, query):
        """
        Performs a select query on the database

        Parameters
        ----------
        query : str
            the query to perform on the database

        Returns
        -------
        Pandas.DataFrame
            a dataframe of data
        """
        db = DefilerDB()
        query_result = db.execute_select_query(query)
        if 'ERROR' in query_result:
            sg.popup_ok(f'{query_result}')
            return
        else:
            self._export_table = ExportTable(query, query_result)
            return f'{query_result}'
