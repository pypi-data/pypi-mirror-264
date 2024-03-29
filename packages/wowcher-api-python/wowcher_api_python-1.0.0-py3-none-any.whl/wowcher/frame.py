from .api import WowcherApi


class WowcherPaymentFrame(WowcherApi):
    GET_FRAME_LINK = '/ext/frame/link'

    def get_frame_url(
            self,
            client_id: str,
            merchant_id: str,
            activation_callback_url: str,
            language: str = "en",
            countries: list = None
    ):
        url = f'{self.api_url}{self.GET_FRAME_LINK}'
        headers = {
            "X-ApiKey": self.api_key
        }

        request_body = {
            "client_id": client_id,
            "merchant_id": merchant_id,
            "activation_callback_url": activation_callback_url,
            "language": language
        }

        if countries is not None:
            request_body["countries"] = countries

        response = self.api_request(url, request_body, headers=headers)

        return response["data"]["link"]
