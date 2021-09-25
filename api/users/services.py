import requests
from urllib.parse import urlparse

from django.conf import settings


class AddressService(object):
    def __init__(self):
        self.url = "https://dapi.kakao.com/v2/local/search/address.json?query="

    def get_address_point(self, text):
        client_secret = getattr(settings, 'KAKAO')['admin_key']
        request_url = self.url + text
        result = requests.get(
            urlparse(request_url).geturl(),
            headers={'Authorization': 'KakaoAK '+client_secret}
        )
        address = result.json()['documents'][0]['address']
        lat = address['y']
        long = address['x']
        return float(lat), float(long)