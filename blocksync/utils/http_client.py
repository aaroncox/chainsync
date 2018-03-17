import requests
from jsonrpcclient import config
from jsonrpcclient.exceptions import ParseResponseError
from jsonrpcclient.http_client import HTTPClient
from jsonrpcclient.prepared_request import PreparedRequest
from jsonrpcclient.request import Request
config.validate = False

class HttpClient(HTTPClient):

    def send(self, request, **kwargs):
        response = super(HttpClient, self).send(request, **kwargs)
        if not response or 'error' in response:
            print("response")
            print(response)
            raise requests.RequestException()
        return response

    def request(self, method_name, *args, **kwargs):
        response = super(HttpClient, self).send(Request(method_name, *args, **kwargs))
        if not response or 'error' in response:
            print("response")
            print(response)
            raise requests.RequestException()
        return response
