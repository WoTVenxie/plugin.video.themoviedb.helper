from tmdbhelper.lib.addon.plugin import get_setting
import tmdbhelper.lib.sync.trakt.synctype as trakt_synctype
import tmdbhelper.lib.sync.mdblist.synctype as mdblist_synctype
import tmdbhelper.lib.sync.flicklist.synctype as flicklist_synctype


def SyncHiddenProgressWatched():
    if get_setting('sync_source_watched', 'str') == 'MDbList':
        return mdblist_synctype.SyncHiddenProgressWatched
    return trakt_synctype.SyncHiddenProgressWatched


def SyncHiddenProgressCollected():
    if get_setting('sync_source_collection', 'str') == 'MDbList':
        return mdblist_synctype.SyncHiddenProgressCollected
    return trakt_synctype.SyncHiddenProgressCollected


def SyncHiddenCalendar():
    if get_setting('sync_source_watched', 'str') == 'MDbList':
        return mdblist_synctype.SyncHiddenCalendar
    return trakt_synctype.SyncHiddenCalendar


def SyncHiddenDropped():
    return trakt_synctype.SyncHiddenDropped


def SyncRatings():
    if get_setting('sync_source_ratings', 'str') == 'FlickList':
        return flicklist_synctype.SyncRatings
    return trakt_synctype.SyncRatings


def SyncFavorites():
    return trakt_synctype.SyncFavorites


def SyncAllNextEpisodes():
    if get_setting('sync_source_collection', 'str') == 'MDbList':
        return mdblist_synctype.SyncAllNextEpisodes
    return trakt_synctype.SyncAllNextEpisodes


def SyncWatchlist():
    source = get_setting('sync_source_watchlist', 'str')

    if source == 'MDbList':
        return mdblist_synctype.SyncWatchlist

    if source == 'FlickList':
        return flicklist_synctype.SyncWatchlist

    return trakt_synctype.SyncWatchlist


def SyncCollection():
    if get_setting('sync_source_collection', 'str') == 'MDbList':
        return mdblist_synctype.SyncCollection
    return trakt_synctype.SyncCollection


def SyncPlayback():
    source = get_setting('sync_source_playback', 'str')

    if source == 'MDbList':
        return mdblist_synctype.SyncPlayback

    if source == 'FlickList':
        return flicklist_synctype.SyncPlayback

    return trakt_synctype.SyncPlayback


def SyncNextEpisodes():
    if get_setting('sync_source_watched', 'str') == 'MDbList':
        return mdblist_synctype.SyncNextEpisodes
    return trakt_synctype.SyncNextEpisodes


def SyncWatched():
    source = get_setting('sync_source_watched', 'str')

    if source == 'MDbList':
        return mdblist_synctype.SyncWatched

    if source == 'FlickList':
        return flicklist_synctype.SyncWatched

    return trakt_synctype.SyncWatched


def SyncAiredEpisodes():
    if get_setting('sync_source_watched', 'str') == 'MDbList':
        return SyncNextEpisodes()  # AIRED/WATCHED counts in next episodes for MDbList
    return SyncWatched()
