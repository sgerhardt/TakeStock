__author__ = 'Sean Gerhardt'

import sys

from PyQt4 import QtGui
from PyQt4 import QtCore

import TakeStock_Reporter


class MyForm(QtGui.QWidget):
    def __init__(self):
        super(MyForm, self).__init__()

        self.ticker_label = QtGui.QLabel('Ticker Entry')
        self.ticker_entry = QtGui.QLineEdit()
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.ticker_label)
        hbox.addWidget(self.ticker_entry)

        self.search_tickers = QtGui.QPushButton('Search Tickers')
        self.results_table = QtGui.QTableWidget()
        self.results_table.setColumnCount(6)
        self.header_names = ['Ticker', 'Price', 'PEG Ratio', 'RSI', '52 Wk Hi-Low', 'Earnings Date']
        self.results_table.setHorizontalHeaderLabels(self.header_names)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addLayout(hbox)
        mainLayout.addWidget(self.search_tickers)
        mainLayout.addWidget(self.results_table)
        self.setLayout(mainLayout)

        self.thread = Worker()
        self.connect(self.thread, QtCore.SIGNAL("finished()"), self.updateUi)
        self.connect(self.thread, QtCore.SIGNAL("terminated()"), self.updateUi)
        self.connect(self.thread, QtCore.SIGNAL("output()"), self.test)
        self.connect(self.search_tickers, QtCore.SIGNAL("clicked()"), self.search_tickers_clicked)

        self.setGeometry(300, 300, 800, 300)
        self.setWindowTitle('TakeStock')
        self.show()

    def test(self):
        print('test')

    def search_tickers_clicked(self):
        self.search_tickers.setEnabled(False)
        self.thread.start_thread(gui=self)

    def updateUi(self):
        self.search_tickers.setEnabled(True)


class Worker(QtCore.QThread):
    def __init__(self, parent=None):

        QtCore.QThread.__init__(self, parent)
        self.exiting = False

    def __del__(self):
        self.exiting = True
        self.wait()

    def start_thread(self, gui):
        self.gui = gui
        self.start()

    def run(self):
        # Note: This is never called directly. It is called by Qt once the
        # thread environment has been set up.
        self.gui.results = TakeStock_Reporter.get_results(tickers=self.gui.ticker_entry.text().replace(" ", '').split(','))
        if self.gui.results == None:
            return
        self.gui.results_table.setRowCount(len(self.gui.results))
        self.gui.results_table.setColumnCount(len(self.gui.results[0].__dict__))

        for row_index, row in enumerate(self.gui.results):
            for col_index in range(len(row.__dict__)):
                if self.gui.header_names[col_index] == 'Ticker':
                    item = QtGui.QTableWidgetItem(row.ticker)
                elif self.gui.header_names[col_index] == 'Price':
                    item = QtGui.QTableWidgetItem(row.price)
                elif self.gui.header_names[col_index] == 'PEG Ratio':
                    item = QtGui.QTableWidgetItem(row.peg_ratio)
                elif self.gui.header_names[col_index] == 'PEG Ratio':
                    item = QtGui.QTableWidgetItem(row.peg_ratio)
                elif self.gui.header_names[col_index] == 'RSI':
                    item = QtGui.QTableWidgetItem(row.rsi)
                elif self.gui.header_names[col_index] == '52 Wk Hi-Low':
                    item = QtGui.QTableWidgetItem(row.fifty_two)
                elif self.gui.header_names[col_index] == 'Earnings Date':
                    item = QtGui.QTableWidgetItem(row.earnings_date)
                else:
                    item = QtGui.QTableWidgetItem('No Data Found')
                self.gui.results_table.setItem(row_index, col_index, item)


app = QtGui.QApplication(sys.argv)
mainWindow = MyForm()
status = app.exec_()
sys.exit(status)