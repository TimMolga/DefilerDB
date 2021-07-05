DB_NAME = 'Defiler.db'

IMPORT_INFO = """
              IMPORTING DATA:
              -------------------------------------------
              Data needs to be imported from a CSV or XLSX file prior to querying.

              How To:

              -Browse for the file you wish to import
              -Enter the sheet you wish to import (if an XLSX file).

              Data Requirements:

              -Column values cannot be empty, null, or duplicates.
              -There are no restrictions with data values.
              """

QUERY_INFO = """
             QUERYING DATA:
             -------------------------------------------
             Use SQL syntax compatible with SQLite3 to perform queries on available tables.

             Only SELECT queries are allowed at this time.
             """

EXPORT_INFO = """
              EXPORTING DATA:
              -------------------------------------------
              Data that is queried can be exported to a CSV or XLSX file.

              How To:
              
              -Browse for the folder you wish to export the data to.
              -Choose the type of file you wish to save the file as (CSV or XLSX).
              """

ABOUT_INFO = """
             ABOUT DEFILERDB:
             -------------------------------------------
             DefilerDB is a database solution to query CSV and XLSX files of your own data.

             Query your data with SQL syntax and create CSV or XLSX files with the data you want.

             DefilerDB utilizes a SQLite3 database so your data is all stored locally and you have full control over it.

             """
