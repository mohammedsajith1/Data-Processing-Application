import unittest
from io import StringIO
from main import PurchasePriceDataIngestion
import pandas as pd

class TestPurchasePriceData(unittest.TestCase):
    def test_load_purchase_price_data(self):
        csv_data = """Volume,Size
500ml,250ml
1000ml,500ml"""
        purchase_ingestion = PurchasePriceDataIngestion()
        df = purchase_ingestion.load_data(StringIO(csv_data))
        self.assertIsNotNone(df)
        self.assertFalse(df.empty)

if __name__ == '__main__':
    unittest.main()




