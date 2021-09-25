import requests

from django.conf import settings

from rest_framework.validators import ValidationError

from apps.oauth.models import OAuth


class OAuthService(object):
    config_secret = ()

    @staticmethod
    def google_validate_client_id(self, data):
        # [id_token]으로 Google OAuth에 request 전송
        # client_id값으로 user 유효성 검증 (request를 보낸 client가 우리의 client가 맞는지 확인하는 logic)
        context = {
            'id_token': data['tokenId']
        }
        response = requests.post(self.google_id_token_info_url, data=context)
        if not response.ok:
            raise ValidationError(response.reason)

        response_json = response.json()
        client_id = getattr(settings, 'auth')['google']['client_id']
        print(client_id)

        response_flag = [client_id == response_json['aud']]
        print(response_flag)
        return response_flag
