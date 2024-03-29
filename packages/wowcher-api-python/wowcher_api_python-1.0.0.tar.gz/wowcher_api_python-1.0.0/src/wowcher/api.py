import requests


class WowcherApi:
    ACTIVATION_VOUCHERS_ROUTE = '/ext/voucher/activate/list'
    BASE_URL = 'https://wowcher.app'

    def __init__(self, api_key: str, base_url: str = BASE_URL):
        self.base_url = base_url
        self.api_url = f"{base_url}/api/v1"
        self.api_key = api_key

    def activate_vouchers(self, codes: list) -> dict:
        url = f'{self.api_url}{self.ACTIVATION_VOUCHERS_ROUTE}'
        headers = {
            "X-ApiKey": self.api_key
        }

        response = self.api_request(url, {"codes": codes}, headers=headers)

        return response["data"]["items"]

    @staticmethod
    def api_request(url, json, headers=None):
        result = requests.post(url, json=json, headers=headers)

        if result.status_code in [400, 401, 402, 403, 404]:
            if result.headers and 'application/json' in result.headers.get('Content-Type'):
                if result.json().get("message"):
                    raise Exception(result.json().get("message"))

        if result.status_code != 200:
            raise Exception("Sorry, an unknown error has returned from the server. Please try again later.")

        return result.json()
