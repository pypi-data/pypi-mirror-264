# XLSX DictReader

This is a simple Python module that takes an openpyxl `Worksheet` object and returns a list of dictionaries. Each dictionary represents a row in the Excel file. The keys of the dictionary are the column names and the values are the cell values.

I've recently found myself, several times, wanting a thing like `csv.DictReader` for specific ranges of cells in Excel files. This does the job for me so far.

Sample Usage:

```python

from openpyxl import load_workbook
from xlsx_dictreader import DictReader

wb = load_workbook('sample.xlsx', data_only=True)
ws = wb.active


reader = DictReader(ws, skip_blank=True)
for row in reader:
    print(row)

```
