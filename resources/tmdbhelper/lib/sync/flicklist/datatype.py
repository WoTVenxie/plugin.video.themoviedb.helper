from tmdbhelper.lib.sync.datatype import DataType, DataTypeEpisodesInShows, DataTypeShowsToEpisodes


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
        return self.flicklist_api.request(
            '/{}'.format(self.method)
        )

    def get_response_sync(self, *args, **kwargs):
        response = self.get_response_sync_data(*args, **kwargs)

        if response is None:
            return

        if isinstance(response, dict):
            for key in ('items', 'results', 'data'):
                if key in response:
                    return response[key]

        return response


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
