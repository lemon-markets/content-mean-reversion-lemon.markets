from models.Order import Order
from models.Instruments import Instruments
from models.TradingVenue import TradingVenue
from models.Token import Token
import time
import statistics
import os
from dotenv import load_dotenv


def mean_reversion_decision(isin: str, x1: str = "d1"):
    """
    :param isin: pass the isin of your instrument
    :param x1: pass what type of data you want to retrieve (m1, h1 or d1)
    :return: returns whether you should buy (True) or sell (False), depending on MR criteria
    """
    market_data = Instruments(
        isin=isin,
        x1=x1
    ).get_market_data()
    d1_prices = market_data['results']
    prices_close = [x["c"] for x in d1_prices]  # you can obviously change that to low, close or open
    mean_price = statistics.mean(prices_close)
    print(f'Mean Price: {mean_price}')
    latest_close_price = Instruments(
        isin=isin,
        x1="m1"
    ).get_latest_market_data()
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
            placed_order = Order(
                isin=isin,
                expires_at="p7d",
                side="buy",
                quantity=1,
                venue=os.getenv("MIC"),
                space_id=os.getenv("SPACE_ID")

            ).place_order()
            order_uuid = placed_order.get('uuid')
            # subsequently activate the order
            activated_order = Order().activate_order(order_uuid)
            print(activated_order)
            time.sleep(14400)  # check back in 4 hours
        except Exception as e:
            print(f'1{e}')
            time.sleep(60)
    else:
        try:
            # create a sell order if mean reversion decision returns False
            print('sell')
            placed_order = Order(
                isin=isin,
                expires_at="p7d",
                side="sell",
                quantity=1,
                venue=os.getenv("MIC"),
                space_id=os.getenv("SPACE_ID")
            ).place_order()
            order_uuid = placed_order.get('uuid')
            activated_order = Order().activate_order(order_uuid)
            print(activated_order)
            time.sleep(14400)  # check back in 4 hours
        except Exception as e:
            print(f'2{e}')
            time.sleep(60)


def mean_reversion():
    """
    main function to be executed
    """
    while True:
        if TradingVenue().check_if_open():
            # make buy or sell decision
            check_if_buy(
                isin="US88160R1014",  # this is Tesla, but you can obviously use any ISIN you like :)
                x1="d1"
            )
        else:
            # sleep until market reopens in case it is closed
            time.sleep(TradingVenue().seconds_till_tv_opens())


if __name__ == '__main__':
    mean_reversion()
