import logging
import requests

blocksync_defaults = {
    'endpoint': 'http://localhost:8090',
    'endpoints': ['http://localhost:8090'],
}

class BaseAdapter():

    def __init__(self, endpoints=['http://localhost:8090'], debug=False):
        self.debug = debug
        #
        if not debug:
            request_logger = logging.getLogger('jsonrpcclient.client.request')
            response_logger = logging.getLogger('jsonrpcclient.client.response')
            request_logger.setLevel(logging.getLevelName('WARNING'))
            response_logger.setLevel(logging.getLevelName('WARNING'))
        # Use endpoints or set defaults
        if isinstance(endpoints, list):
            self.endpoint = endpoints[0] if endpoints else blocksync_defaults['endpoint']
            self.endpoints = endpoints if endpoints else blocksync_defaults['endpoints']
        elif isinstance(endpoints, str):
            self.endpoint = endpoints if endpoints else blocksync_defaults['endpoint']
            self.endpoints = [self.endpoint]
        else:
            self.endpoint = blocksync_defaults['endpoint']
            self.endpoints = blocksync_defaults['endpoints']

    def call(self, method, **kwargs):
        try:
            # Execute the call against the loaded adapter
            response = getattr(self, method)(**kwargs)
            # Return the response
            return response
        except requests.ConnectionError:
            # Identify the failing endpoint
            failure = self.endpoint
            # Remove the failing node from the endpoints
            self.endpoints.remove(failure)
            # If we have remaining endpoints to try, attempt them
            if len(self.endpoints) > 0:
                # Set the new endpoints as the next in the list
                self.endpoint = self.endpoints[0]
                # Retry the call with the new endpoint
                return self.call(method, **kwargs)
            else:
                # If no endpoints are reachable, raise an exception
                raise Exception("connection error - no available endpoints")
