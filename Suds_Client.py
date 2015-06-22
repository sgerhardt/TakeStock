__author__ = 'Sean Gerhardt'

from suds.client import Client
import bs4


def main():
    quote_request(ticker='')


def quote_request(wsdl='http://www.webservicex.net/stockquote.asmx?WSDL', ticker=''):
    client = Client(wsdl)

    request_data = client.factory.create('GetQuote')
    request_data.symbol = ticker

    result = client.service.GetQuote(request_data)

    soup = bs4.BeautifulSoup(result)

    return soup.last.text

if __name__ == "__main__":
    # If the script is being invoked directly, run the main method.
    main()