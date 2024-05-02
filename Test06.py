import unittest
from io import StringIO
from main import PurchasePriceDataIngestion
import pandas as pd

class TestPurchasePriceDataCleaning(unittest.TestCase):
    def test_clean_purchase_price_data(self):
        csv_data = """Volume,Size
500ml,250ml
1000ml,500ml"""
        purchase_ingestion = PurchasePriceDataIngestion()
        df = pd.read_csv(StringIO(csv_data))
        clean_df = purchase_ingestion.clean_data(df)
        self.assertIn('Volume_ml', clean_df.columns)
        self.assertIn('Size_ml', clean_df.columns)

if __name__ == '__main__':
    unittest.main()

