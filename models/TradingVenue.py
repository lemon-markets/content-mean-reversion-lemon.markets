import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from lemon import api
import datetime

load_dotenv()
client = api.create(
    trading_api_token=os.environ.get('TRADING_API_KEY'),
    market_data_api_token=os.environ.get('DATA_API_KEY'),
    env='paper'
)
print(client)


class TradingVenue:
    def __init__(self, is_open: bool = False):
        self.is_open = is_open

    def seconds_till_tv_opens(self):
        load_dotenv()
        times_venue = client.market_data.venues.get(os.getenv('MIC'))
        today = datetime.datetime.today()
        opening_days_venue = times_venue.results[0].opening_days
        next_opening_day = datetime.datetime.combine(opening_days_venue[0], datetime.datetime.min.time())
        next_opening_hour = datetime.datetime.combine(opening_days_venue[0], times_venue.results[0].opening_hours.start)
        date_difference = next_opening_day - today
        days = date_difference.days + 1

        if not self.is_open:
            print('Trading Venue not open')
            time_delta = datetime.datetime.combine(
                datetime.datetime.now().date() + timedelta(days=1), next_opening_hour.time()
            ) - datetime.datetime.now()
            print(time_delta.seconds + (days * 86400))
            return time_delta.seconds
        else:
            print('Trading Venue is open')
            return 0
