# Imports:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

import time
import requests
import os

# variables------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
length = -1
stocks = {}

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Functions:

def ms(inputt):
    file = open("Correlations", "w")
    for item in inputt:
        file.write("%s\n" % item)
    file.close()

def getlist(file):
    x = []
    for line in open(file,"r"):
        y = line.split(',')
        x.append((y[0]).strip('""'))
    x.remove('Symbol')
    #print(x)
    return x

def make_list(values): #makes dictionary into a list
    x = []
    if values == None:
        return None
    for key, value in values.items():
        temp = float(value)
        x.append(temp)
   # print(len(x))
    return x

def compare(x): # uses a built in sorted function to sort lists. Compare is the key of the sorted function
    return x[1]

def download_file(symbol,URL): # dowloads file as NAME.csv
    file = open("11111/"+symbol, "w")
    r = requests.get(URL)
    if r.status_code == 404:
        return 
    file.write(r.text)
    file.close()
    with open (("11111/"+symbol), 'r') as nfile:
        data = nfile.readlines()
        #print(data)
        return data

def dpcreate(data): # creates a dictionary with dates as keys and prices as values
    global length
    returning = {}
    x = []
    for line in data:
        x.append(line.strip().split(","))
    x.pop(0)
    for countera in range(0,len(x)):
        returning[x[countera][0]] = x[countera][6]
    #print(len(x))
    if length == -1:
        length = len(returning)
   # print(len(returning))
    #print(len(returning))
    if len(returning) != length:
        #print('Unequal lengths')
        #print('x')
        return None
    return returning

def find_correlation_value(x,y,delay): # finds correlation
    global length
    length -= 1
    #print('before' + str(len(x))  +  str(len(y)))
    #print(len(x))
    #print(len(y))
    if delay == 1:
        x.pop(0)
        y.pop(length)
    if delay == 0:
        x.pop(0)
        y.pop(0)
    #print(len(x))
    #print(len(y))
    number_points = len(x)
    x_sum, y_sum, correlation = 0, 0, 0
    bottom, b_sum, a_sum = 0, 0, 0
    top, xsquare, ysquare = 0, 0, 0
    for counter in range(0,number_points):
        a_sum = a_sum + x[counter]*y[counter]
        x_sum += x[counter]
        y_sum += y[counter]
        xsquare = xsquare + x[counter]**2
        ysquare = ysquare + y[counter]**2
    b_sum = x_sum*y_sum
    a_sum = a_sum*number_points
    top = a_sum-b_sum
    bottom = ((number_points*xsquare-x_sum**2)*(number_points*ysquare-y_sum**2))**.5
    correlation = top/bottom

    return correlation
'''
def createURL(symbol,dend,mend,yend,frequ,mart,dart,yart): # creates a url to dowload using parameters 
    return 'http://real-chart.finance.yahoo.com/table.csv?s='+symbol+'&d='+mend+'&e='+dend+'&f='+yend+'&g='+frequ+'&a='+mart+'&b='+dart+'&c='+yart+'&ignore=.csv'
'''
def createURL(symbols,mart,dart,yart,freq,mend,dend,yend):
    #print('http://chart.finance.yahoo.com/table.csv?s='+symbols+'&a='+mart+'&b='+dart+'&c='+yart+'&d='+mend+'&e='+dend+'&f='+yend+'&g='+freq+'&ignore=.csv')
    return 'http://chart.finance.yahoo.com/table.csv?s='+symbols+'&a='+mart+'&b='+dart+'&c='+yart+'&d='+mend+'&e='+dend+'&f='+yend+'&g='+freq+'&ignore=.csv'

def download(symbols,mart,dart,yart,frequ,mend,dend,yend,delay):
    global stocks
    dictionary = {}
    for counter in range(0,len(symbols)): # Downloads every stock file and sets stock ticker to a dictionary
        URL = createURL(symbols[counter],mart,dart,yart,frequ,mend,dend,yend)
 #       print(URL)
        fileData = download_file(symbols[counter],URL)
        #print(fileData)
        if fileData == None: # Filters out 404 responses
            #print('404')
            continue
        if counter == 1800:
            print('Sleeping')
            time.sleep(3600)
            print('Finished Sleeping')
        dictionary = dpcreate(fileData)
        stocks[symbols[counter]] = make_list(dictionary)
    return

     
def analysis(symbols,mart,dart,yart,frequ,mend,dend,yend,delay): # is the driving function, performs all the other functions
    global stocks
    values = {}
    download(symbols,mart,dart,yart,frequ,mend,dend,yend,delay) #downloads files with for loop
    for countera in range(0, len(symbols)):
        for counterb in range(0, len(symbols)):
            if countera == counterb:
                continue
            stock1_name = symbols[countera]
            stock2_name = symbols[counterb]
            #nonref[stock1, stock2, delay] = find_correlation_value(stocks[stock1_name], stocks[stock2_name],delay)
            #nonref[stock1, stock2, delay] = find_correlation_value(stocks[stock1_name], stocks[stock2_name],0)
            if stock2_name not in stocks: #not all stocks are in symbols
                continue 
            if stock1_name not in stocks:
                continue
            
            #print(len(stocks[stock1_name]))
            #print(len(stocks[stock1_name]))
            #print(stocks)
            with_in = find_correlation_value((stocks[stock1_name])[:], (stocks[stock2_name])[:],delay)
            with_out = find_correlation_value((stocks[stock1_name])[:],(stocks[stock2_name])[:],0)
            if (abs(with_in)-abs(with_out)) > .1:
                if abs(with_in) > .8:
                    values[stock1_name, stock2_name, delay] = with_in
                    values[stock1_name, stock2_name, 0] = with_out
 #                   values[stock1_name, stock2_name, delay] = find_correlation_value(stocks[stock1_name], stocks[stock2_name],delay)
#                    values[stock1_name, stock2_name, 0] = find_correlation_value(stocks[stock1_name], stocks[stock2_name],0)
    return stats(values)    

def stats(values): # sorts values within the list given(Stocks and their correlations with and without delaY)
    y = []
    #print(values)
    x = []
    z = []
    greatest = []
    for key, value in values.items():
        x.append([key, value])
    for key in values.keys():
        greatest.append(values[key])
    x = sorted(x, key = compare)
    x.reverse()
    ms(x)
    #print(x)
    print('complete')
    
    return x


#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Program:
#(symbol,mend,dend,yend,freq,mart,dart,yart) #0 index
time.sleep(3600)
analysis(getlist('Nasdaq.csv'),'0','1','2016','d','8','24','2016',1)
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
