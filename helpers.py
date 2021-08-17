import os
import requests
from dotenv import load_dotenv


class RequestHandler:
    load_dotenv()
    url_data: str = os.environ.get("BASE_URL_DATA")
    url_trading: str = os.environ.get("BASE_URL_TRADING")
    auth_url: str = os.environ.get("AUTH_URL")

    def get_token(self, endpoint: str, data):
        """
        :param data:
        :param endpoint:
        :return: access token as String
        """
        response = requests.post(self.auth_url + endpoint, data)
        return response

    def get_data_trading(self, endpoint: str):
        response = requests.get(self.url_trading + endpoint,
                                headers={
                                    "Authorization": "Bearer " + os.environ.get("TOKEN_KEY")
                                })

        return response.json()

    def get_data_data(self, endpoint: str):
        """
        :param endpoint: {str} only append the endpoint to the base url
        :return:
        """
        response = requests.get(self.url_data + endpoint,
                                headers={
                                    "Authorization": "Bearer " + os.environ.get("TOKEN_KEY")
                                })

        return response.json()

    def put_data(self, endpoint: str):
        response = requests.put(self.url_trading + endpoint,
                                headers={
                                    "Authorization": "Bearer " + os.environ.get("TOKEN_KEY")
                                })
        return response.json()

    def post_data(self, endpoint: str, data):
        response = requests.post(self.url_trading + endpoint,
                                 data,
                                 headers={
                                     "Authorization": "Bearer " + os.environ.get("TOKEN_KEY")
                                 })
        return response.json()
