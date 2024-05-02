import unittest
import pandas as pd
from main import plot_purchase_price_data

class TestPlotPurchasePriceData(unittest.TestCase):
    def test_plot_purchase_price_data(self):
        df = pd.DataFrame({
            'PurchasePrice': [10, 20],
            'Price': [30, 50],
            'Classification': ['A', 'B'],
            'VendorName': ['Vendor1', 'Vendor2']
        })
        print("Testing DataFrame:", df)
        try:
            plot_purchase_price_data(df)
            plot_success = True
        except Exception as e:
            print(f"Plotting Error: {e}")
            plot_success = False
        self.assertTrue(plot_success)

if __name__ == '__main__':
    unittest.main()
