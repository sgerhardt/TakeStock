__author__ = 'Sean Gerhardt'

import requests
import bs4
import re
import Suds_Client


def main():
    pass


def get_earnings_date(ticker=''):
    """
    This function gets the earnings date for the given ticker symbol. It performs a request to the
    nasdaq url and parses the response to find the earnings date.
    :param ticker: The stock symbol/ticker to use for the lookup
    :return: String containing the earnings date
    """
    try:
        earnings_url = 'http://www.nasdaq.com/earnings/report/' + ticker.lower()
        request = requests.get(earnings_url)
        soup = bs4.BeautifulSoup(request.text, 'html.parser')
        tag = soup.find(text=re.compile('Earnings announcement*'))
        return tag[tag.index(':') + 1:].strip()
    except:
        return 'No Data Found'

def get_fifty_two_week_high_low(ticker=''):
    """
    This function gets the fifty-two week high and lows for the given ticker symbol. It performs a request to the
    http://www.barchart.com/ url and parses the response to find the fifty-two week high and low.
    :param ticker: The stock symbol/ticker to use for the lookup
    :return: String containing the fifty two week high and low
    """
    try:
        earnings_url = 'http://www.barchart.com/quotes/stocks/' + ticker.upper()
        request = requests.get(earnings_url)
        soup = bs4.BeautifulSoup(request.text, 'html.parser')
        found_value = soup.find(text=re.compile('52Wk'))
        high_text = found_value.findPrevious('td').text.strip()
        low_text = found_value.findNext('td').text.strip()
        return high_text[0:high_text.index('\t')]+'H ' + low_text[0:low_text.index('\t')]+'L'
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
        key_stats_url = 'http://finance.yahoo.com/q/ks?s=' + ticker.lower() + '+Key+Statistics'
        request = requests.get(key_stats_url)
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
        rsi_url = 'http://charting.nasdaq.com/ext/charts.dll?2-1-14-0-0-512-03NA000000' + ticker.upper() \
                  + '-&SF:1|27-SH:27=10-BG=FFFFFF-BT=0-WD=635-HT=395--XTBL-'
        request = requests.get(rsi_url)
        soup = bs4.BeautifulSoup(request.text, 'html.parser')
        return soup.find_all('td', class_="DrillDownData")[1].text
    except:
        return 'No Data Found'


def get_stocks(tickers=None):
    """
    This function creates a list of Stock objects.
    """
    stocks = []
    for ticker in tickers:
        stocks.append(
            Stock(price=Suds_Client.quote_request(ticker=ticker), earnings_date=get_earnings_date(ticker=ticker),
                  ticker=ticker, peg_ratio=get_peg_ratio(ticker), rsi=get_rsi(ticker=ticker),
                  fifty_two=get_fifty_two_week_high_low(ticker=ticker)))
    return stocks


class Stock:
    """
    Defines a stock.
    """
    def __init__(self, price=0, earnings_date='', ticker='', peg_ratio='', rsi='', fifty_two=''):
        self.price = price
        self.earnings_date = earnings_date
        self.ticker = ticker
        self.peg_ratio = peg_ratio
        self.rsi = rsi
        self.fifty_two = fifty_two

if __name__ == "__main__":
    # If the script is being invoked directly, run the main method.
    main()