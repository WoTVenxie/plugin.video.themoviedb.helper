from tmdbhelper.lib.addon.consts import HALFDAY_EXPIRY
from tmdbhelper.lib.sync.flicklist.datatype import (
    FlickListDataType,
    FlickListDataTypeEpisodesInShows,
    FlickListDataTypeShowsToEpisodes,
)
from tmdbhelper.lib.sync.datatype import timerlock


class SyncWatched(FlickListDataTypeEpisodesInShows):
    keys = (
        'plays',
        'last_watched_at',
        'reset_at',
    )
    last_activities_key = 'last_watched_at'
    method = 'watched'


class SyncPlayback(FlickListDataTypeShowsToEpisodes):
    keys = (
        'progress',
        'paused_at',
        'id',
    )
    last_activities_key = 'id'
    method = 'playback'
    key_prefix = 'playback'


class SyncRatings(FlickListDataType):
    keys = (
        'rating',
        'rated_at',
    )
    last_activities_key = 'rated_at'
    method = 'ratings'


class SyncWatchlist(FlickListDataType):
    keys = (
        'listed_at',
    )
    last_activities_key = 'added_at'
    method = 'watchlist'
    key_prefix = 'watchlist'


class SyncUpNext(FlickListDataTypeShowsToEpisodes):
    keys = (
        'next_episode_id',
        'next_episode_aired_at',
    )
    last_activities_key = 'watched_at'
    method = 'up_next'
    expiry_time = HALFDAY_EXPIRY

    @timerlock
    def sync_func(self):
        """Get next episodes from FlickList."""
        return self.get_response_sync()
