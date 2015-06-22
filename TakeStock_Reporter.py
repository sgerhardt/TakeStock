__author__ = 'Sean Gerhardt'

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import getopt
import sys

import QuarterlyReport


def main():
    global email_sender
    global email_receiver
    global email_cred
    global tickers
    global smtp
    global port
    global verbose

    if not len(sys.argv[1:]):
        usage()

    # Read the commandline options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "he:r:p:t:s:o:v", ['help', 'email_sender=', 'email_receiver=',
                                                                    'password=', 'tickers=' 'smtp=', 'port=',
                                                                    'verbose'])
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
        else:
            assert False, "Unhandled Option"

    # Send an email report for the stocks listed in the tickers list.
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
            -v --verbose            - print results to cmd line
            \n\n
            Examples:
            TakeStock.py -e sender_email@your_domain.com -p sender_password -r email_recipient@recipient_domain.com -s smtp.gmail.com -p 587 -t 'AAPL,MSFT,AMT' -v
            TakeStock.py -v -t 'AAPL,AMZN,MSFT,AMT'
            """)
    sys.exit(0)


def send_email(tickers=None, to_addr='your_email_here@your_domain.com'):
    """
    Given a list of stock tickers, this will send an email report formatted as an HTML table to the designated address.
    """

    # Create a message summarizing the best deals.
    message = MIMEMultipart('alternative')

    message['Subject'] = 'TakeStock Report'
    message['From'] = email_sender

    html = """\
      <table border=1>
      <thead><tr><td>Stock Symbol</td><td>Earnings Date</td><td>Price</td></tr></thead>
      <tbody>
    """

    stocks = QuarterlyReport.get_stocks(tickers)

    if verbose:
        print('Ticker   Earnings Date   Price')
        for stock in stocks:
            print(stock.ticker + ' ' + stock.earnings_date + ' ' + str(stock.price))

    for stock in stocks:
        html += "<tr>" + "<td>" + stock.ticker + "</td>" + "<td>" + stock.earnings_date + "<td/>" + "<td>" + \
                str(stock.price) + "</td>"

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


if __name__ == "__main__":
    # If the script is being invoked directly, run the main method.
    main()