import unittest, pandas as pd, os
from Exporter import Exporter

class ExporterTestCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cwd = os.getcwd() + '\\tests'
        cls.fake_cwd = 'C:\\Users\\tmolga\\Documents\\FakeFolder'
        cls.table_name1 = 'TestExport1'
        cls.table_name2 = 'TestExport2'
        cls.file_type1 = 'csv'
        cls.file_type2 = 'xlsx'
        cls.path1 = cls.cwd + '\\TestTable1.csv'
        cls.path2 = cls.cwd + '\\TestTable2.xlsx'
        cls.sheet = 'Sheet1'
        cls.data = pd.DataFrame({'col_one':['one', 'two', 'three', 'four'], 'col_two': [1, 2, 3, 4], 'col_three': [1.0, 2.0, 3.0, 4.0]})
        cls.data.index.name = 'Id'
        cls.empty_dataframe = pd.DataFrame({})
        cls.exp = Exporter()

    def test_export_file_data_expected_csv(self):
        export = self.exp.export_file_data(self.cwd,self.data, self.table_name1, self.file_type1)
        self.assertTrue('SUCCESS' in export, 'Test: Check File Export Success - CSV File')

    def test_export_file_data_expected_xlsx(self):
        export = self.exp.export_file_data(self.cwd, self.data, self.table_name2, self.file_type2)
        self.assertTrue('SUCCESS' in export, 'Test: Check File Export Success - XLSX File')

    def test_export_file_data_unexpected_directory_missing(self):
        export = self.exp.export_file_data(self.fake_cwd, self.data, self.table_name1, self.file_type1)
        self.assertTrue('ERROR' in export, 'Test: Check File Export Fail - Directory Does Not Exist')

    def test_export_file_data_unexpected_directory_empty(self):
        export = self.exp.export_file_data('', self.data, self.table_name1, self.file_type1)
        self.assertTrue('ERROR' in export, 'Test: Check File Export Fail - Folder Not Provided')

    def test_export_file_data_unexpected_data_missing(self):
        export = self.exp.export_file_data(self.cwd, self.empty_dataframe, self.table_name1, self.file_type1)
        self.assertTrue('ERROR' in export, 'Test: Check File Export Fail - No Data')


if __name__ == '__main__':
    unittest.main()
