import time

from tmdbhelper.lib.api.request import NoCacheRequestAPI
from tmdbhelper.lib.addon.plugin import get_setting, set_setting


API_URL = 'https://flicklist.tv/api'
API_V3_URL = 'https://flicklist.tv/api/v3'
CLIENT_ID = 'fl_kodi_scrobbler'


class FlickListAPI(NoCacheRequestAPI):

    def __init__(self):
        super(FlickListAPI, self).__init__(
            req_api_url=API_V3_URL,
            req_api_name='FlickListAPI',
            timeout=20
        )

        self.token = get_setting('flicklist_token')
        self.token_stored_at = get_setting('flicklist_token_stored_at')

    @property
    def headers(self):
        return {
            'Authorization': 'Bearer {}'.format(self.token),
            'Content-Type': 'application/json',
        }

    @headers.setter
    def headers(self, value):
        """Ignore base class req_api attempting to set headers."""
        return

    # ------------------------------------------------------------------
    # Authentication
    # ------------------------------------------------------------------

    def device_code(self):
        return self.get_api_request_json(
            '{}/auth/device/code'.format(API_URL),
            postdata={
                'client_id': CLIENT_ID,
                'credential': 'session'
            }
        )

    def device_token(self, device_code):
        return self.get_api_request_json(
            '{}/auth/device/token'.format(API_URL),
            postdata={
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

        response = self.get_api_request_json(
            '{}/auth/refresh'.format(API_URL),
            headers=self.headers,
            method='post'
        )

        if response and response.get('token'):
            self.authenticate(response['token'])
            return response

        return None

    def is_authenticated(self):
        return bool(self.token)

    # ------------------------------------------------------------------
    # FlickList API v3
    # ------------------------------------------------------------------

    def request(self, endpoint, method='GET', data=None):
        url = '{}{}'.format(API_V3_URL, endpoint)

        return self.get_api_request_json(
            url,
            postdata=data,
            headers=self.headers,
            method=method.lower()
        )

    # ------------------------------------------------------------------
    # Account
    # ------------------------------------------------------------------

    def me(self):
        return self.request('/me')

    # ------------------------------------------------------------------
    # Sync
    # ------------------------------------------------------------------

    def last_activities(self):
        return self.request('/sync/last_activities')

    def watched_movies(self):
        return self.request('/sync/watched/movies')

    def watched_shows(self):
        return self.request('/sync/watched/shows')

    def up_next(self):
        return self.request('/sync/up_next')
