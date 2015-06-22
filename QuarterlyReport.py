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
    earnings_url = 'http://www.nasdaq.com/earnings/report/' + ticker.lower()
    request = requests.get(earnings_url)
    soup = bs4.BeautifulSoup(request.text)
    tag = soup.find(text=re.compile('Earnings announcement*'))
    return tag[tag.index(':') + 1:].strip()


def get_stocks(tickers=None):
    """
    This function creates a list of Stock objects.
    """
    stocks = []
    for ticker in tickers:
        stocks.append(
            Stock(price=Suds_Client.quote_request(ticker=ticker), earnings_date=get_earnings_date(ticker=ticker),
                  ticker=ticker))
    return stocks


class Stock:
    """
    Defines a stock.
    """
    def __init__(self, price=0, earnings_date='', ticker=''):
        self.price = price
        self.earnings_date = earnings_date
        self.ticker = ticker


if __name__ == "__main__":
    # If the script is being invoked directly, run the main method.
    main()