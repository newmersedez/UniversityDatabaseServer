import json


class Request:
    def __init__(self, data=None):
        self.request_name = None
        self.args = []
        self._parseRequest(data)

    def _parseRequest(self, data):
        request = json.loads(data)
        self.request_name = request['RequestName']
        self.args = request['Args']
