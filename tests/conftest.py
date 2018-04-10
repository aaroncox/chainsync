import pytest

from chainsync.adapters.steem import SteemAdapter
from chainsync.adapters.steemv2 import SteemV2Adapter


def pytest_addoption(parser):
    parser.addoption("--adapter", action="store", default="steem", help="steem, steemv2, etc")
    parser.addoption("--endpoint", action="store", default="https://api.steemit.com", help="http://localhost:8090, https://public-endpoint.com")


@pytest.fixture(scope="class")
def client(request):
    adapter = request.config.getoption("--adapter")
    endpoint = request.config.getoption("--endpoint")
    test_data = {
        'block_with_ops': 1093,
        'blocks_with_ops': 1094,
    }

    if adapter == 'steem_appbase':
        request.cls.adapter = SteemV2Adapter(endpoints=[endpoint])
    else:
        request.cls.adapter = SteemAdapter(endpoints=[endpoint])

    request.cls.test_data = test_data
