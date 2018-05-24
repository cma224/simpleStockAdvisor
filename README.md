# simpleStockAdvisor

This tool is a simple Python-based script that attempts to find companies that appear undervalued using Yahoo Finance and a CSV generated with TradingView's screening tool.

A CSV was generated using TradingView's screening tool to find stock symbols with "Buy" or "Strong Buy" ratings as of May 23, 2018. This script retrieves each symbol, builds the appropriate URL, and extracts the appropriate statistics on Yahoo Finance. The stocks that match the criteria below are then placed in another CSV file.

A company is "under-valued" if:

(1) Its forward PE ratio is less than S&P500 PE ratio

(2) Its quarterly earnings growth exceeds 25%

Don't know what a forward PE ratio is? 
[See here](https://ycharts.com/glossary/terms/forward_pe_ratio)

Don't know what quarterly earnings growth is?
[See here](http://www.investorguide.com/definition/quarterly-earnings-growth.html)
