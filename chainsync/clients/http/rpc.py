import requests
import sys
import datetime
import time

from jsonrpcclient.http_client import HTTPClient
from jsonrpcclient.request import Request

from jsonrpcclient import config
config.validate = False


class Client(HTTPClient):

    def send(self, request, **kwargs):
        # start_time = time.time()
        response = super(Client, self).send(request, **kwargs)
        # total_time = "%.3f" % (time.time() - start_time)
        # print("[{}] http request - {} kb / {} sec - {} {}".format(datetime.datetime.now(), sys.getsizeof(str(response)) / 1000, total_time, request, list(kwargs)))
        # print(response)
        if 'error' in response:
            print("response error")
            print(response)
            raise requests.RequestException()
        return response

    def request(self, method_name, *args, **kwargs):
        # start_time = time.time()
        response = super(Client, self).send(Request(method_name, *args, **kwargs))
        # total_time = "%.3f" % (time.time() - start_time)
        # print("[{}] http request - {} kb / {} sec - {} {}".format(datetime.datetime.now(), sys.getsizeof(str(response)) / 1000, total_time, method_name, list(args)))
        # print(response)
        if 'error' in response:
            print("response error")
            print(response)
            raise requests.RequestException()
        return response
