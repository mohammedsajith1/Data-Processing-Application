import unittest
from io import StringIO
from main import SalesDataIngestion
import pandas as pd

class TestSalesData(unittest.TestCase):
    def test_load_sales_data(self):
        csv_data = """Order Date,Price Each,Quantity Ordered
2021-01-01,20,5
2021-02-01,30,10"""
        sales_ingestion = SalesDataIngestion()
        df = sales_ingestion.load_data(StringIO(csv_data))
        self.assertIsNotNone(df)
        self.assertFalse(df.empty)

if __name__ == '__main__':
    unittest.main()
