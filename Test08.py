import unittest
import pandas as pd
from main import plot_sales_data

class TestPlotSalesData(unittest.TestCase):
    def test_plot_sales_data(self):
        df = pd.DataFrame({
            'Order Date': pd.to_datetime(['2021-01-01', '2021-02-01']),
            'Profit': [500, 1000]
        })
        try:
            plot_sales_data(df)
            plot_success = True
        except Exception:
            plot_success = False
        self.assertTrue(plot_success)

if __name__ == '__main__':
    unittest.main()
