# SimpleStocksApplication
Super simple stocks is an application to manage trades on a set of stocks in the market.

## Problem Statement

### 1. Assignment Description

##### Requirements

1.	Provide working source code that will:

    a.	For a given stock:
    
        i.    Calculate the dividend yield.
        ii.   Calculate the P/E Ratio.
        iii.  Record a trade, with timestamp, quantity of shares, buy or sell indicator and price.
        iv.   Calculate Stock Price based on trades recorded in past 15 minutes.

    b.	Calculate the GBCE All Share Index using the geometric mean of prices for all stocks

##### Constraints & Notes

1.	Written in one of these languages:
    
    * Java, C#, C++, Python.
    
2.	No database or GUI is required, all data need only be held in memory.

3.	Formulas and data provided are simplified representations for the purpose of this exercise.

##### Global Beverage Corporation Exchange

Stock Symbol  | Type | Last Dividend | Fixed Dividend | Par Value
------------- | ---- | ------------: | :------------: | --------: 
TEA           | Common    | 0  |    | 100
POP           | Common    | 8  |    | 100
ALE           | Common    | 23 |    | 60
GIN           | Preferred | 8  | 2% | 100
JOE           | Common    | 13 |    | 250




## Prerequisite

You should have installed
- Python 2.7 +  (tested on 2.7)
- Tested on Ubuntu / Microsoft windows

## Installation

### Application
To install application with all dependencies:

```
pip install git+git://github.com/neelamgautam0107/StocksApp.git
```

### Design Details:
The code design consists of three main clases:
 - Stock: The class contains methods to initialize stocks. i.e. stocks details to generate trades.
 - Trade: This class contains method to generate trades on the specified stocks.
 - StockMarket: This class represents the stocks market. It has additional methods to record trades, calculate all share index and also method to calculate volume weight stock prices for the trades happened in last 15 minutes.
 
 The code for above 3 classes can be found in src/app.py

### In this implementation we are modeling stock market as sequence of trade objects. Then we have defined different methods to calculate the trades and market state as specified in the problem description above.

The example of the using the code to record trades/market are detailed under tests/test_app.py
The test suite contains details on how to use this application. The test suit has usage details on all of the calculation method as specified in the above problem description section. The usage contains details on:

- For a given stock, 
    - Calculate the dividend yield
    - Calculate the P/E Ratio
    - Record a trade, with timestamp, quantity of shares, buy or sell indicator and price
    - Calculate Stock Price based on trades recorded in past 15 minutes
- Calculate the GBCE All Share Index using the geometric mean of prices for all stocks

### How to Run this application:
Simply go to shell and run following command while you are under tests directory:

```
/StocksApp/tests$ python test_app.py
```

The output should show as 
```
.....
----------------------------------------------------------------------
Ran 5 tests in 0.002s

OK
```
Which means all of the test cases have passed.

## Author
Neelam Gautam
