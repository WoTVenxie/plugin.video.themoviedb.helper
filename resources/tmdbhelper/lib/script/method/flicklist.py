# Module: default
# Author: WoTVenxie
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html

import time

from xbmcgui import Dialog

from tmdbhelper.lib.api.flicklist.api import FlickListAPI
from tmdbhelper.lib.addon.plugin import executebuiltin


def authenticate_flicklist(**kwargs):
    api = FlickListAPI()

    response = api.device_code()

    if not response:
        Dialog().notification(
            'FlickList',
            'Unable to start authentication',
            time=5000
        )
        return

    device_code = response.get('device_code')
    user_code = response.get('user_code')
    verification_uri = response.get(
        'verification_uri',
        'https://flicklist.tv/link'
    )
    expires_in = response.get('expires_in', 900)
    interval = response.get('interval', 5)

    if not device_code or not user_code:
        Dialog().notification(
            'FlickList',
            'Invalid device authentication response',
            time=5000
        )
        return

    Dialog().ok(
        'FlickList Authentication',
        'Open the following address:\n\n'
        '{}\n\n'
        'Enter this code:\n\n'
        '[B]{}[/B]'.format(
            verification_uri,
            user_code
        )
    )

    executebuiltin(
        'System.OpenURL({})'.format(verification_uri)
    )

    started = time.time()

    while time.time() - started < expires_in:
        time.sleep(interval)

        response = api.device_token(device_code)

        if not response:
            continue

        error = response.get('error')

        if error == 'authorization_pending':
            continue

        if error == 'access_denied':
            Dialog().notification(
                'FlickList',
                'Authentication was denied',
                time=5000
            )
            return

        if error == 'expired_token':
            Dialog().notification(
                'FlickList',
                'Authentication code expired',
                time=5000
            )
            return

        token = response.get('access_token') or response.get('token')

        if token:
            api.authenticate(
                token,
                stored_at=time.time()
            )

            Dialog().notification(
                'FlickList',
                'Authentication successful',
                time=5000
            )

            return

    Dialog().notification(
        'FlickList',
        'Authentication timed out',
        time=5000
    )


def test_flicklist(**kwargs):
    api = FlickListAPI()

    if not api.is_authenticated():
        Dialog().notification(
            'FlickList',
            'Not authenticated',
            time=5000
        )
        return

    response = api.me()

    if not response:
        Dialog().notification(
            'FlickList',
            'Authentication failed',
            time=5000
        )
        return

    username = response.get('username') or response.get('display_name')

    if username:
        Dialog().notification(
            'FlickList',
            'Authenticated as {}'.format(username),
            time=5000
        )
    else:
        Dialog().notification(
            'FlickList',
            'Authentication successful',
            time=5000
        )


def test_flicklist_activities(**kwargs):
    from tmdbhelper.lib.addon.logger import kodi_log

    api = FlickListAPI()

    if not api.is_authenticated():
        Dialog().notification(
            'FlickList',
            'Not authenticated',
            time=5000
        )
        return

    response = api.last_activities()

    kodi_log(
        'FlickList last_activities: {}'.format(response),
        1
    )

    Dialog().notification(
        'FlickList',
        'Last activities written to Kodi log',
        time=5000
    )
