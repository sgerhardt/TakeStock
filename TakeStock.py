__author__ = 'Sean Gerhardt'

import sys
import datetime

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

        self.search_tickers_button = QtGui.QPushButton('Search Tickers')
        self.results_table = QtGui.QTableWidget()
        self.results_table.setColumnCount(6)
        self.header_names = ['Ticker', 'Price', 'PEG Ratio', 'RSI', '52 Wk Hi-Low', 'Earnings Date']
        self.results_table.setHorizontalHeaderLabels(self.header_names)
        self.results_table.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.export_button = QtGui.QPushButton('Export')

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addLayout(hbox)
        mainLayout.addWidget(self.search_tickers_button)
        mainLayout.addWidget(self.results_table)
        mainLayout.addWidget(self.export_button)
        self.setLayout(mainLayout)

        self.thread = Worker()
        self.connect(self.thread, QtCore.SIGNAL("finished()"), self.updateUi)
        self.connect(self.thread, QtCore.SIGNAL("terminated()"), self.updateUi)
        self.connect(self.search_tickers_button, QtCore.SIGNAL("clicked()"), self.search_tickers_clicked)
        self.connect(self.export_button, QtCore.SIGNAL("clicked()"), self.export_clicked)

        self.setGeometry(300, 300, 800, 325)
        self.setWindowTitle('TakeStock    ' + datetime.date.today().strftime("%b %d, %Y"))
        self.show()

    def export_clicked(self):
        import csv
        file_name = QtGui.QFileDialog.getSaveFileName(QtGui.QFileDialog(), caption="Save File", filter='*.csv',)
        with open(file_name, newline='', mode='w') as csvfile:
            csv_writer = csv.writer(csvfile)
            row_result = []
            csv_writer.writerow(self.header_names)
            for row_index in range(self.results_table.rowCount()):
                for col_index in range(self.results_table.columnCount()):
                    row_result.append(self.results_table.item(row_index, col_index).text())
                csv_writer.writerow(row_result)
                row_result = []


    def search_tickers_clicked(self):
        self.search_tickers_button.setEnabled(False)
        self.thread.start_thread(gui=self)

    def updateUi(self):
        self.search_tickers_button.setEnabled(True)


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
        self.gui.results = TakeStock_Reporter.get_results(
            tickers=self.gui.ticker_entry.text().replace(" ", '').split(','))
        if self.gui.results is None:
            return
        self.gui.results_table.setRowCount(len(self.gui.results))
        self.gui.results_table.setColumnCount(len(self.gui.results[0].__dict__) - 1)

        for row_index, row in enumerate(self.gui.results):
            for col_index in range(len(row.__dict__) - 1):
                if self.gui.header_names[col_index] == 'Ticker':
                    item = QtGui.QTableWidgetItem(row.ticker)
                elif self.gui.header_names[col_index] == 'Price':
                    item = QtGui.QTableWidgetItem(row.price)
                elif self.gui.header_names[col_index] == 'PEG Ratio':
                    item = QtGui.QTableWidgetItem(row.peg_ratio)
                    if is_number(row.peg_ratio):
                        if 0 < float(row.peg_ratio) <= 1:
                            item.setTextColor(QtGui.QColor('green'))
                        elif float(row.peg_ratio) > 1:
                            item.setTextColor(QtGui.QColor('orange'))  # Dark Yellow
                        elif float(row.peg_ratio) < 0:
                            item.setTextColor(QtGui.QColor('red'))
                elif self.gui.header_names[col_index] == 'RSI':
                    item = QtGui.QTableWidgetItem(row.rsi)
                    if is_number(row.rsi):
                        if 0 < float(row.rsi) <= 30:
                            item.setTextColor(QtGui.QColor('green'))
                        elif 30 < float(row.rsi) < 70:
                            item.setTextColor(QtGui.QColor('orange'))  # Dark Yellow
                        elif float(row.rsi) > 70:
                            item.setTextColor(QtGui.QColor('red'))
                elif self.gui.header_names[col_index] == '52 Wk Hi-Low':
                    item = QtGui.QTableWidgetItem(row.fifty_two)
                elif self.gui.header_names[col_index] == 'Earnings Date':
                    item = QtGui.QTableWidgetItem(row.earnings_date)
                    if row.earnings_soon:
                        font = QtGui.QFont()
                        font.setBold(True)
                        font.setPointSize(14)
                        item.setFont(font)
                else:
                    item = QtGui.QTableWidgetItem('No Data Found')
                self.gui.results_table.setItem(row_index, col_index, item)


def is_number(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


app = QtGui.QApplication(sys.argv)
mainWindow = MyForm()
status = app.exec_()
sys.exit(status)
