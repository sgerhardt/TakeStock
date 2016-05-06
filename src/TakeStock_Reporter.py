__author__ = 'Sean Gerhardt'

import getopt
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src import QuarterlyReport


def main():
    global email_sender
    global email_receiver
    global email_cred
    global tickers
    global smtp
    global port
    global verbose
    global pe_ratio
    global peg_ratio
    global rsi
    global fifty_two

    email_sender = None
    email_receiver = None
    email_cred = None
    smtp = None
    port = None
    tickers = None
    verbose = False
    pe_ratio = False
    peg_ratio = False
    rsi = False
    fifty_two = False

    if not len(sys.argv[1:]):
        usage()

    # Read the commandline options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "he:r:p:t:s:o:vzgif", ['help', 'email_sender=', 'email_receiver=',
                                                                       'password=', 'tickers=' 'smtp=', 'port=',
                                                                       'verbose', 'pe', 'growth', 'rsi', 'fifty_two'])
    except getopt.GetoptError as err:
        print(str(err))
        usage()

    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
        elif o in ('-e', '--email_sender'):
            email_sender = a
        elif o in ('-r', '--email_receiver'):
            email_receiver = a
        elif o in ('-p', '--password'):
            email_cred = a
        elif o in ('-t', '--tickers'):
            tickers = a
        elif o in ('-s', '--smtp'):
            smtp = a
        elif o in ('-o', '--port'):
            port = a
        elif o in ('-v', '--verbose'):
            verbose = True
        elif o in ('-z', '--pe_ratio'):
            pe_ratio = True
        elif o in ('-g', '--peg_ratio'):
            peg_ratio = True
        elif o in ('-i', '--rsi'):
            rsi = True
        elif o in ('-f', '--fifty_two'):
            fifty_two = True
        else:
            assert False, "Unhandled Option"

    if verbose:
        get_results(tickers=tickers.replace("'", '').split(','))
    # Send an email report for the stocks listed in the tickers list.

    if email_receiver is not None:
        send_email(tickers=tickers.replace("'", '').split(','),
                   to_addr='your_email_here@your_domain.com')


def usage():
    print("""
            TakeStock Market Reporting Tool \n\n

            Usage: TakeStock.py -e email_address -p email_password -s smtp_server -p port -v verbose
            -e --email              - email address to send report
            -p --password           - password for email_address
            -s --smtp               - smtp server that sends the email report
            -t --port               - port for the smtp server
            -v --verbose            - print earnings date and price
            -o --pe_ratio           - print pe ratio
            -g --peg_ratio          - print peg ratio
            -r --rsi                - print relative strength indicator
            -f --fifty_two          - print fifty-two week high and low
            \n\n
            Examples:
            TakeStock.py -e sender_email@your_domain.com -p sender_password -r email_recipient@recipient_domain.com -s smtp.gmail.com -p 587 -t 'AAPL,MSFT,AMT' -v
            TakeStock.py -v -g -t 'AAPL,AMZN,MSFT,AMT'
            """)
    sys.exit(0)


def get_results(tickers=None):
    """
    Given a list of stock tickers, this print formatted results to the terminal.
    """
    if tickers == ['']:
        return

    stocks = QuarterlyReport.get_stocks(tickers)

    if verbose:
        string_header = '{:<10}'.format('Ticker') + '{:<17}'.format('Earnings Date')
        string_to_line = ''
        if peg_ratio:
            string_header += '{:<13}'.format('Peg Ratio')
        if pe_ratio:
            string_header += '{:<13}'.format('PE Ratio')
        if rsi:
            string_header += '{:<13}'.format('RSI')
        if fifty_two:
            string_header += '{:<20}'.format('52Wk H&L')
        string_header += '{:<12}'.format('Price')
        print(string_header)
        for stock in stocks:
            string_to_line = '{:<10}'.format(stock.ticker) + '{:<17}'.format(stock.earnings_date)
            if peg_ratio:
                string_to_line += '{:<13}'.format(str(stock.peg_ratio))
            if pe_ratio:
                string_to_line += '{:<13}'.format(str(stock.pe_ratio))
            if rsi:
                string_to_line += '{:<13}'.format(str(stock.rsi))
            if fifty_two:
                string_to_line += '{:<20}'.format(str(stock.fifty_two))
            string_to_line += '{:<12}'.format(str(stock.price))
            print(string_to_line)
    return stocks


def send_email(tickers=None, to_addr='your_email_here@your_domain.com'):
    """
    Given a list of stock tickers, this will send an email report formatted as an HTML table to the designated address.
    """

    stocks = QuarterlyReport.get_stocks(tickers)

    if ('email_sender' and 'email_cred' and 'email_receiver' and 'port' and 'smtp') in globals():
        # Create a message summarizing the best deals.
        message = MIMEMultipart('alternative')

        message['Subject'] = 'TakeStock Report'
        message['From'] = email_sender
        html = ''
        if peg_ratio:
            html = """\
            <table border=1>
            <thead><tr><td>Stock Symbol</td><td>Earnings Date</td><td>PEG Ratio</td><td>Price</td></tr></thead>
            <tbody>
            """
        else:
            html = """\
            <table border=1>
            <thead><tr><td>Stock Symbol</td><td>Earnings Date</td><td>Price</td></tr></thead>
            <tbody>
            """

        for stock in stocks:
            if peg_ratio:
                html += "<tr>" + "<td>" + stock.ticker + "</td>" + "<td>" + stock.earnings_date + "</td>" + \
                        "<td>" + str(stock.peg_ratio) + "</td>" + "<td>" + str(stock.price) + "</td></tr>"
            else:
                html += "<tr>" + "<td>" + stock.ticker + "</td>" + "<td>" + stock.earnings_date + "</td>" + "<td>" + \
                        str(stock.price) + "</td></tr>"

        html += '</tbody></table>'

        text = MIMEText(html, 'html')
        message.attach(text)
        # Email the deals.
        message['To'] = email_receiver
        server = smtplib.SMTP(smtp + ":" + port)
        # server.ehlo()
        server.starttls()
        server.login(email_sender, email_cred)
        server.sendmail(email_sender, email_receiver, message.as_string())
        server.quit()
        return html

if __name__ == "__main__":
    # If the script is being invoked directly, run the main method.
    main()
else:
    # Running from GUI or other context
    verbose = True
    rsi = True
    fifty_two = True
    pe_ratio = True
    peg_ratio = True
