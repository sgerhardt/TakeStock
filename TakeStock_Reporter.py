__author__ = 'Sean Gerhardt'

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import QuarterlyReport


def main():
    #Send an email report for the stocks listed in the tickers list.
    send_email(tickers=['AAPL', 'DIS', 'FFIV', 'AMT', 'COO', 'JPM', 'CAT', 'JCP', 'AMZN'],
               to_addr='your_email_here@your_domain.com')


def send_email(tickers=None, to_addr='your_email_here@your_domain.com'):
    """
    Given a list of stock tickers, this will send an email report formatted as an HTML table to the designated address.
    """
    from_addr = 'TakeStock'

    # Create a message summarizing the best deals.
    message = MIMEMultipart('alternative')

    message['Subject'] = 'TakeStock Report'
    message['From'] = 'your_email_here@your_domain.com'

    html = """\
      <table border=1>
      <thead><tr><td>Stock Symbol</td><td>Earnings Date</td><td>Price</td></tr></thead>
      <tbody>
    """

    stocks = QuarterlyReport.get_stocks(tickers)
    for stock in stocks:
        html += "<tr>" + "<td>" + stock.ticker + "</td>" + "<td>" + stock.earnings_date + "<td/>" + "<td>" + \
                str(stock.price) + "</td>"

    html += '</tbody></table>'

    text = MIMEText(html, 'html')
    message.attach(text)
    # Email the deals.
    message['To'] = to_addr
    server = smtplib.SMTP('your_smtp_server_here')#E.g. smtp.gmail.com:587
    #server.ehlo()
    server.starttls()
    server.login("your_email_address_here", "your_email_pw_here")
    server.sendmail(from_addr, to_addr, message.as_string())
    server.quit()


if __name__ == "__main__":
    # If the script is being invoked directly, run the main method.
    main()