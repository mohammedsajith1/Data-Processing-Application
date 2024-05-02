import unittest
from io import StringIO
from main import FinanceDataIngestion
import pandas as pd

class TestFinanceDataCleaning(unittest.TestCase):
    def test_clean_finance_data(self):
        csv_data = """date,units_sold,manufacturing_price,sale_price,gross_sales,discounts,sales,cogs,profit
2021-01-01,'100','$10','$20','$2000','$200','$1800','$800','$1000'"""
        finance_ingestion = FinanceDataIngestion()
        df = pd.read_csv(StringIO(csv_data))
        clean_df = finance_ingestion.clean_data(df)
        self.assertTrue(pd.api.types.is_float_dtype(clean_df['manufacturing_price']))
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(clean_df['date']))

if __name__ == '__main__':
    unittest.main()
