"""Unit tests for the Super Simple Stock Market Application."""

import unittest
from time import time


class TestSystem(unittest.TestCase):

    def setUp(self):

        # setup stocks data
        self.tea_stock = Stock(stock_symbol="TEA", stock_type="Common",
                               last_dividend=0, par_value=100)
        self.pop_stock = Stock(stock_symbol="POP", stock_type="Common",
                               last_dividend=8, par_value=100)
        self.ale_stock = Stock(stock_symbol="ALE", stock_type="Common",
                               last_dividend=23, par_value=60)
        self.gin_stock = Stock(stock_symbol="GIN", stock_type="Preferred",
                               last_dividend=8, fixed_dividend=0.02,
                               par_value=100)
        self.joe_stock = Stock(stock_symbol="JOE", stock_type="Common",
                               last_dividend=13, par_value=250)

        self.stocks = [self.tea_stock, self.pop_stock, self.ale_stock,
                       self.gin_stock, self.joe_stock]

        # Generate trades

        # TEA trades
        self.tea_trade1 = self.tea_stock.generate_trade(
                              trade_time=time() - 890, quantity_stocks=50,
                              indicator="Buy", price=500)

        self.tea_trade2 = self.tea_stock.generate_trade(
                              trade_time=time() - 420, quantity_stocks=40,
                              indicator="Sell", price=30)
        self.tea_trade3 = self.tea_stock.generate_trade(
                              trade_time=time() - 210, quantity_stocks=10,
                              indicator="Buy", price=100)

        # GIN trades
        self.gin_trade1 = self.gin_stock.generate_trade(
                              trade_time=time() - 125, quantity_stocks=25,
                              indicator="Sell", price=400)
        self.gin_trade2 = self.gin_stock.generate_trade(
                              trade_time=time() - 90, quantity_stocks=70,
                              indicator="Buy", price=300)
        self.gin_trade3 = self.gin_stock.generate_trade(
                              quantity_stocks=260, indicator="Sell", price=30)

        # ALE trades
        self.ale_trade1 = self.ale_stock.generate_trade(
                              quantity_stocks=25, indicator="Buy", price=500)
        self.ale_trade2 = self.ale_stock.generate_trade(
                              quantity_stocks=30, indicator="Buy", price=490)
        self.ale_trade3 = self.ale_stock.generate_trade(
                              quantity_stocks=70, indicator="Buy", price=480)

        self.first_trades = [self.tea_trade1, self.tea_trade2, self.tea_trade3,
                             self.gin_trade1, self.gin_trade2, self.gin_trade3]

        self.later_trades = [self.ale_trade1, self.ale_trade2, self.ale_trade3]

        # record trades in market
        self.market1, self.market2 = StockMarket(), StockMarket()

        self.market1.record_trades(self.first_trades)
        self.market2.record_trades(self.first_trades + self.later_trades)


class TestStock(TestSystem):

    def test_dividend_yield(self):
        self.assertEqual(self.tea_stock.dividend_yield(price=500), 0)
        self.assertEqual(self.pop_stock.dividend_yield(price=500), 0.016)
        self.assertEqual(self.ale_stock.dividend_yield(price=500), 0.046)
        self.assertEqual(self.gin_stock.dividend_yield(price=500), 0.004)
        self.assertEqual(self.joe_stock.dividend_yield(price=500), 0.026)

    def test_calc_pe_ratio(self):
        self.assertEqual(self.tea_stock.calc_pe_ratio(price=500), float("0"))
        self.assertEqual(self.pop_stock.calc_pe_ratio(price=500), 62.5)
        self.assertEqual(round(self.ale_stock.calc_pe_ratio(price=500), 3),
                         21.739)
        self.assertEqual(self.gin_stock.calc_pe_ratio(price=500), 62.5)
        self.assertEqual(round(self.joe_stock.calc_pe_ratio(price=500), 3),
                         38.462)


class TestMarket(TestSystem):

    def test_record_trade(self):
        for trade in self.market1.trades:
            self.assertEqual(self.market1.trades, self.first_trades)
        self.assertEqual(self.market1.stocks, {self.tea_stock, self.gin_stock})

    def test_volume_weighted_stock_price(self):
        # ale has not been traded in market1 yet
        self.assertEqual(
            self.market1.volume_weighted_stock_price(self.ale_stock), 0
        )
        # but it has in market 2
        self.assertEqual(
            self.market2.volume_weighted_stock_price(self.ale_stock), 486.4
        )
        # all gin trades have taken place in the last 15 minutes
        self.assertEqual(
            round(self.market1.volume_weighted_stock_price(self.gin_stock), 3),
            109.296
        )
        # nothing should change in the other market
        self.assertEqual(
            round(self.market2.volume_weighted_stock_price(self.gin_stock), 3),
            109.296
        )
        # the first tea trade took place more than 15 minutes ago
        self.assertEqual(
            self.market1.volume_weighted_stock_price(self.tea_stock), 272
        )
        # again nothing should change in the other market
        self.assertEqual(
            self.market2.volume_weighted_stock_price(self.tea_stock), 272
        )

    def test_all_share_index(self):
        self.assertEqual(round(self.market1.all_share_index, 3), 172.419)
        self.assertEqual(round(self.market2.all_share_index, 3), 243.625)

if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path
        sys.path.append( path.dirname( path.dirname( path.abspath(__file__))))
        from src.app import Stock, StockMarket
    else:
        from .src.app import Stock, StockMarket
    unittest.main()
