import unittest
import os
import sys
from Importer import Importer


class ImporterTestCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cwd = os.getcwd() + '\\tests'
        cls.path1 = cls.cwd + '\\TestTable1.csv'
        cls.path2 = cls.cwd + '\\TestTable2.xlsx'
        cls.path3 = cls.cwd + '\\TestTable3.xlsx'
        cls.path4 = cls.cwd + '\\TestTable4.xlsx'
        cls.path5 = cls.cwd + '\\FakeTextTable.txt'
        cls.path6 = cls.cwd + '\\FakeTable.csv'
        cls.sheet1 = 'Sheet1'
        cls.sheet2 = 'Sheet2'
        cls.sheet3 = 'Sheet3'
        cls.sheet4 = 'DoesNotExist'
        cls.df_columns = {'Name', 'Age', 'Payment', 'Email'}
        cls.df_values1 = ['John Smith', 21, 1111.33, '']
        cls.df_values2 = ['Gorge', 25, 123.55, '']
        cls.df_values3 = ['Fan', 26, 1437.50, '']
        cls.df_values4 = ['Ben', 25, 866.77, 'af@gmail.com']
        cls.df_values5 = ['George Lucas', 25, 866.77, 'af@gmail.com']
        cls.imp = Importer()

    @classmethod
    def check_if_value_exists(self, dataframe, set_list_values):
        """
        Checks if a value exists in a dataframe from a set or list of values.

        Parameters
        ----------
        dataframe : pandas.DataFrame
            The dataframe to check for values. 
        set_list_values : list or set
            The list or set values to match against the dataframe.

        Returns
        -------
        bool
            A True or False value whether the values exist in the dataframe.
        """
        value_exists = False
        for elem in set_list_values:
            if elem in dataframe.values:
                value_exists = True
                break
            else:
                continue
        return value_exists

    def test_import_file_data_expected_csv(self):
        df = self.imp.import_file_data(self.path1)
        self.assertTrue(
            len(df) > 0, 'Test: Check File Import Success - CSV File')

    def test_import_file_data_expected_xlsx(self):
        df = self.imp.import_file_data(self.path2, self.sheet1)
        self.assertTrue(
            len(df) > 0, 'Test: Check File Import Success - XLSX File')

    def test_import_file_data_expected_columns_match_one(self):
        df = self.imp.import_file_data(self.path1)
        self.assertTrue(self.check_if_value_exists(df.columns, self.df_columns),
                        'Test: Check File Import Success - Columns Match in DF1')

    def test_import_file_data_expected_columns_match_two(self):
        df = self.imp.import_file_data(self.path2, self.sheet1)
        self.assertTrue(self.check_if_value_exists(df.columns, self.df_columns),
                        'Test: Check File Import Success - Columns Match in DF2')

    def test_import_file_data_expected_columns_match_three(self):
        df = self.imp.import_file_data(self.path2, self.sheet2)
        self.assertTrue(self.check_if_value_exists(df.columns, self.df_columns),
                        'Test: Check File Import Success - Columns Match in DF3')

    def test_import_file_data_expected_columns_intersect(self):
        df1 = self.imp.import_file_data(self.path1)
        df1_set = set(df1.columns)
        df2 = self.imp.import_file_data(self.path2, self.sheet1)
        df2_set = set(df2.columns)
        df3 = self.imp.import_file_data(self.path2, self.sheet2)
        df3_set = set(df3.columns)
        df_intersect = self.df_columns.intersection(df1_set, df2_set, df3_set)
        self.assertTrue(len(df_intersect) == 4,
                        'Test: Check File Import Success - All Columns Imported From All Files')

    def test_import_file_data_expected_values_match_one(self):
        df = self.imp.import_file_data(self.path1)
        self.assertTrue(self.check_if_value_exists(
            df, self.df_values1), 'Test: Check File Import Success - Values Match in DF1')
        self.assertTrue(self.check_if_value_exists(
            df, self.df_values2), 'Test: Check File Import Success - Values Match in DF1')

    def test_import_file_data_expected_values_match_two(self):
        df = self.imp.import_file_data(self.path2, self.sheet1)
        self.assertTrue(self.check_if_value_exists(
            df, self.df_values3), 'Test: Check File Import Success - Values Match in DF2')
        self.assertTrue(self.check_if_value_exists(
            df, self.df_values4), 'Test: Check File Import Success - Values Match in DF2')

    def test_import_file_data_expected_values_match_three(self):
        df = self.imp.import_file_data(self.path2, self.sheet2)
        self.assertTrue(self.check_if_value_exists(
            df, self.df_values5), 'Test: Check File Import Success - Values Match in DF3')

    def test_import_file_data_unexpected_import_missing_sheet(self):
        df = self.imp.import_file_data(self.path3, self.sheet4)
        self.assertTrue(
            'ERROR' in df, 'Test: Check File Import Fail - Missing Sheet')

    def test_import_file_data_unexpected_import_wrong_file_type(self):
        df = self.imp.import_file_data(self.path5)
        self.assertTrue(
            'ERROR' in df, 'Test: Check File Import Fail - Wrong File Type')

    def test_import_file_data_unexpected_import_does_not_exist(self):
        df = self.imp.import_file_data(self.path6)
        self.assertTrue(
            'ERROR' in df, 'Test: Check File Import Fail - File Does Not Exist')

    def test_import_file_data_unexpected_columns_blank(self):
        df = self.imp.import_file_data(self.path3, self.sheet1)
        self.assertTrue(
            'ERROR' in df, 'Test: Check File Import Fail - Blank Column Name')

    def test_import_file_data_unexpected_columns_null(self):
        df = self.imp.import_file_data(self.path3, self.sheet2)
        self.assertTrue(
            'ERROR' in df, 'Test: Check File Import Fail - NULL Column Name')

    def test_import_file_data_unexpected_columns_duplicate(self):
        df = self.imp.import_file_data(self.path3, self.sheet3)
        self.assertTrue(
            'ERROR' in df, 'Test: Check File Import Fail - Duplicate Column Name')

    def test_import_file_data_unexpected_values_blank(self):
        df = self.imp.import_file_data(self.path4, self.sheet1)
        df_blank_values = df.isna().any(axis=None)
        self.assertTrue(df_blank_values,
                        'Test: Check File Import Success - Blank Values')


if __name__ == '__main__':
    unittest.main()
