__author__ = 'Sean Gerhardt'

import datetime
import re

import bs4
import requests


def main():
    pass


timeout = 3


def get_share_price(ticker=''):
    """
    This function gets the share price for the given ticker symbol. It performs a request to the
    nasdaq url and parses the response to find the share price.
    :param ticker: The stock symbol/ticker to use for the lookup
    :return: String containing the earnings date
    """
    try:
        earnings_url = 'https://finance.yahoo.com/q/ks?s=' + ticker.lower() + '+Key+Statistics'
        request = requests.get(earnings_url, timeout=timeout)
        soup = bs4.BeautifulSoup(request.text, 'html.parser')
        # TODO replace magic string with reasonable/free API call
        return '$' + soup.find('span', {'data-reactid': '50'}).text
    except:
        return 'No Data Found'


def get_earnings_date(ticker=''):
    """
    This function gets the earnings date for the given ticker symbol. It performs a request to the
    zacks url and parses the response to find the earnings date.
    :param ticker: The stock symbol/ticker to use for the lookup
    :return: String containing the earnings date
    """
    try:
        earnings_url = 'https://www.zacks.com/stock/quote/' + ticker.upper()
        request = requests.get(earnings_url, timeout=timeout, headers={
         'User-Agent': 'Mozilla'
        })
        soup = bs4.BeautifulSoup(request.text, 'html.parser')
        # TODO replace magic string with reasonable/free API call
        return soup.find('section', {'id': 'stock_key_earnings'}).find('table', attrs={'abut_bottom'}).find('tbody').findAll(
            'tr')[4].findAll('td')[1].text.replace('*AMC', '')
    except:
        return 'No Data Found'


def get_fifty_two_week_high_low(ticker=''):
    """
    This function gets the fifty-two week high and lows for the given ticker symbol. It performs a request to the
    Yahoo url and parses the response to find the fifty-two week high and low.
    :param ticker: The stock symbol/ticker to use for the lookup
    :return: String containing the fifty two week high and low
    """
    try:
        earnings_url = 'https://finance.yahoo.com/q/ks?s=' + ticker.lower() + '+Key+Statistics'
        request = requests.get(earnings_url, timeout=timeout)
        soup = bs4.BeautifulSoup(request.text, 'html.parser')
        # TODO replace magic string with reasonable/free API call
        rows = soup.findAll('tr')
        high, low = 0, 0
        for row in rows:
            if '52 Week High' in row.text:
               high = row.contents[1].contents[0]
        for row in rows:
            if '52 Week Low' in row.text:
               low = row.contents[1].contents[0]
        return high + 'H ' + low + 'L'
    except:
        return 'No Data Found'


def get_trailing_pe_ratio(ticker=''):
    """
    This function gets the trailing PE ratio for the given ticker symbol. It performs a request to the
    Yahoo url and parses the response to find the trailing PE ratio.
    :param ticker: The stock symbol/ticker to use for the lookup
    :return: String containing the trailing PE ratio
    """
    try:
        key_stats_url = 'https://finance.yahoo.com/q/ks?s=' + ticker.lower() + '+Key+Statistics'
        request = requests.get(key_stats_url, timeout=timeout)
        soup = bs4.BeautifulSoup(request.text, 'html.parser')
        return soup.find(text=re.compile('Trailing P/E')).findNext('td').text
    except:
        return 'No Data Found'


def get_peg_ratio(ticker=''):
    """
    This function gets the PEG ratio for the given ticker symbol. It performs a request to the
    Yahoo url and parses the response to find the PEG ratio.
    :param ticker: The stock symbol/ticker to use for the lookup
    :return: String containing the PEG ratio
    """
    try:
        key_stats_url = 'https://finance.yahoo.com/q/ks?s=' + ticker.lower() + '+Key+Statistics'
        request = requests.get(key_stats_url, timeout=timeout)
        soup = bs4.BeautifulSoup(request.text, 'html.parser')
        return soup.find(text=re.compile('PEG Ratio')).findNext('td').text
    except:
        return 'No Data Found'


def get_rsi(ticker=''):
    """
    This function gets the rsi for the given ticker symbol. It performs a request to the
    nasdaq url and parses the response to find the rsi.
    :param ticker: The stock symbol/ticker to use for the lookup
    :return: String containing the rsi
    """
    try:
        rsi_url = 'https://charting.nasdaq.com/ext/charts.dll?2-1-14-0-0-512-03NA000000' + ticker.upper() \
                  + '-&SF:1|27-SH:27=10-BG=FFFFFF-BT=0-WD=635-HT=395--XTBL-'
        request = requests.get(rsi_url, timeout=timeout)
        soup = bs4.BeautifulSoup(request.text, 'html.parser')
        return soup.find_all('td', class_="DrillDownData")[1].text
    except:
        return 'No Data Found'


# def get_past_consensus_performance(ticker=''):
# TODO finish implementation
#     """
#     This function gets the past performance versus analyst consensus for the given ticker symbol.
#     It performs a request to the nasdaq url and parses the response to get the data
#     :param ticker: The stock symbol/ticker to use for the lookup
#     :return: String containing the performance against consensus for past
#     """
#     try:
#         earnings_url = 'https://www.nasdaq.com/symbol/' + ticker.lower() + '/earnings-surprise'
#         request = requests.get(earnings_url)git
#         soup = bs4.BeautifulSoup(request.text, 'html.parser')
#         # tag = soup.find(text=re.compile(''))
#         # return tag[tag.index(':') + 1:].strip()
#     except:
#         return 'No Data Found'


def get_stocks(tickers=None):
    """
    This function creates a list of Stock objects.
    """
    stocks = []
    for ticker in tickers:
        stocks.append(
            Stock(price=get_share_price(ticker), earnings_date=get_earnings_date(ticker=ticker),
                  ticker=ticker, pe_ratio=get_trailing_pe_ratio(ticker), peg_ratio=get_peg_ratio(ticker),
                  rsi=get_rsi(ticker=ticker), fifty_two=get_fifty_two_week_high_low(ticker=ticker)))
    return stocks


class Stock:
    """
    Defines a stock.
    """

    def __init__(self, price=0, earnings_date='', ticker='', pe_ratio='', peg_ratio='', rsi='', fifty_two=''):
        self.price = price
        self.earnings_date = earnings_date
        self.earnings_soon = False
        if self.earnings_date:
            if self.earnings_date != 'No Data Found':
                dayStart = self.earnings_date[self.earnings_date.index('/') + 1:]
                day = dayStart[:dayStart.index('/')]
                earnings_date = datetime.date(year=int(self.earnings_date[len(self.earnings_date) - 2:]),
                                              month=int(self.earnings_date[0:2].replace('/', '')),
                                              day=int(day))
                if 0 <= abs((earnings_date - datetime.date.today()).days) <= 7:
                    self.earnings_soon = True

        self.ticker = ticker
        self.pe_ratio = pe_ratio
        self.peg_ratio = peg_ratio
        self.rsi = rsi
        self.fifty_two = fifty_two


if __name__ == "__main__":
    # If the script is being invoked directly, run the main method.
    main()
