import uuid
from wowcher import WowcherPaymentFrame


def test_get_frame_url(requests_mock):
    frame = WowcherPaymentFrame("api_key")

    data = {
        "link": f'https://wowcher.app/en/payment-frame?frame_id=test123'
    }

    requests_mock.post(
        "https://wowcher.app/api/v1/ext/frame/link",
        json={
            "code": 0,
            "data": data,
            "status": "success",
            "message": "The request was successful."
        },
        status_code=200,
        headers={"Content-Type": "application/json"}
    )

    assert frame.get_frame_url(
        uuid.uuid4().hex,
        uuid.uuid4().hex,
        'https://example.com',
        "en",
        ["EG"]
    ) == data['link']
