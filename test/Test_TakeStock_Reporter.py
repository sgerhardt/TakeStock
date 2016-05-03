import unittest

from src import TakeStock_Reporter


class TakeStockReporterTest(unittest.TestCase):
    def test_get_results(self):
        test_ticker = 'AAPL'
        result = TakeStock_Reporter.get_results(tickers=[test_ticker])[0]
        self.assertIsNotNone(result)
        self.assertEqual(result.price[0], '$')
        self.assertGreater(float(result.price[1:]), 0)
        self.assertGreater(float(result.rsi), 0)
        self.assertIsNotNone(result.fifty_two)
        self.assertIsNotNone(result.pe_ratio)
        self.assertIsNotNone(result.peg_ratio)
        if result.earnings_soon:
            self.assertIsNotNone(result.earnings_date)

if __name__ == '__main__':
    unittest.main()
