import requests
import sys
import datetime
import time
import json

from jsonrpcclient import config
from jsonrpcclient.http_client import HTTPClient
from jsonrpcclient.request import Request

from websocket import create_connection

config.validate = False


class Client(HTTPClient):

    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.connect()

    def connect(self):
        print("connecting: {}".format(self.endpoint))
        self.websocket = create_connection(self.endpoint)

    def send(self, request, **kwargs):
        # start_time = time.time()
        self.websocket.send(str(request))
        response = self.websocket.recv()
        # total_time = "%.3f" % (time.time() - start_time)
        # print("[{}] http request - {} kb / {} sec - {} {}".format(datetime.datetime.now(), sys.getsizeof(str(response)) / 1000, total_time, request, list(kwargs)))
        if 'error' in response:
            print("response error")
            print(response)
            raise requests.RequestException()
        return json.loads(response)['result']

    def request(self, method_name, *args, **kwargs):
        # start_time = time.time()
        self.websocket.send(str(Request(method_name, *args, **kwargs)))
        response = self.websocket.recv()
        # total_time = "%.3f" % (time.time() - start_time)
        # print("[{}] http request - {} kb / {} sec - {} {}".format(datetime.datetime.now(), sys.getsizeof(str(response)) / 1000, total_time, method_name, list(args)))
        if 'error' in response:
            print("response error")
            print(response)
            raise requests.RequestException()
        return json.loads(response)['result']
