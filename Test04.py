import unittest
from io import StringIO
from main import SalesDataIngestion
import pandas as pd

class TestSalesDataCleaning(unittest.TestCase):
    def test_clean_sales_data(self):
        csv_data = """Order Date,Price Each,Quantity Ordered
2021-01-01,20,5
2021-02-01,30,10"""
        sales_ingestion = SalesDataIngestion()
        df = pd.read_csv(StringIO(csv_data))
        clean_df = sales_ingestion.clean_data(df)
        self.assertTrue('Profit' in clean_df.columns)

if __name__ == '__main__':
    unittest.main()
