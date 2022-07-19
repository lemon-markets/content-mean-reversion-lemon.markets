import os
import statistics
from datetime import datetime, timedelta

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from dotenv import load_dotenv
from lemon import api
from pytz import utc

load_dotenv()
# create your api client with separate trading and market data api tokens
client = api.create(
    trading_api_token=os.environ.get('PAPER_TRADING_API_KEY'),
    market_data_api_token=os.environ.get('DATA_API_KEY'),
    env='paper'
)


def simple_moving_average_calculator(isin, period, from_date, num_days=10):
    """
    :param isin: isin of stock/ETF you want to calculate the average for
    :param period: m1, h1, or d1 depending on the period you are calculating with
    :param num_days: number of days you wish to include in the average
    :param from_date: the date you want to calculate the SMA for
    :return: SMA as a number
    """
    prices_close = []
    while len(prices_close) < num_days:
        market_data = client.market_data.ohlc.get(
            isin=isin,
            from_=from_date.strftime('%Y-%m-%d'),
            to=from_date.strftime('%Y-%m-%d'),
            decimals=True,
            period=period,
            mic=os.getenv("MIC")
        )
        if len(market_data.results) != 0:  # make sure that we aren't counting weekends/holidays
            prices_close.append(market_data.results[0].c)
        from_date = (from_date - timedelta(days=1))
    return statistics.mean(prices_close)  # SMA calculation


def exponential_moving_average_calculator(isin, period, from_date, num_days=10):
    past_x_days = []
    while len(past_x_days) < num_days:  # make a list of the last ten days the market was open
        market_data = client.market_data.ohlc.get(
            isin=isin,
            from_=from_date.strftime('%Y-%m-%d'),
            to=from_date.strftime('%Y-%m-%d'),
            period=period
        )
        if len(market_data.results) != 0:  # make sure that we aren't counting weekends/holidays
            past_x_days.insert(0, from_date)
        from_date = (from_date - timedelta(days=1))
    print(past_x_days)
    exponential_moving_avg = 0
    ema_yest = simple_moving_average_calculator(isin=isin, period=period, from_date=past_x_days[0])
    multiplier = 2 / (num_days + 1)
    for day in past_x_days:  # initialize all variables above, then recursively find the EMA
        day_x_close_price = client.market_data.ohlc.get(
            period=period,
            isin=isin,
            from_=day.strftime('%Y-%m-%d'),
            to=day.strftime('%Y-%m-%d'),
            decimals=True,
            mic=os.getenv("MIC")).results[0].c
        exponential_moving_avg = day_x_close_price * multiplier + ema_yest * (1 - multiplier)
        ema_yest = exponential_moving_avg
    return exponential_moving_avg


def mean_reversion_decision(isin: str, x1: str = "d1"):
    """
    :param isin: pass the isin of your instrument
    :param x1: pass what type of data you want to retrieve (m1, h1 or d1)
    :return: returns whether you should buy (True) or sell (False), depending on MR criteria
    """
    simple_moving_avg = simple_moving_average_calculator(isin=isin, period=x1, from_date=datetime.now())
    print(f'Simple Moving Average Price: {simple_moving_avg}')
    exponential_moving_avg = exponential_moving_average_calculator(isin=isin, period=x1, from_date=datetime.now())
    print(f'Exponential Moving Average Price: {exponential_moving_avg}')

    latest_close_price = client.market_data.ohlc.get(
        period=x1,
        isin=isin,
        from_=datetime.now().strftime('%Y-%m-%d'),
        mic=os.getenv("MIC")).results[0].c
    if latest_close_price < exponential_moving_avg:  # change this line to use SMA or EMA
        return True
    return False


def mean_reversion(isin: str = "DE0007664039", x1: str = "d1"):
    """
    :param isin: pass the isin of the stock you are interested in,
                the default is Volkswagen here, but you can obviously use any ISIN you like :)
    :param x1:  pass the market data format you are interested in (m1, h1, or d1)
    """
    load_dotenv()
    venue = client.market_data.venues.get(os.getenv("MIC")).results[0]
    if not venue.is_open:  # make sure the venue is actually open
        print(f"Your selected venue, {venue.name}, is not open today. Next opening day is: "
              f"{venue.opening_days[0].day}-{venue.opening_days[0].month}-{venue.opening_days[0].year}")
        return

    quantity = 2
    price = client.market_data.quotes.get_latest(isin=isin).results[0].a
    if price * quantity < 50:  # make sure the order amount is large enough to pass through the api
        print(f"This order totals, €{price * quantity}, which is below the minimum order amount of €50.")

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
                expires_at=7,
                side="buy",
                quantity=quantity,
                venue=os.getenv("MIC"),
            )
            order_id = placed_order.results.id
            # subsequently activate the order
            activated_order = client.trading.orders.activate(order_id)
            print(activated_order)
        except Exception as e:
            print(f'1{e}')
    else:
        try:
            # create a sell order if mean reversion decision returns False
            print('sell')
            placed_order = client.trading.orders.create(
                isin=isin,
                expires_at=7,
                side="sell",
                quantity=quantity,
                venue=os.getenv("MIC"),
            )
            # if position in portfolio, activate order
            if placed_order is not None:
                order_id = placed_order.results.id
                activated_order = client.trading.orders.activate(order_id)
                print(activated_order)
            else:
                print("You do not have sufficient holdings to place this order.")
        except Exception as e:
            print(f'2{e}')


if __name__ == '__main__':
    scheduler = BlockingScheduler(timezone=utc)

    for x in range(13):
        scheduler.add_job(mean_reversion,
                          trigger=CronTrigger(day_of_week="mon-fri",
                                              hour=8 + x,
                                              minute=30,
                                              timezone=utc),
                          name="Perform Mean Reversion Hourly")

    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
