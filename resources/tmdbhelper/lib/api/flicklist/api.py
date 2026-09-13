import time

from tmdbhelper.lib.addon.plugin import get_setting, set_setting
from tmdbhelper.lib.request import request_json


API_URL = 'https://flicklist.tv/api'
API_V3_URL = 'https://flicklist.tv/api/v3'
CLIENT_ID = 'fl_kodi_scrobbler'


class FlickListAPI:

    def __init__(self):
        self.token = get_setting('flicklist_token')
        self.token_stored_at = get_setting('flicklist_token_stored_at')

    def _headers(self):
        return {
            'Authorization': 'Bearer {}'.format(self.token),
            'Content-Type': 'application/json',
        }

    def request(self, endpoint, method='GET', data=None):
        url = '{}{}'.format(API_V3_URL, endpoint)

        return request_json(
            url,
            headers=self._headers(),
            method=method,
            data=data
        )

    def device_code(self):
        return request_json(
            '{}/auth/device/code'.format(API_URL),
            headers={'Content-Type': 'application/json'},
            method='POST',
            data={
                'client_id': CLIENT_ID,
                'credential': 'session'
            }
        )

    def device_token(self, device_code):
        return request_json(
            '{}/auth/device/token'.format(API_URL),
            headers={'Content-Type': 'application/json'},
            method='POST',
            data={
                'device_code': device_code
            }
        )

    def authenticate(self, token, stored_at=None):
        self.token = token
        self.token_stored_at = stored_at or time.time()

        set_setting('flicklist_token', self.token)
        set_setting(
            'flicklist_token_stored_at',
            str(self.token_stored_at)
        )

    def refresh(self):
        if not self.token:
            return None

        response = request_json(
            '{}/auth/refresh'.format(API_URL),
            headers=self._headers(),
            method='POST'
        )

        if response and response.get('token'):
            self.authenticate(response['token'])
            return response

        return None

    def is_authenticated(self):
        return bool(self.token)

    def me(self):
        return self.request('/me')
