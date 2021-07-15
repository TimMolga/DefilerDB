import unittest
from ImporterTestCases import *
from ExporterTestCases import *
from DefilerDBTestCases import *


def suite():
    suite = unittest.TestSuite()
    suite.addTests([
        ImporterTestCases('test_import_file_data_expected_csv'),
        ImporterTestCases('test_import_file_data_expected_xlsx'),
        ImporterTestCases('test_import_file_data_expected_columns_match_one'),
        ImporterTestCases('test_import_file_data_expected_columns_match_two'),
        ImporterTestCases(
            'test_import_file_data_expected_columns_match_three'),
        ImporterTestCases('test_import_file_data_expected_columns_intersect'),
        ImporterTestCases('test_import_file_data_expected_values_match_one'),
        ImporterTestCases('test_import_file_data_expected_values_match_two'),
        ImporterTestCases('test_import_file_data_expected_values_match_three'),
        ImporterTestCases(
            'test_import_file_data_unexpected_import_missing_sheet'),
        ImporterTestCases(
            'test_import_file_data_unexpected_import_wrong_file_type'),
        ImporterTestCases(
            'test_import_file_data_unexpected_import_does_not_exist'),
        ImporterTestCases('test_import_file_data_unexpected_columns_blank'),
        ImporterTestCases('test_import_file_data_unexpected_columns_null'),
        ImporterTestCases(
            'test_import_file_data_unexpected_columns_duplicate'),
        ImporterTestCases('test_import_file_data_unexpected_values_blank'),
        ExporterTestCases('test_export_file_data_expected_csv'),
        ExporterTestCases('test_export_file_data_expected_xlsx'),
        ExporterTestCases(
            'test_export_file_data_unexpected_directory_missing'),
        ExporterTestCases('test_export_file_data_unexpected_directory_empty'),
        ExporterTestCases('test_export_file_data_unexpected_data_missing'),
        DefilerDBTestCases('test_execute_create_query_expected'),
        DefilerDBTestCases(
            'test_execute_create_query_unexpected_table_exists'),
        DefilerDBTestCases('test_execute_insert_query_expected'),
        DefilerDBTestCases(
            'test_execute_insert_query_unexpected_data_missing'),
        DefilerDBTestCases('test_execute_select_query_expected_all'),
        DefilerDBTestCases(
            'test_execute_select_query_unexpected_invalid_operation'),
        DefilerDBTestCases(
            'test_execute_select_query_unexpected_invalid_table'),
        DefilerDBTestCases(
            'test_execute_select_query_unexpected_invalid_syntax'),
        DefilerDBTestCases('test_execute_table_drop_query_expected'),
        DefilerDBTestCases(
            'test_execute_table_drop_query_unexpected_table_missing'),
    ])
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
