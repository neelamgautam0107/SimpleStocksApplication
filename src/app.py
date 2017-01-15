"""
Super simple stocks application.
Module name: api.py
Description: Contain classes used in the Super Simple Stock Application.
Author: Neelam Gautam
"""

import sys
import logging
from datetime import datetime
from time import time
from operator import mul

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)

VALID_INDICATORS = ['Buy', 'Sell']

# no of seconds for calculating historical vol weight stock price
HISTORICAL_TRADES_TIME = 900

class Stock(object):
    """ Class to record and represent an individual stock."""

    def __init__(self, stock_symbol, stock_type, last_dividend,
                 par_value, fixed_dividend=None):
        """
        Initialize Stock

        :param: stock_symbol: <str> stock's symbol 3 letters abbreviation
        :param: stock_type: <str> "Common" or "Preferred"
        :param: last_dividend: <int> last dividend value
        :param: par_value: <int> par value of stock
        :param: fixed_dividend: If stock is preferred, then fixed dividend
                of stock.

        :sample usage:
            Stock(stock_symbol="TEA", stock_type="Common",
                  last_dividend=0, par_value=100)
        """

        self.stock_symbol = stock_symbol
        self.stock_type = stock_type
        self.last_dividend = last_dividend
        self.par_value = par_value
        if self.stock_type == "Preferred":
            self.fixed_dividend = fixed_dividend

    def __str__(self):
        """Return the stock symbol if we print the object."""
        
        logger.info("Stock is:")
        return self.stock_symbol

    def dividend_yield(self, price):
        """Method used to calculate dividend yield of the stock for given price.

        :param:price: <int> of the stock

        :return: dividend yield (in pences).
        """

        # validate price
        if not price or price<0:
            logger.info("dividend_yield: Please provide valid price.")
            return float(0)

        if self.stock_type == "Common":
            return self.last_dividend / float(price)
        elif self.stock_type == "Preferred":
            return self.fixed_dividend * self.par_value / float(price)

    def calc_pe_ratio(self, price):
        """ Calculate P/E ratio of stock given its price.
 
        :param: price: <int> of the stock

        formula:
            price/dividend

        :return: The P/E ratio (in pences).
        """

        # validate price
        if not price or price<0:
            logger.info("calc_pe_ratio: Please provide valid price.")
            return float(0)

        if not self.last_dividend:
            return float(0)
        else:
            return float(price) / self.last_dividend

    def generate_trade(self, quantity_stocks, indicator, price,
                       trade_time=time()):
        """Generate a trade object.

        :param: quantity_stocks <int>: The quantity of stock buying/selling.
        :param: indicator <str>: "Buy" or "Sell".
        :param: price <int>: The price of the stock.
        :param: trade_time <int>: A time in seconds, defaults to current time.

        :return: a Trade instance/object or None.
        """
        
        # validate price
        if not price or price<0:
            logger.info("generate_trade: Please provide valid price.")
            return False

        # validate indicator
        if not indicator or (indicator not in VALID_INDICATORS):
            logger.info("generate_trade: Please provide valid indicator.\
                        Valid values are: 'Buy' or 'Sell'")
            return False
        
        # validate quantity_stocks
        if not quantity_stocks or quantity_stocks<0:
            logger.info("generate_trade: Please provide valid quantity of\
                        stocks i.e. a positive integer.")
            return False

        return Trade(self, quantity_stocks, indicator, price, trade_time)

class Trade(object):
    """Class to represent an individual trade involving a stock."""

    def __init__(self, stock, quantity_stocks, indicator, price, trade_time):
        """
        Initialize Trade

        :param: stock <Stock>: The stock involved in the trade
        :param: quantity_stocks <int>: The quantity of stock traded.
        :param: indicator <str>: "Buy" or "Sell".
        :param: price <int>: The price of the stock.
        :param: trade_time <int>: A time in seconds.
        """

        self.stock = stock
        self.trade_time = trade_time
        self.timestamp = datetime.fromtimestamp(trade_time).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        self.quantity_stocks = quantity_stocks
        self.indicator = indicator
        self.price = price

    def __str__(self):
        """Return string representing the recorded trade.

           e.g. "2017-01-12 10:40:55 Sell 30 GIN at 1000"
        """
        logger.info("Trade:")
        return "{} {} {} {} at {}".format(self.timestamp, self.indicator,
                                          self.quantity_stocks,
                                          self.stock.stock_symbol,
                                          self.price)


class StockMarket(object):
    """Represent a stock market as a sequence of trades."""

    def __init__(self):
        """
        Initialize Market
        
        :param: trades <List[trades]>: A list of trade objects recorded in the
            stock market.
        :param: stocks <Set[stocks]>: A set of stocks involved in a trade
            recorded in the stock market.
        """
        self.trades = []
        self.stocks = set()

    def __str__(self):
        """Returns/prints a list of historical stock market trades."""

        if self.trades:
            logger.info("Printing Market Trades:")
            return "\n".join(str(trade) for trade in self.trades)
        else:
            logger.info("No trades recorded in stock market as of now.")
            return None

    def record_trades(self, trades):
        """Records a sequence of trades into the stock market.

        :param: trades <List[Trade]>: A sequence of Trade objects.
        """

        for trade in trades:
            self.trades.append(trade)
            if trade.stock not in self.stocks:
                self.stocks.add(trade.stock)

    def volume_weighted_stock_price(self, stock):
        """Returns the volume weighted stock price of the given stock.

        :param: stock <Stock>: Stock instance.

        Returns:
            If the stock has been seen in the market, return the Volume
            Weighted Stock Price as in Table 2. Otherwise, return 0 (float).
        """

        if stock not in self.stocks:
            return 0

        # trades in last 15 mins
        recent_trades = [trade for trade in self.trades if
                         time() - trade.trade_time <= HISTORICAL_TRADES_TIME and
                         trade.stock == stock]
        numerator = sum(trade.price * trade.quantity_stocks
                        for trade in recent_trades)
        denominator = sum(trade.quantity_stocks for trade in recent_trades)
        return float(numerator) / denominator

    @property
    def all_share_index(self):
        """ Calculate GBCE All Share Index of the market using
        Geometric mean.

        returns: float all share index
        """

        number_of_stocks = len(self.stocks)
        product = reduce(mul,
                         (self.volume_weighted_stock_price(stock) for stock in
                          self.stocks))
        return product ** (1 / float(number_of_stocks))

