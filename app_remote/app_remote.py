import requests
import json


class AppRemote(object):

    def __init__(self, domain: str, port: int, protocol: str, access_token: str=None):
        self.domain = domain
        self.port = port
        self.protocol = protocol
        self.access_token = access_token

    def request(self, path: str, method: str, params=None, req_body=None, req_headers=None) -> dict:
        if req_headers is None:
            req_headers = {}
        if req_body is None:
            req_body = {}
        if params is None:
            params = {}
        url = '{}://{}:{}{}'.format(self.protocol, self.domain, self.port, path)
        response = requests.request(method, url, params=params, json=req_body, headers=req_headers)
        resp_json = json.loads(response.text)
        return resp_json