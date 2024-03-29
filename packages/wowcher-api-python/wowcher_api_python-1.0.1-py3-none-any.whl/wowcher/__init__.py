import os

from .api import WowcherApi
from .frame import WowcherPaymentFrame
from .mock import WowcherApiMock
from .mock import WowcherPaymentFrameMock


WowcherApi = WowcherApi\
    if os.environ.get('WOWCHER_API_MOCK', "False") != "True"\
    else WowcherApiMock

WowcherPaymentFrame = WowcherPaymentFrame\
    if os.environ.get('WOWCHER_API_MOCK', "False") != "True"\
    else WowcherPaymentFrameMock
