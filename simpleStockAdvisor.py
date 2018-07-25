import urllib.request
import re
import csv
from datetime import datetime

with open('buyOrStrongBuy.csv', newline='') as csvfile:

    # Setup output CSV file, add column names
    file = open("output.csv", "a")
    file.write("Name,Symbol,closing,earningsQuarterlyGrowth,ForwardPE\n")
    file.close()


    # Get estimated S&P 500 PE ratio
    sp500url = 'http://www.multpl.com/'
    sp500PE = 0
    with urllib.request.urlopen(sp500url) as response:
        html = str(response.read())
        sp500PE = float(
            str(re.search('\d+\.\d+', str(re.search("\"endLabel\":\[\"(.*?)\"", str(html)).group())).group()))
        response.close()

    # Open CSV file with Buy or Strong Buy ratings, skip header row
    stockNameReader = csv.reader(csvfile)
    next(stockNameReader)

    # Iterate through rows, extracting stock symbols
    for row in stockNameReader:
        symbol = row[0].replace(" ", "")
        print("checking " + symbol)

        try:
            # Build Yahoo Finance URL using each symbol
            url = 'https://finance.yahoo.com/quote/' + symbol + '/key-statistics?p=' + symbol

            # Search page's HTML source for earnings quarterly growth and forward PE
            with urllib.request.urlopen(url) as response:
                html = str(response.read())
                earningsQuarterlyGrowth = 100 * \
                    float(re.search(
                        '\d+\.\d+', str(re.search('earningsQuarterlyGrowth(.*?)"\d+\.\d+(.*?)\d+\.\d+', html))).group())
                forwardPE = float(
                    re.search('\d+\.\d+', str(re.search('forwardPE(.*?)\d+\.\d+', html).group())).group())
                name = str(re.search('\|(.*?)Stock',str(re.search('<title>(.*?)</title>',html).group())).group())[2:]
                name = name[:name.index(" Stock")]
                # Write symbol, closing price, and ratios to file if company appears under-valued
                if earningsQuarterlyGrowth > 50 and forwardPE <= sp500PE:
                    print(symbol + " is a match")
                    file = open("output.csv", "a")
                    file.write(name + "," + symbol + "," + str(row[1]) + "," + str(earningsQuarterlyGrowth) + "," + str(forwardPE) + "\n")
                    file.close()

        except:
            print("Symbol " + symbol + " not found")

    file.close()
