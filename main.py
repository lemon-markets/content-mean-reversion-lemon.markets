from lemon import api
import time
import statistics
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

from models import TradingVenue

load_dotenv()
client = api.create(
    trading_api_token=os.environ.get('TRADING_API_KEY'),
    market_data_api_token=os.environ.get('DATA_API_KEY'),
    env='paper'
)
print(client)


def mean_reversion_decision(isin: str, x1: str = "d1"):
    """
    :param isin: pass the isin of your instrument
    :param x1: pass what type of data you want to retrieve (m1, h1 or d1)
    :return: returns whether you should buy (True) or sell (False), depending on MR criteria
    """
    from_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    market_data = client.market_data.ohlc.get(
        isin=isin,
        from_=from_date,
        period=x1
    )
    print(market_data)

    d1_prices = market_data.results
    prices_close = [x.c for x in d1_prices]  # you can obviously change that to low, close or open
    mean_price = statistics.mean(prices_close)
    print(f'Mean Price: {mean_price}')
    latest_close_price = client.market_data.ohlc.get(
        isin=isin,
        from_='latest',
        period="m1"
    ).results[0].c
    print(f'Latest Close Price: {latest_close_price}')
    if latest_close_price < mean_price:
        return True
    return False


def check_if_buy(isin: str, x1: str = "d1"):
    """
    :param isin: pass the isin of the stock you are interested in
    :param x1:  pass the market data format you are interested in (m1, h1, or d1)
    """
    load_dotenv()

    # check for MR decision
    if mean_reversion_decision(
            isin=isin,
            x1=x1
    ):
        # create a buy order if True is returned by MR decision function
        try:
            print('buy')
            placed_order = client.trading.orders.create(
                isin=isin,
                expires_at="p7d",
                side="buy",
                quantity=1,
                venue=os.getenv("MIC"),
            )
            order_id = placed_order.results.id
            # subsequently activate the order
            activated_order = client.trading.orders.activate(order_id)
            print(activated_order)
            time.sleep(14400)  # check back in 4 hours
        except Exception as e:
            print(f'1{e}')
            time.sleep(60)
    else:
        try:
            # create a sell order if mean reversion decision returns False
            print('sell')
            placed_order = client.trading.orders.create(
                isin=isin,
                expires_at="p7d",
                side="sell",
                quantity=1,
                venue=os.getenv("MIC"),
            )
            # if position in portfolio, activate order
            if placed_order is not None:
                order_id = placed_order.results.id
                activated_order = client.trading.orders.activate(order_id)
                print(activated_order)
            else:
                print("You do not have sufficient holdings to place this order.")
            time.sleep(14400)  # check back in 4 hours
        except Exception as e:
            print(f'2{e}')
            time.sleep(60)


def mean_reversion():
    """
    main function to be executed
    """
    while True:
        if client.market_data.venues.get(os.getenv('MIC')).results[0].is_open:
            # make buy or sell decision
            check_if_buy(
                isin="DE0007664039",  # this is Volkswagen, but you can obviously use any ISIN you like :)
                x1="d1"
            )
        else:
            # sleep until market reopens in case it is closed
            time.sleep(TradingVenue.seconds_till_tv_opens())


if __name__ == '__main__':
    mean_reversion()
