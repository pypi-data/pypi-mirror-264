from wowcher import WowcherApi


def test_activate_vouchers(requests_mock):
    codes = ["code1", "code2"]

    data = {
        "items": [
            {
                "code": code,
                "value": 100,
                "currency": "USD"
            } for code in codes
        ]
    }

    requests_mock.post(
        "https://wowcher.app/api/v1/ext/voucher/activate/list",
        json={
            "code": 0,
            "data": data,
            "status": "success",
            "message": "The request was successful."
        },
        status_code=200,
        headers={"Content-Type": "application/json"}
    )

    api = WowcherApi("api_key")
    result = api.activate_vouchers(codes)

    assert result == data["items"]


def test_activate_vouchers_400(requests_mock):
    codes = ["code1", "code2"]
    error_message = "Voucher not found."

    requests_mock.post(
        "https://wowcher.app/api/v1/ext/voucher/activate/list",
        json={
            "code": 1019,
            "status": "error",
            "message": error_message
        },
        status_code=400,
        headers={"Content-Type": "application/json"}
    )

    api = WowcherApi("api_key")

    try:
        api.activate_vouchers(codes)
    except Exception as e:
        assert str(e) == error_message


def test_activate_vouchers_500(requests_mock):
    codes = ["code1", "code2"]
    error_message = "Sorry, an unknown error has returned from the server. Please try again later."

    requests_mock.post(
        "https://wowcher.app/api/v1/ext/voucher/activate/list",
        json={
            "code": 1019,
            "status": "error",
            "message": error_message
        },
        status_code=500,
        headers={"Content-Type": "application/json"}
    )

    api = WowcherApi("api_key")

    try:
        api.activate_vouchers(codes)
    except Exception as e:
        assert str(e) == error_message


def test_activate_vouchers_without_error_message(requests_mock):
    codes = ["code1", "code2"]
    error_message = "Sorry, an unknown error has returned from the server. Please try again later."

    requests_mock.post(
        "https://wowcher.app/api/v1/ext/voucher/activate/list",
        json={
            "status": "error",
        },
        status_code=400,
        headers={"Content-Type": "application/json"}
    )

    api = WowcherApi("api_key")

    try:
        api.activate_vouchers(codes)
    except Exception as e:
        assert str(e) == error_message
