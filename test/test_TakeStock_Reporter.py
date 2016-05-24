import unittest
import getopt
import sys

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

    def test_opts(self):
        # Override existing args for testing
        sys.argv[1] = '-v'
        sys.argv[2] = '-f'
        sys.argv.append('-t AAPL')
        sys.argv.append('-i')
        sys.argv.append('-g')
        sys.argv.append('-z')
        sys.argv.append('-t AAPL')


        TakeStock_Reporter.tickers = ['\'AAPL\'']
        TakeStock_Reporter.main()
        self.assertTrue(TakeStock_Reporter.verbose)
        self.assertTrue(TakeStock_Reporter.fifty_two)
        self.assertTrue(TakeStock_Reporter.rsi)
        self.assertTrue(TakeStock_Reporter.pe_ratio)
        self.assertTrue(TakeStock_Reporter.peg_ratio)

if __name__ == '__main__':
    unittest.main()
