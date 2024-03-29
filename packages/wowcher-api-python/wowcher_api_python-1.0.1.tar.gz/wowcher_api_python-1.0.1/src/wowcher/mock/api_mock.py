from wowcher.api import WowcherApi


class WowcherApiMock(WowcherApi):
    @staticmethod
    def api_request(url, json, headers=None):
        return {
            "result": "success",
            "data": {
                "items": [{
                    "code": code,
                    "value": 100,
                    "currency": "USD",
                } for code in json["codes"]]
            }
        }
