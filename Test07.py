import unittest
import pandas as pd
from main import plot_finance_data

class TestPlotFinanceData(unittest.TestCase):
    def test_plot_finance_data(self):
        df = pd.DataFrame({
            'product': ['A', 'B'],
            'sales': [1000, 2000],
            'date': pd.to_datetime(['2021-01-01', '2021-02-01']),
            'profit': [500, 1000]
        })
        try:
            plot_finance_data(df)
            plot_success = True
        except Exception:
            plot_success = False
        self.assertTrue(plot_success)

if __name__ == '__main__':
    unittest.main()
