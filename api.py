import requests
import json
from key import auth
from iex.utils import (param_bool,
                       parse_date,
                       validate_date_format,
                       validate_range_set,
                       validate_output_format,
                       timestamp_to_datetime,
                       timestamp_to_isoformat)
from constants import (BASE_URL)


class Batch:
    def __init__(self, symbols_list, date_format="timestamp"):
        self.symbols = symbols_list

    def _get_with_token(self, url, params):
        request_url = url
        params.update({
            'token': auth._get_publishable()})
        return requests.get(url, params)

    def _get(self, _type, params={}):
        self.url = f"{BASE_URL}/stock/market/batch"
        params.update({
            'symbols': self.symbols,
            'types': _type})

        response = self._get_with_token(self.url, params=params)

        if response.status_code != 200:
            raise Exception(
                f"{response.status_code}: {response.content.decode('utf-8')}")

        return response.json()

    def book(self):
        return self._get("book")

    def company(self):
        return self._get("company")

    def delayed_quote(self):
        return self._get("delayed_quote")

    def earnings(self):
        return self._get('earnings')

    def financials(self):
        return self._get('financials')

    def stats(self):
        return self._get('stats')

    def peers(self):
        return self._get('peers')

    def price(self):
        return self._get("price")

    def quote(self, displayPercent=False):
        displayPercent = param_bool(displayPercent)
        return self._get("quote", params={"displayPercent": displayPercent})
