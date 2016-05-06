import unittest
import time

from PyQt4.QtTest import QTest
from PyQt4.QtCore import Qt

from src import TakeStock


class MyFormTest(unittest.TestCase):
    def test_defaults(self):
        ticker = 'aapl'
        harness = TakeStock.test_harness()
        form = TakeStock.MyForm()
        self.assertEquals(form.ticker_label.text(), "Ticker Entry")
        QTest.keyClicks(form.ticker_entry, ticker)
        QTest.mouseClick(form.search_tickers_button, Qt.LeftButton)
        # Wait 10 seconds before timing out
        trys = 0
        while trys < 10:
            trys += 1
            time.sleep(1)
            if form.results_table.item(0, 0) is not None:
                break
        self.assertEquals(form.results_table.item(0, 0).text(), ticker)
