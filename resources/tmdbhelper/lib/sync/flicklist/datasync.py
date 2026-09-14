#!/usr/bin/python
# -*- coding: utf-8 -*-

from jurialmunkey.ftools import cached_property


class FlickListSyncDataGetterAllUnHiddenShowsInProgress:

    additional_keys = ()

    def __init__(self, instance_syncdata):
        self.instance_syncdata = instance_syncdata

    @cached_property
    def parent_getter(self):
        return self.get_parent_getter()

    def get_parent_getter(self):
        sd = self.instance_syncdata.get_all_unhidden_shows_started_getter()
        sd.additional_keys = self.parent_additional_keys
        return sd

    @cached_property
    def keys(self):
        return self.get_keys()

    def get_keys(self):
        return self.parent_getter.keys

    @property
    def parent_additional_keys(self):
        return (
            'last_watched_at',
            'dropped_hidden_at',
            *(self.additional_keys or ())
        )

    @cached_property
    def items(self):
        return self.get_items()

    def get_items(self):
        sd = self.parent_getter
        return [
            item for item in sd.items
            if item.get('last_watched_at')
        ]
