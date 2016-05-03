import unittest

from src import QuarterlyReport

testing_ticker = 'AAPL'


class QuarterlyReportTest(unittest.TestCase):

    def test_get_share_price(self):
        share_price = QuarterlyReport.get_share_price(testing_ticker)
        self.assertIsNotNone(share_price)
        self.assertIn('$', share_price)

    def test_get_earnings_date(self):
        self.assertIsNotNone(QuarterlyReport.get_earnings_date(testing_ticker))

    def test_get_fifty_two_week_high_low(self):
        hi_low = QuarterlyReport.get_fifty_two_week_high_low(testing_ticker)
        self.assertIsNotNone(hi_low)
        self.assertIn('H', hi_low)
        self.assertIn('L', hi_low)

    def test_get_trailing_pe_ratio(self):
        pe = QuarterlyReport.get_trailing_pe_ratio(testing_ticker)
        self.assertIsNotNone(pe)
        self.assertTrue(is_numeric(float(pe)))

    def test_get_peg_ratio(self):
        peg = QuarterlyReport.get_peg_ratio(testing_ticker)
        self.assertIsNotNone(peg)
        self.assertTrue(is_numeric(float(peg)))

    def test_get_rsi(self):
        rsi = QuarterlyReport.get_rsi(testing_ticker)
        self.assertIsNotNone(rsi)
        self.assertTrue(is_numeric(float(rsi)))


def is_numeric(obj):
    attrs = ['__add__', '__sub__', '__mul__', '__truediv__', '__pow__']
    return all(hasattr(obj, attr) for attr in attrs)

if __name__ == '__main__':
    unittest.main()
