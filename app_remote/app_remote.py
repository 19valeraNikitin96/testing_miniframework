import requests
import json


class AppRemote(object):

    def __init__(self, domain: str, port: int, protocol: str, access_token: str):
        self.domain = domain
        self.port = port
        self.protocol = protocol
        self.access_token = access_token

    def request(self, path: str, method: str, params: dict = {}, req_body: dict = {}, req_headers={}) -> dict:
        url = '{}://{}:{}{}'.format(self.protocol, self.domain, self.port, path)
        response = requests.request(method, url, params=params, json=req_body, headers=req_headers)
        resp_json = json.loads(response.text)
        return resp_json
