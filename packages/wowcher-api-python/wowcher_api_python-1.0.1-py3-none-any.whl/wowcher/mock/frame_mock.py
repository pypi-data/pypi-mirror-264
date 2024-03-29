from wowcher.frame import WowcherPaymentFrame


class WowcherPaymentFrameMock(WowcherPaymentFrame):
    @staticmethod
    def api_request(url, json, headers=None) -> dict:
        return {
            "result": "success",
            "data": {
                "link": f'https://wowcher.app/en/payment-frame?frame_id=test123'
            }
        }
