# TakeStock
This project provides support for the emailing of Stock reports.

It scrapes the NASDAQ site for earnings dates and gets stock prices using a web service.

Earning dates within a week are bolded and the font size increased. 

It gets 52 week highs and lows from http://www.barchart.com/.

It gets peg ratios from http://finance.yahoo.com.

It gets RSIs and earnings dates from http://www.nasdaq.com/.

This project may be run as either a CLI or GUI app.

If ran as GUI, GUI.py is the main script. 

If run as CLI, TakeStock_Reporter.py is the main script. Run this script to see all the commands.

This project has suds-jurko and BeautifulSoup4 as requirements.

![Alt text](/screenshot_gui.png?raw=true "TakeStock in GUI action")
![Alt text](/screenshot.png?raw=true "TakeStock in CLI action")
