import PySimpleGUI as sg

class GUI():
    """This class creates GUI window layouts and responsible for the view
    
    Methods
    -------
    make_drop_window()
        Creates the drop table GUI window
    make_export_window()
        Creates the export GUI window
    make_help_window(help_choice)
        Creates the help GUI window from the help options
    make_import_window()
        Creates the import GUI window
    make_main_window(available_tables)
        Creates the main GUI window
    make_result_window(headers, data)
        Creates the query result GUI window
    """
    sg.theme('DarkGrey14')

    def make_drop_window(self):
        """
        Creates the drop table GUI window

        Returns
        -------
        PySimpleGUI.window
            a drop table window to display
        """
        layout = [
            [sg.Text('Drop a Table in the Database')],
            [sg.Text('Table Name:'), sg.Input(enable_events = True, key='-TABLENAME-')],
            [sg.Button('Drop', key='-DROPTABLE-'), sg.Button('Close', key='-CLOSE-')]
        ]
        return sg.Window('Drop Table', layout)

    def make_export_window(self):
        """
        Creates the export GUI window

        Returns
        -------
        PySimpleGUI.window
            an export window to display
        """
        file_dropdown = ['CSV', 'XLSX']
        layout = [
            [sg.Text('Export Data')],
            [sg.Text('Folder:'), sg.Input(enable_events = True, key='-FOLDERPATH-', readonly=True), sg.FolderBrowse()],
            [sg.Text('Type:  '), sg.Combo(file_dropdown, default_value=file_dropdown[0], key='-FILETYPE-', readonly=True, size=(43, 20))],
            [sg.Button('Export', key='-EXPORTFILEDB-'), sg.Button('Close', key='-CLOSE-')]
        ]
        return sg.Window('Export Data', layout)

    def make_help_window(self, help_choice):
        """
        Creates the help GUI window from the help options

        Parameters
        ----------
        help_choice : str
            the text to display on the help window

        Returns
        -------
        PySimpleGUI.window
            a help window to display
        """
        layout = [
            [sg.Text(help_choice)],
            [sg.Button('Close', key='-CLOSE-')]
        ]
        return sg.Window('Help', layout, element_justification='center')

    def make_import_window(self):
        """
        Creates the import GUI window

        Returns
        -------
        PySimpleGUI.window
            an import window to display
        """
        layout = [
            [sg.Text('Import Data From File (CSV or XLSX)')],
            [sg.Text('File:   '), sg.Input(enable_events = True, key='-FILEPATH-', readonly=True), sg.FileBrowse()],
            [sg.Text('Sheet:'), sg.Input(enable_events = True, key='-SHEETNAME-', size=(45, 20))],
            [sg.Button('Import', key='-IMPORTFILEDB-'), sg.Button('Close', key='-CLOSE-')]
        ]
        return sg.Window('Import Data', layout)

    def make_main_window(self, available_tables):
        """
        Creates the main GUI window

        Returns
        -------
        PySimpleGUI.window
            a main window to display
        """
        menu_def = [
            ['File', 'Exit'],      
            ['Import', 'Import From File...'],      
            ['Drop', 'Drop Table...'],
            ['Help', ['Getting Started...', ['Importing Data', 'Querying Data', 'Exporting Data'], 'About']], 
        ] 
        layout = [
            [sg.Menu(menu_def)],
            [sg.Text('DefilerDB', pad=(0,20), font=('arial', 20))],
            [sg.Table(key='-AVAILABLETABLES-',
                      values=available_tables,
                      headings=['Available Tables'],
                      def_col_width=20,
                      display_row_numbers=False,
                      auto_size_columns=False,
                      justification='center',
                      hide_vertical_scroll=True,
                      num_rows=5)],
            [sg.Multiline(default_text='Enter a query...', size=(200, 4), pad=(0,20), no_scrollbar=True, key='-STRINGQUERY-')],
            [sg.Button('Execute Query', key='-EXECUTEQUERY-')],
        ]
        return sg.Window('DefilerDB', layout,size=(600, 400), grab_anywhere=False, element_justification='center')

    def make_result_window(self, headers, data):
        """
        Creates the query result GUI window

        Parameters
        ----------
        headers : list
            the table column headers
        data : list
            the table values

        Returns
        -------
        PySimpleGUI.window
            an import window to display
        """
        layout = [
            [sg.Button('Export', key='-EXPORTFILE-')],
            [sg.Text('Query Results:', pad=(0,20))],
            [sg.Table(values=data,
                      headings=headers,
                      display_row_numbers=False,
                      auto_size_columns=False,
                      justification='center',
                      hide_vertical_scroll=True,
                      num_rows=15)],
            [sg.Button('Close', key='-CLOSE-', pad=(0,20))],
        ]
        return sg.Window('Query Results', layout,size=(800, 525), grab_anywhere=False, element_justification='center')




