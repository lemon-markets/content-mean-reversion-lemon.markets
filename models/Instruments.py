import os
from dotenv import load_dotenv
from helpers import RequestHandler
from datetime import datetime, timedelta


class Instruments(RequestHandler):

    def __init__(self, isin: str = "", x1: str = ""):
        self.isin = isin
        self.x1 = x1

    def get_market_data(self):
        load_dotenv()
        mic = os.getenv("MIC")
        from_date = datetime.now() - timedelta(days=7)
        to_date = datetime.now()
        isin = self.isin
        x1 = self.x1
        endpoint = f'ohlc/{x1}/?mic={mic}&isin={isin}&from={from_date}&to={to_date}'
        response = self.get_data_data(endpoint)
        print(response)
        return response

    def get_latest_market_data(self):
        load_dotenv()
        mic = os.getenv("MIC")
        isin = self.isin
        x1 = self.x1
        endpoint = f'ohlc/{x1}/?mic={mic}&isin={isin}&from=latest'
        try:
            response = self.get_data_data(endpoint)
            close_price = response['results'][0].get('c', None)
            return close_price
        except Exception as e:
            print(e)
