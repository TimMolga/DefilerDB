import unittest, pandas as pd
from DefilerDB import DefilerDB

class DefilerDBTestCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.df_db = DefilerDB()
        cls.table_name = 'Test_Table'
        cls.column_names_types = 'id INTEGER, col_one TEXT,col_two INTEGER,col_three REAL'
        cls.column_names = 'id,col_one,col_two,col_three'
        cls.dataframe = pd.DataFrame({'col_one':['one', 'two', 'three', 'four'], 'col_two': [1, 2, 3, 4], 'col_three': [1.0, 2.0, 3.0, 4.0]})
        cls.dataframe.index.name = 'id'
        cls.empty_dataframe = pd.DataFrame({})
        cls.query_string1 = f'SELECT * FROM {cls.table_name}'
        cls.query_string2 = f'INSERT INTO {cls.table_name} (col_one) VALUES (\'five\')'
        cls.query_string3 = f'SELECT col_one FROM col_one'
        cls.query_string4 = f'SELECT FROM UPDATE'

    def test_execute_create_query_expected(self):
        self.df_db.execute_drop_table_query(self.table_name)
        creation_status = self.df_db.execute_create_table_query(self.table_name, self.column_names_types)
        self.assertTrue('SUCCESS' in creation_status, 'Test: Check Table Create Success - Table Created')

    def test_execute_create_query_unexpected_table_exists(self):
        creation_status = self.df_db.execute_create_table_query(self.table_name, self.column_names_types)
        self.assertTrue('ERROR' in creation_status, 'Test: Check Table Create Error - Table Exists')

    def test_execute_insert_query_expected(self):
        insert_status = self.df_db.execute_insert_query(self.table_name, self.column_names, self.dataframe)
        self.assertTrue('SUCCESS' in insert_status, 'Test: Check Table Insert Success - Data Inserted')

    def test_execute_insert_query_unexpected_data_missing(self):
        insert_status = self.df_db.execute_insert_query(self.table_name, self.column_names, self.empty_dataframe)
        self.assertTrue('ERROR' in insert_status, 'Test: Check Table Insert Error - Data Missing')

    def test_execute_select_query_expected_all(self):
        select_status = self.df_db.execute_select_query(self.query_string1)
        self.assertTrue(isinstance(select_status, pd.DataFrame), 'Test: Check Table Select Error - Select All')

    def test_execute_select_query_unexpected_invalid_operation(self):
        select_status = self.df_db.execute_select_query(self.query_string2)
        self.assertTrue('ERROR' in select_status, 'Test: Check Table Select Error - Invalid Operation')

    def test_execute_select_query_unexpected_invalid_table(self):
        select_status = self.df_db.execute_select_query(self.query_string3)
        self.assertTrue('ERROR' in select_status, 'Test: Check Table Select Error - Invalid Table')

    def test_execute_select_query_unexpected_invalid_syntax(self):
        select_status = self.df_db.execute_select_query(self.query_string4)
        self.assertTrue('ERROR' in select_status, 'Test: Check Table Select Error - Invalid Syntax')

    def test_execute_table_drop_query_expected(self):
        drop_status = self.df_db.execute_drop_table_query(self.table_name)
        self.assertTrue('SUCCESS' in drop_status, 'Test: Check Table Drop Success - Table Dropped')

    def test_execute_table_drop_query_unexpected_table_missing(self):
        drop_status = self.df_db.execute_drop_table_query('')
        self.assertTrue('ERROR' in drop_status, 'Test: Check Table Drop Error - Table Name Missing')


if __name__ == '__main__':
    unittest.main()
