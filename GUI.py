__author__ = 'Sean Gerhardt'

import sys
from PyQt4 import QtGui

import TakeStock_Reporter


class MyForm(QtGui.QWidget):
    def __init__(self):
        super(MyForm, self).__init__()
        self.ticker_entry = QtGui.QLineEdit()

        self.search_tickers = QtGui.QPushButton('Search Tickers')
        self.search_tickers.clicked.connect(self.search_tickers_clicked)

        self.results_table = QtGui.QTableWidget()
        self.results_table.setColumnCount(6)
        self.header_names = ['Ticker', 'Price', 'PEG Ratio', 'RSI', '52 Wk Hi-Low', 'Earnings Date']
        self.results_table.setHorizontalHeaderLabels(self.header_names)

        mainLayout = QtGui.QFormLayout()
        mainLayout.addRow('Ticker:', self.ticker_entry)
        mainLayout.addRow(self.search_tickers)
        mainLayout.addRow('Results:', self.results_table)
        self.setLayout(mainLayout)

        self.setGeometry(300, 300, 800, 300)
        self.setWindowTitle('TakeStock')
        self.show()

    def search_tickers_clicked(self):
        self.results = TakeStock_Reporter.get_results(tickers=self.ticker_entry.text().replace(" ", '').split(','))
        if self.results == None:
            return
        self.results_table.setRowCount(len(self.results))
        self.results_table.setColumnCount(len(self.results[0].__dict__))

        for row_index, row in enumerate(self.results):
            for col_index in range(len(row.__dict__)):
                if self.header_names[col_index] == 'Ticker':
                    item = QtGui.QTableWidgetItem(row.ticker)
                elif self.header_names[col_index] == 'Price':
                    item = QtGui.QTableWidgetItem(row.price)
                elif self.header_names[col_index] == 'PEG Ratio':
                    item = QtGui.QTableWidgetItem(row.peg_ratio)
                elif self.header_names[col_index] == 'PEG Ratio':
                    item = QtGui.QTableWidgetItem(row.peg_ratio)
                elif self.header_names[col_index] == 'RSI':
                    item = QtGui.QTableWidgetItem(row.rsi)
                elif self.header_names[col_index] == '52 Wk Hi-Low':
                    item = QtGui.QTableWidgetItem(row.fifty_two)
                elif self.header_names[col_index] == 'Earnings Date':
                    item = QtGui.QTableWidgetItem(row.earnings_date)
                else:
                    item = QtGui.QTableWidgetItem('No Data Found')
                self.results_table.setItem(row_index, col_index, item)

app = QtGui.QApplication(sys.argv)
mainWindow = MyForm()
status = app.exec_()
sys.exit(status)