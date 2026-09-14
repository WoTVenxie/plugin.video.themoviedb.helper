#!/usr/bin/python
# -*- coding: utf-8 -*-

from jurialmunkey.ftools import cached_property
from tmdbhelper.lib.sync.itemdata import SyncItemData, SyncItem
from tmdbhelper.lib.sync.itemconf import SyncItemConstructor


class FlickListSyncItemData(SyncItemData):

    def __init__(self, item, item_type):
        self.item = item
        self.item_type = item_type

    """
    season_number
    """
    @cached_property
    def season_number(self):
        return self.get_season_number()

    def get_season_number(self):
        if self.item_type == 'season':
            try:
                return self.item['season']['number']
            except (AttributeError, KeyError, TypeError):
                return

        if self.item_type == 'episode':
            try:
                return self.item['episode']['season']
            except (AttributeError, KeyError, TypeError):
                return

    """
    episode_number
    """
    @cached_property
    def episode_number(self):
        return self.get_episode_number()

    def get_episode_number(self):
        if self.item_type == 'episode':
            try:
                return self.item['episode']['number']
            except (AttributeError, KeyError, TypeError):
                return

    """
    tmdb_id
    """
    @cached_property
    def tmdb_id(self):
        return self.get_tmdb_id()

    def get_tmdb_id(self):
        try:
            return self.item[self.parent_item_type]['ids']['tmdb']
        except (AttributeError, KeyError, TypeError):
            return

    """
    flicklist_id
    """
    @cached_property
    def flicklist_id(self):
        return self.get_flicklist_id()

    def get_flicklist_id(self):
        try:
            return self.item[self.parent_item_type]['ids']['fldb']
        except (AttributeError, KeyError, TypeError):
            try:
                return self.item['ids']['fldb']
            except (AttributeError, KeyError, TypeError):
                return

    """
    flicklist_slug
    """
    @cached_property
    def flicklist_slug(self):
        return self.get_flicklist_slug()

    def get_flicklist_slug(self):
        try:
            return self.item[self.parent_item_type]['ids']['slug']
        except (AttributeError, KeyError, TypeError):
            try:
                return self.item['ids']['slug']
            except (AttributeError, KeyError, TypeError):
                return

    """
    plays
    """
    @cached_property
    def plays(self):
        return self.get_plays()

    def get_plays(self):
        return self.item.get('plays')

    """
    last_watched_at
    """
    @cached_property
    def last_watched_at(self):
        return self.get_last_watched_at()

    def get_last_watched_at(self):
        return self.item.get('last_watched_at') or self.item.get('watched_at')

    """
    reset_at
    """
    @cached_property
    def reset_at(self):
        return self.get_reset_at()

    def get_reset_at(self):
        return self.item.get('reset_at')

    """
    rating
    """
    @cached_property
    def rating(self):
        return self.get_rating()

    def get_rating(self):
        return self.item.get('rating')

    """
    rated_at
    """
    @cached_property
    def rated_at(self):
        return self.get_rated_at()

    def get_rated_at(self):
        return self.item.get('rated_at')

    """
    progress
    """
    @cached_property
    def progress(self):
        return self.get_progress()

    def get_progress(self):
        progress = self.item.get('progress')
        if progress is None:
            return
        return float(progress) / 100.0

    """
    updated_at
    """
    @cached_property
    def updated_at(self):
        return self.get_updated_at()

    def get_updated_at(self):
        return self.item.get('updated_at')

    """
    id
    """
    @cached_property
    def id(self):
        return self.get_id()

    def get_id(self):
        return self.item.get('updated_at')

    """
    paused
    """
    @cached_property
    def paused(self):
        return self.get_paused()

    def get_paused(self):
        return self.item.get('paused')

    """
    paused_at
    """
    @cached_property
    def paused_at(self):
        return self.get_paused_at()

    def get_paused_at(self):
        return self.item.get('updated_at') if self.item.get('paused') else None

    """
    status
    """
    @cached_property
    def status(self):
        return self.item.get('status')

    """
    premiered
    """
    @cached_property
    def premiered(self):
        return self.get_premiered()

    def get_premiered(self):
        return

    """
    year
    """
    @cached_property
    def year(self):
        return self.get_year()

    def get_year(self):
        try:
            return self.item[self.parent_item_type]['year']
        except (AttributeError, KeyError, TypeError):
            try:
                return self.item['year']
            except (AttributeError, KeyError, TypeError):
                return

    """
    title
    """
    @cached_property
    def title(self):
        return self.get_title()

    def get_title(self):
        try:
            return self.item[self.parent_item_type]['title']
        except (AttributeError, KeyError, TypeError):
            try:
                return self.item['title']
            except (AttributeError, KeyError, TypeError):
                return

    """
    media_type
    """
    @cached_property
    def media_type(self):
        return self.get_media_type()

    def get_media_type(self):
        return self.item.get('media_type')

    """
    episode_name
    """
    @cached_property
    def episode_name(self):
        return self.get_episode_name()

    def get_episode_name(self):
        return self.item.get('episode_name')

    """
    added_at
    """
    @cached_property
    def added_at(self):
        return self.get_added_at()

    def get_added_at(self):
        return self.item.get('added_at')

    """
    started_at
    """
    @cached_property
    def started_at(self):
        return self.get_started_at()

    def get_started_at(self):
        return self.item.get('started_at')

    """
    completed_at
    """
    @cached_property
    def completed_at(self):
        return self.get_completed_at()

    def get_completed_at(self):
        return self.item.get('completed_at')


class FlickListSyncItemConstructor(SyncItemConstructor):
    item_data_class = FlickListSyncItemData


class FlickListSyncItem(SyncItem):

    _additional_keys = (
        'item_type',
        'tmdb_type',
        'tmdb_id',
        'season_number',
        'episode_number',
        'flicklist_id',
        'flicklist_slug',
        'premiered',
        'year',
        'title',
        'status',
        'media_type',
        'episode_name',
        'plays',
        'last_watched_at',
        'reset_at',
        'rating',
        'rated_at',
        'paused',
        'added_at',
        'started_at',
        'completed_at',
    )

    def get_data(self):
        return FlickListSyncItemConstructor(
            self.meta,
            self.keys,
            self.item_type
        ).data
