import csv, re, _thread, urllib.request
from datetime import datetime

sp500PE = 0

def getStocks(symbol):

    # Iterate through rows, extracting stock symbols
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

            # Write symbol and ratios to file if company appears under-valued
            if earningsQuarterlyGrowth > 50 and forwardPE <= sp500PE:
                print(symbol + " is a match")
                file = open("output.csv", "a")
                file.write(symbol + "," + str(earningsQuarterlyGrowth) + "," + str(forwardPE) + "\n")
                file.close()

    except:
        print("Symbol " + symbol + " not found")


with open('buyOrStrongBuy.csv', newline='') as csvfile:
    # Setup output CSV file, add column names
    file = open("output.csv", "a")
    file.write("Symbol,earningsQuarterlyGrowth,ForwardPE\n")
    file.close()

    # Get estimated S&P 500 PE ratio
    sp500url = 'http://www.multpl.com/'

    with urllib.request.urlopen(sp500url) as response:
        html = str(response.read())
        sp500PE = float(
            str(re.search('\d+\.\d+', str(re.search("\"endLabel\":\[\"(.*?)\"", str(html)).group())).group()))
        response.close()


    # Open CSV file with Buy or Strong Buy ratings, skip header row
    stockNameReader = csv.reader(csvfile)
    next(stockNameReader)
    print("sp500PE is " + str(sp500PE))
    for row in stockNameReader:
        symbol = row[0].replace(" ", "")
        print("checking " + symbol)

        # Start threads for each stock symbol
        try:
            _thread.start_new_thread(getStocks,(symbol, ))
        except:
           print ("Error: unable to start thread " + symbol)
