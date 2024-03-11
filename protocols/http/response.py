import requests

class HttpResponse:

    def __init__(self, status=None, header=None, body=None, raw=None, response:requests.Response=None):
        self.status = status
        self.header = header
        self.body = body
        self.raw = raw
        if response is not None:
            self.setResponse(response)

    def setResponse(self, response: requests.Response):
        self.status = response.status_code
        self.header = response.headers
        self.body = response.text
        self.raw = response.raw
    