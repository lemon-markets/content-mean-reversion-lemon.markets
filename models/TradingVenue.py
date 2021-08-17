import os
from dotenv import load_dotenv
from helpers import RequestHandler
from datetime import datetime, timedelta
import datetime


class TradingVenue(RequestHandler):

    def __init__(self, is_open: bool = False):
        self.is_open = is_open

    def check_if_open(self):
        load_dotenv()
        mic = os.getenv("MIC")
        endpoint = f'venues/?mic={mic}'
        response = self.get_data_data(endpoint)
        self.is_open = response['results'][0].get('is_open', None)
        return self.is_open

    def get_opening_times(self):
        load_dotenv()
        mic = os.getenv("MIC")
        endpoint = f'venues/?mic={mic}'
        response = self.get_data_data(endpoint)
        return response

    def seconds_till_tv_opens(self):
        times_venue = self.get_opening_times()
        today = datetime.datetime.today()
        opening_days_venue = times_venue['results'][0].get('opening_days', None)
        next_opening_day = datetime.datetime.strptime(opening_days_venue[0], '%Y-%m-%d')
        next_opening_hour = datetime.datetime.strptime(times_venue['results'][0]['opening_hours'].get('start', None),                                            '%H:%M')
        date_difference = next_opening_day - today
        days = date_difference.days + 1

        if not self.check_if_open():
            print('Trading Venue not open')
            time_delta = datetime.datetime.combine(
                datetime.datetime.now().date() + timedelta(days=1), next_opening_hour.time()
            ) - datetime.datetime.now()
            print(time_delta.seconds + (days * 86400))
            return time_delta.seconds
        else:
            print('Trading Venue is open')
            return 0
