__author__ = 'Sean Gerhardt'

import datetime
import sys

from PyQt5 import QtCore, QtWidgets, QtGui

from src import TakeStock_Reporter


class MyForm(QtWidgets.QWidget):
    def __init__(self):
        super(MyForm, self).__init__()

        self.ticker_label = QtWidgets.QLabel('Ticker Entry')
        self.ticker_entry = QtWidgets.QLineEdit()
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self.ticker_label)
        hbox.addWidget(self.ticker_entry)

        self.search_tickers_button = QtWidgets.QPushButton('Search Tickers')
        self.results_table = QtWidgets.QTableWidget()
        self.header_names = ['Ticker', 'Price', 'PE Ratio (TTM)', 'PEG Ratio', 'RSI', '52 Wk Hi-Low', 'Earnings Date']
        self.results_table.setColumnCount(len(self.header_names))
        self.results_table.setHorizontalHeaderLabels(self.header_names)
        self.results_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.export_button = QtWidgets.QPushButton('Export')

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addLayout(hbox)
        mainLayout.addWidget(self.search_tickers_button)
        mainLayout.addWidget(self.results_table)
        mainLayout.addWidget(self.export_button)
        self.setLayout(mainLayout)

        self.work = Worker(None, self.update_ui)
        self.thread = QtCore.QThread()

        self.work.moveToThread(self.thread)
        self.thread.start()

        self.search_tickers_button.clicked.connect(self.search_tickers_clicked)
        self.export_button.clicked.connect(self.export_clicked)

        self.setGeometry(300, 300, 1000, 325)
        self.setWindowTitle('TakeStock    ' + datetime.date.today().strftime("%b %d, %Y"))
        self.show()

    def export_clicked(self):
        import csv
        file_name = QtWidgets.QFileDialog.getSaveFileName(QtWidgets.QFileDialog(), caption="Save File", filter='*.csv',)
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
        self.setCursor(QtCore.Qt.BusyCursor)
        self.work.start_thread(gui=self)

    def update_ui(self):
        self.search_tickers_button.setEnabled(True)
        self.unsetCursor()


class Worker(QtCore.QThread):
    def __init__(self, parent=None, update_ui=None):
        QtCore.QThread.__init__(self, parent)
        if update_ui:
            self.finished.connect(update_ui)
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
                    item = QtWidgets.QTableWidgetItem(row.ticker)
                elif self.gui.header_names[col_index] == 'Price':
                    item = QtWidgets.QTableWidgetItem(row.price)
                elif self.gui.header_names[col_index] == 'PE Ratio (TTM)':
                    item = QtWidgets.QTableWidgetItem(row.pe_ratio)
                    if is_number(row.pe_ratio):
                        if 0 < float(row.pe_ratio) <= 20:
                            item.setForeground(QtGui.QColor('green'))
                        elif 20 < float(row.pe_ratio) < 70:
                            item.setForeground(QtGui.QColor('orange'))
                        elif float(row.pe_ratio) > 70:
                            item.setForeground(QtGui.QColor('red'))
                elif self.gui.header_names[col_index] == 'PEG Ratio':
                    item = QtWidgets.QTableWidgetItem(row.peg_ratio)
                    if is_number(row.peg_ratio):
                        if 0 < float(row.peg_ratio) <= 1:
                            item.setForeground(QtGui.QColor('green'))
                        elif float(row.peg_ratio) > 1:
                            item.setForeground(QtGui.QColor('orange'))
                        elif float(row.peg_ratio) < 0:
                            item.setForeground(QtGui.QColor('red'))
                elif self.gui.header_names[col_index] == 'RSI':
                    item = QtWidgets.QTableWidgetItem(row.rsi)
                    if is_number(row.rsi):
                        if 0 < float(row.rsi) <= 30:
                            item.setForeground(QtGui.QColor('green'))
                        elif 30 < float(row.rsi) < 70:
                            item.setForeground(QtGui.QColor('orange'))
                        elif float(row.rsi) > 70:
                            item.setForeground(QtGui.QColor('red'))
                elif self.gui.header_names[col_index] == '52 Wk Hi-Low':
                    item = QtWidgets.QTableWidgetItem(row.fifty_two)
                elif self.gui.header_names[col_index] == 'Earnings Date':
                    item = QtWidgets.QTableWidgetItem(row.earnings_date)
                    if row.earnings_soon:
                        font = QtGui.QFont()
                        font.setBold(True)
                        font.setPointSize(14)
                        item.setFont(font)
                else:
                    item = QtWidgets.QTableWidgetItem('No Data Found')
                self.gui.results_table.setItem(row_index, col_index, item)


def is_number(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


def main():
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MyForm()
    status = app.exec_()
    sys.exit(status)


def test_harness():
    return QtWidgets.QApplication(sys.argv)

if __name__ == "__main__":
    main()
