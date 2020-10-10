# TakeStock
![Build Status](https://travis-ci.org/sgerhardt/TakeStock.svg?branch=master)
[![codecov.io](https://codecov.io/github/sgerhardt/TakeStock/coverage.svg?branch=master)](httpss://codecov.io/github/sgerhardt/TakeStock?branch=master)

This project scrapes multiple sites for stock data.

It scrapes the NASDAQ site for earnings dates and gets stock prices using a web service.

Earning dates within a week are bolded and the font size increased. 

It gets 52 week highs and lows, pe and peg ratios from https://finance.yahoo.com.

It gets RSIs from https://www.nasdaq.com/.

It gets earnings dates from https://https://www.zacks.com/

This project may be run as either a CLI or GUI app.

launch_TakeStock.py is the main script. If given arguments, it will run from CLI.

This CLI provides support for the emailing of Stock reports.

![Alt text](/screenshot_gui.png?raw=true "TakeStock in GUI action")
![Alt text](/screenshot.png?raw=true "TakeStock in CLI action")
