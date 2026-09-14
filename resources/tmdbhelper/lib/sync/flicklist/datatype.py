from tmdbhelper.lib.sync.datatype import (
    DataType,
    DataTypeEpisodesInShows,
    DataTypeShowsToEpisodes,
)


class FlickListDataType(DataType):

    @property
    def sync_args(self):
        return ('sync', self.method, f'{self.item_type}s',)

    def get_syncitem(self, meta):
        from tmdbhelper.lib.sync.flicklist.itemdata import FlickListSyncItem
        return FlickListSyncItem(
            self.item_type,
            meta,
            self.keys,
            key_prefix=self.key_prefix
        )

    def get_response_sync_data(self, *args, **kwargs):
        endpoint = '/sync/{}'.format(self.method)

        if self.method == 'watched':
            if self.item_type == 'movie':
                endpoint = '/sync/watched/movies'
            elif self.item_type == 'show':
                endpoint = '/sync/watched/shows'

        return self.flicklist_api.request(endpoint)

    def get_response_sync(self, *args, **kwargs):
        response = self.get_response_sync_data(*args, **kwargs)

        if response is None:
            return

        if not isinstance(response, list):
            if isinstance(response, dict):
                for key in ('items', 'results', 'data'):
                    if isinstance(response.get(key), list):
                        response = response[key]
                        break

        if not isinstance(response, list):
            return

        if self.method != 'watched' or self.item_type == 'movie':
            return response

        flattened = []

        for show in response:
            show_data = show.get('show') or {}
            show_plays = show.get('plays')
            show_last_watched = show.get('last_watched_at')
            reset_at = show.get('reset_at')

            for season in show.get('seasons') or []:
                season_number = season.get('number')

                if season_number == 0:
                    continue

                for episode in season.get('episodes') or []:
                    flattened.append({
                        'show': show_data,
                        'episode': {
                            'season': season_number,
                            'number': episode.get('number'),
                        },
                        'plays': episode.get('plays', show_plays),
                        'last_watched_at': (
                            episode.get('last_watched_at')
                            or show_last_watched
                        ),
                        'reset_at': reset_at,
                    })

        return flattened


class FlickListDataTypeEpisodesInShows(
    DataTypeEpisodesInShows,
    FlickListDataType
):
    pass


class FlickListDataTypeShowsToEpisodes(
    DataTypeShowsToEpisodes,
    FlickListDataType
):
    pass
